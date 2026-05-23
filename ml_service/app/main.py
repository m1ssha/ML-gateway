import time
import torch
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .schemas import PredictRequest, PredictResponse, HealthResponse
from .loader import load_model, load_tokenizer, get_device
from .config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# State container
class AppState:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None

state = AppState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting ML service...")
    try:
        state.device = get_device()
        logger.info(f"Using device: {state.device}")
        
        state.tokenizer = load_tokenizer()
        logger.info("Tokenizer loaded successfully")
        
        state.model = load_model(state.device)
        logger.info(f"Model {settings.MODEL_NAME} loaded successfully")
        
        # Log some info as requested
        logger.info(f"Model version: {settings.MODEL_VERSION}")
        logger.info(f"Attack threshold: {settings.ATTACK_THRESHOLD}")
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        # In a real production app, we might want to exit here
        raise RuntimeError("Initialization failed") from e
        
    yield
    # Shutdown
    logger.info("Shutting down ML service...")
    # Clean up resources if necessary
    state.model = None
    state.tokenizer = None

app = FastAPI(title="ML Gateway Protection Service", lifespan=lifespan)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        model_loaded=state.model is not None,
        device=str(state.device)
    )

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    if state.model is None or state.tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.perf_counter()
    
    try:
        # 1. Tokenization
        inputs = state.tokenizer(
            request.context,
            truncation=True,
            max_length=settings.MAX_LENGTH,
            padding=False, # Single request, padding not strictly needed but can be added
            return_tensors="pt"
        ).to(state.device)
        
        # 2. Inference
        with torch.inference_mode():
            logits, risk_score = state.model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            
            # 3. Post-processing
            prob_attack = torch.sigmoid(logits).item()
            risk_score_val = risk_score.item()
            is_attack = prob_attack >= settings.ATTACK_THRESHOLD
            
        inference_time_ms = int((time.perf_counter() - start_time) * 1000)
        
        return PredictResponse(
            is_attack=is_attack,
            prob_attack=round(prob_attack, 4),
            risk_score=round(risk_score_val, 4),
            inference_ms=inference_time_ms,
            model_version=settings.MODEL_VERSION
        )
        
    except Exception as e:
        logger.error(f"Prediction error for session {request.session_id}: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error during inference"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
