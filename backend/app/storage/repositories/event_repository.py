import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.models import EventLogModel

class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(self, session_id: uuid.UUID | None, event_type: str, payload: dict) -> EventLogModel:
        event = EventLogModel(
            session_id=session_id,
            event_type=event_type,
            payload=payload
        )
        self.db.add(event)
        await self.db.commit()
        return event

    async def get_logs(self, session_id: uuid.UUID | None = None, limit: int = 100) -> Sequence[EventLogModel]:
        query = select(EventLogModel).order_by(EventLogModel.created_at.desc()).limit(limit)
        if session_id:
            query = query.where(EventLogModel.session_id == session_id)
        
        result = await self.db.execute(query)
        return result.scalars().all()
