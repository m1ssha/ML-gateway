import uuid
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.database import get_db
from app.storage.models import EventLogModel, SessionModel, MessageModel
from app.storage.repositories.event_repository import EventRepository
from app.api.schemas.admin_schemas import AdminStatsResponse, LogEntry

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/logs", response_model=list[LogEntry])
async def get_logs(session_id: uuid.UUID | None = None, limit: int = 100, db: AsyncSession = Depends(get_db)):
    repo = EventRepository(db)
    logs = await repo.get_logs(session_id, limit)
    return logs

@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    # 1. Всего запросов (событий типа 'request')
    total_q = await db.execute(select(func.count()).select_from(EventLogModel).where(EventLogModel.event_type == 'request'))
    total_requests = total_q.scalar() or 0
    
    # 2. Заблокировано
    blocked_q = await db.execute(select(func.count()).select_from(EventLogModel).where(EventLogModel.event_type == 'block'))
    blocked_requests = blocked_q.scalar() or 0
    
    # 3. Средний риск
    risk_q = await db.execute(select(func.avg(MessageModel.risk_score)).select_from(MessageModel))
    avg_risk_score = risk_q.scalar() or 0.0
    
    # 4. Активных сессий
    sessions_q = await db.execute(select(func.count()).select_from(SessionModel))
    active_sessions = sessions_q.scalar() or 0
    
    return {
        "total_requests": total_requests,
        "blocked_requests": blocked_requests,
        "avg_risk_score": float(avg_risk_score),
        "active_sessions": active_sessions
    }
