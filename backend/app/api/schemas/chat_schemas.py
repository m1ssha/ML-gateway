import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: uuid.UUID
    message: str = Field(..., min_length=1, max_length=4000)

class ChatResponse(BaseModel):
    session_id: uuid.UUID
    step: int
    status: str # 'passed', 'reviewed', 'blocked'
    reply: str
    risk_score: float
    is_attack: bool
