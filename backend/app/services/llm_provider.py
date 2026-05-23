from app.config import settings, LLMProvider
from app.services.llm_adapters.base_adapter import BaseLLMAdapter
from app.services.llm_adapters.mock_adapter import MockAdapter
from app.services.llm_adapters.openai_adapter import OpenAIAdapter
from app.services.llm_adapters.openrouter_adapter import OpenRouterAdapter

class LLMProviderFactory:
    @staticmethod
    def get_adapter() -> BaseLLMAdapter:
        print(f"DEBUG: Current LLM_PROVIDER from settings: '{settings.LLM_PROVIDER}'")
        if settings.LLM_PROVIDER == LLMProvider.OPENAI:
            print("DEBUG: Selecting OpenAIAdapter")
            return OpenAIAdapter()
        elif settings.LLM_PROVIDER == LLMProvider.OPENROUTER:
            print("DEBUG: Selecting OpenRouterAdapter")
            return OpenRouterAdapter()
        # По умолчанию или при выборе mock
        print("DEBUG: Selecting MockAdapter (fallback)")
        return MockAdapter()

llm_provider = LLMProviderFactory()
