import uuid
from datetime import datetime
from pydantic import BaseModel

class LogEntry(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID | None
    event_type: str
    payload: dict
    created_at: datetime

class AdminStatsResponse(BaseModel):
    total_requests: int
    blocked_requests: int
    avg_risk_score: float
    active_sessions: int
