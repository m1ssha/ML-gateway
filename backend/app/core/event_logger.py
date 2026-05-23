import asyncio
import uuid
import logging
from typing import Any
from app.storage.database import AsyncSessionLocal
from app.storage.repositories.event_repository import EventRepository

logger = logging.getLogger(__name__)

class EventLogger:
    @staticmethod
    async def log(session_id: uuid.UUID | None, event_type: str, payload: dict[str, Any]):
        """
        Асинхронно записывает событие в лог. 
        Использует новый сеанс БД, чтобы не мешать основной транзакции.
        """
        async def _persist():
            try:
                async with AsyncSessionLocal() as db:
                    repo = EventRepository(db)
                    await repo.log_event(session_id, event_type, payload)
            except Exception as e:
                logger.error(f"Failed to log event {event_type} for session {session_id}: {e}")

        # Запускаем фоновую задачу, чтобы не блокировать основной поток
        asyncio.create_task(_persist())

event_logger = EventLogger()
