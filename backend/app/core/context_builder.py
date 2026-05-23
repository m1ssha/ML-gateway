import uuid
import json
from app.storage.redis_client import get_redis
from app.storage.repositories.message_repository import MessageRepository
from app.storage.database import AsyncSessionLocal

class ContextBuilder:
    @staticmethod
    async def build_context(session_id: uuid.UUID, limit: int = 4) -> str:
        """
        Формирует скользящее окно из последних N реплик диалога.
        Сначала пытается получить из Redis, если нет - из БД.
        """
        redis = await get_redis()
        cache_key = f"context:{session_id}"
        
        # 1. Пробуем Redis
        cached_context = await redis.get(cache_key)
        if cached_context:
            return cached_context

        # 2. Если нет в Redis, берем из БД
        async with AsyncSessionLocal() as db:
            repo = MessageRepository(db)
            messages = await repo.get_session_history(session_id, limit=limit)
            
        # Сортируем по шагу (repo возвращает desc, нам нужен asc для контекста)
        messages = sorted(messages, key=lambda m: m.step)
        
        # 3. Форматируем
        context_parts = []
        for msg in messages:
            role_marker = f"[{msg.role.upper()}]"
            context_parts.append(f"{role_marker} {msg.content}")
        
        context_str = "\n".join(context_parts)
        
        # 4. Обрезаем, если слишком длинный (~1500 символов)
        if len(context_str) > 1500:
            context_str = context_str[-1500:]

        # 5. Кэшируем в Redis на 30 минут
        await redis.set(cache_key, context_str, ex=1800)
        
        return context_str

context_builder = ContextBuilder()
