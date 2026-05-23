import asyncio
from app.services.llm_adapters.base_adapter import BaseLLMAdapter

class MockAdapter(BaseLLMAdapter):
    async def generate(self, user_message: str, history: list[dict], system_prompt: str | None = None) -> str:
        """
        Имитирует задержку и возвращает детерминированный ответ.
        """
        await asyncio.sleep(0.5)
        
        if "hello" in user_message.lower():
            return "Привет! Я защищенный ассистент ML Gateway. Чем могу помочь?"
        
        if len(user_message) > 50:
            return f"Вы написали довольно длинное сообщение ({len(user_message)} симв.). Я проанализировал его и готов к работе."
            
        return f"Это имитация ответа на ваш запрос: '{user_message}'. Шлюз работает корректно."
