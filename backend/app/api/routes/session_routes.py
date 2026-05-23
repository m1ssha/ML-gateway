import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.database import get_db
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

@router.post("/", response_model=SessionCreateResponse)
async def create_session(request: SessionCreateRequest):
    session_id = await session_manager.create_session(request.user_id)
    return {"session_id": session_id, "created_at": uuid.uuid4().hex} # Mock created_at for simple response

@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
async def get_history(session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    message_repo = MessageRepository(db)
    history = await message_repo.get_session_history(session_id, limit=50)
    
    return {
        "session_id": session_id,
        "history": [
            MessageSchema(
                role=m.role, 
                content=m.content, 
                step=m.step, 
                created_at=m.created_at
            ) for m in reversed(history)
        ]
    }
