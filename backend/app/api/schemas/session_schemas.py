import uuid
from datetime import datetime
from pydantic import BaseModel

class SessionCreateRequest(BaseModel):
    user_id: uuid.UUID | None = None

class SessionCreateResponse(BaseModel):
    session_id: uuid.UUID
    created_at: datetime

class MessageSchema(BaseModel):
    role: str
    content: str
    step: int
    created_at: datetime

class SessionHistoryResponse(BaseModel):
    session_id: uuid.UUID
    cumulative_risk: float
    is_blocked: bool
    history: list[MessageSchema]
