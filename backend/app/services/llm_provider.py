from app.config import settings, LLMProvider
from app.services.llm_adapters.base_adapter import BaseLLMAdapter
from app.services.llm_adapters.mock_adapter import MockAdapter
from app.services.llm_adapters.openai_adapter import OpenAIAdapter

class LLMProviderFactory:
    @staticmethod
    def get_adapter() -> BaseLLMAdapter:
        if settings.LLM_PROVIDER == LLMProvider.OPENAI:
            return OpenAIAdapter()
        # По умолчанию или при выборе mock
        return MockAdapter()

llm_provider = LLMProviderFactory()
