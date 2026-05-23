import asyncio
import logging
import httpx
from app.config import settings
from app.services.llm_adapters.base_adapter import BaseLLMAdapter
from app.core.exceptions import LLMProviderError

logger = logging.getLogger(__name__)

class OpenRouterAdapter(BaseLLMAdapter):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model_id = settings.LLM_MODEL
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.LLM_MAX_RETRIES
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.HTTP_REFERER,
            "X-Title": settings.APP_TITLE,
            "Content-Type": "application/json"
        }

    async def generate(self, user_message: str, history: list[dict], system_prompt: str | None = None) -> str:
        if not self.api_key:
            logger.error("OpenRouter API key is not configured")
            raise LLMProviderError("OpenRouter API key is not configured")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        logger.info(f"DEBUG: Sending request to OpenRouter. Model: {self.model_id}")

        retries = 0
        while retries <= self.max_retries:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.base_url,
                        headers=self.headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 429:
                        # Rate Limit: exponential backoff (1 retry)
                        if retries < self.max_retries:
                            wait_time = 2 ** (retries + 1)
                            logger.warning(f"Rate limited by OpenRouter. Retrying in {wait_time}s...")
                            await asyncio.sleep(wait_time)
                            retries += 1
                            continue
                        else:
                            logger.error("Rate limit exceeded and no more retries left")
                            raise LLMProviderError("OpenRouter rate limit exceeded")

                    if 500 <= response.status_code < 600:
                        # Server Error: 1 retry with delay
                        if retries < self.max_retries:
                            wait_time = 2
                            logger.warning(f"OpenRouter server error {response.status_code}. Retrying in {wait_time}s...")
                            await asyncio.sleep(wait_time)
                            retries += 1
                            continue
                        else:
                            logger.error(f"OpenRouter server error {response.status_code} and no more retries left")
                            raise LLMProviderError(f"OpenRouter server error: {response.status_code}")

                    response.raise_for_status()
                    data = response.json()
                    
                    if "choices" not in data or not data["choices"]:
                        logger.error(f"Invalid response from OpenRouter: {data}")
                        raise LLMProviderError("Invalid response format from OpenRouter")
                        
                    return data["choices"][0]["message"]["content"]

            except httpx.TimeoutException:
                logger.error(f"Timeout while calling OpenRouter (retry {retries}/{self.max_retries})")
                if retries < self.max_retries:
                    retries += 1
                    continue
                raise LLMProviderError("OpenRouter request timed out")
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (401, 403):
                    logger.error(f"Authentication error with OpenRouter: {e.response.status_code}")
                    raise LLMProviderError(f"OpenRouter authentication failed: {e.response.status_code}")
                logger.error(f"HTTP error from OpenRouter: {e.response.status_code}")
                raise LLMProviderError(f"OpenRouter HTTP error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Unexpected error calling OpenRouter: {str(e)}", exc_info=True)
                raise LLMProviderError(f"Unexpected error calling OpenRouter: {str(e)}")

        raise LLMProviderError("Failed to get response from OpenRouter after retries")
