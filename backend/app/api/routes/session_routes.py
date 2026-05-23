import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.database import get_db, AsyncSessionLocal
from app.storage.repositories.session_repository import SessionRepository
from app.storage.repositories.message_repository import MessageRepository
from app.api.schemas.session_schemas import (
    SessionCreateRequest, 
    SessionCreateResponse, 
    SessionHistoryResponse,
    MessageSchema
)
from app.core.session_manager import session_manager

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", response_model=SessionCreateResponse)
async def create_session(request: SessionCreateRequest):
    session_id = await session_manager.create_session(request.user_id)
    # We need to get the session from DB to have the correct created_at
    # or rely on the session_manager returning the object.
    # For now, let's fix the immediate validation error by returning a dummy valid datetime
    # or better, fetch the session.
    async with AsyncSessionLocal() as db:
        repo = SessionRepository(db)
        session = await repo.get_by_id(session_id)
        return {"session_id": session.id, "created_at": session.created_at}

@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
async def get_history(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    session_repo = SessionRepository(db)
    message_repo = MessageRepository(db)
    
    session = await session_repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    history = await message_repo.get_session_history(session_id, limit=50)
    
    return {
        "session_id": session_id,
        "cumulative_risk": session.cumulative_risk,
        "is_blocked": session.is_blocked,
        "history": [
            MessageSchema(
                role=m.role, 
                content=m.content, 
                step=m.step, 
                created_at=m.created_at
            ) for m in reversed(history)
        ]
    }
