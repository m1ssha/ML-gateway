import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.models import MessageModel

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(
        self, 
        session_id: uuid.UUID, 
        step: int, 
        role: str, 
        content: str, 
        risk_score: float | None = None,
        is_attack: bool | None = None,
        decision: str | None = None
    ) -> MessageModel:
        message = MessageModel(
            session_id=session_id,
            step=step,
            role=role,
            content=content,
            risk_score=risk_score,
            is_attack=is_attack,
            decision=decision
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_session_history(self, session_id: uuid.UUID, limit: int = 10) -> Sequence[MessageModel]:
        result = await self.db.execute(
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.step.desc())
            .limit(limit)
        )
        return result.scalars().all()
