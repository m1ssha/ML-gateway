import httpx
from app.config import settings
from app.services.llm_adapters.base_adapter import BaseLLMAdapter

class OpenAIAdapter(BaseLLMAdapter):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def generate(self, user_message: str, history: list[dict], system_prompt: str | None = None) -> str:
        if not self.api_key:
            return "Ошибка: API ключ OpenAI не настроен."

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Добавляем историю
        messages.extend(history)
        # Добавляем текущее сообщение
        messages.append({"role": "user", "content": user_message})

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "temperature": 0.7
                    },
                    timeout=15.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Ошибка при вызове OpenAI: {str(e)}"
