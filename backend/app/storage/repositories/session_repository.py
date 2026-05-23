import uuid
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.models import SessionModel

class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: uuid.UUID | None = None) -> SessionModel:
        session = SessionModel(user_id=user_id)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_by_id(self, session_id: uuid.UUID) -> SessionModel | None:
        result = await self.db.execute(select(SessionModel).where(SessionModel.id == session_id))
        return result.scalar_one_or_none()

    async def update_cumulative_risk(self, session_id: uuid.UUID, risk: float):
        await self.db.execute(
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(cumulative_risk=risk)
        )
        await self.db.commit()

    async def block_session(self, session_id: uuid.UUID):
        await self.db.execute(
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(is_blocked=True)
        )
        await self.db.commit()
