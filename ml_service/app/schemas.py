from pydantic import BaseModel, Field
from typing import Optional

class PredictRequest(BaseModel):
    session_id: str = Field(..., example="uuid-string")
    context: str = Field(..., example="USER: hello\nASSISTANT: hi")

class PredictResponse(BaseModel):
    is_attack: bool
    prob_attack: float
    risk_score: float
    inference_ms: int
    model_version: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
