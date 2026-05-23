from abc import ABC, abstractmethod

class BaseLLMAdapter(ABC):
    @abstractmethod
    async def generate(self, user_message: str, history: list[dict], system_prompt: str | None = None) -> str:
        """
        Генерирует ответ от LLM.
        history: список словарей [{"role": "user", "content": "..."}, ...]
        """
        pass
