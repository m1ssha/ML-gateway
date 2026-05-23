import uuid
import httpx
import logging
import time
from typing import Any
from app.config import settings

logger = logging.getLogger(__name__)

class MLClient:
    def __init__(self):
        self.url = settings.ML_SERVICE_URL
        self.timeout = 2.0

    async def predict(self, session_id: uuid.UUID, context: str) -> dict[str, Any]:
        """
        Вызывает ML-сервис для оценки риска.
        Реализует fail-closed логику и ретраи.
        """
        async with httpx.AsyncClient() as client:
            for attempt in range(2):
                try:
                    start_time = time.time()
                    response = await client.post(
                        self.url,
                        json={"session_id": str(session_id), "context": context},
                        timeout=self.timeout
                    )
                    response.raise_for_status()
                    data = response.json()
                    data["inference_ms"] = int((time.time() - start_time) * 1000)
                    return data
                except (httpx.HTTPError, httpx.TimeoutException) as e:
                    logger.warning(f"ML service error (attempt {attempt+1}): {e}")
                    if attempt == 0:
                        await asyncio.sleep(0.5) # Маленькая задержка перед ретраем
                        continue
                    
        # Fail-closed: если сервис недоступен, возвращаем максимальный риск
        return {
            "is_attack": True,
            "prob_attack": 1.0,
            "risk_score": 1.0,
            "inference_ms": 0,
            "model_version": "fail-closed",
            "error": "ML service unavailable"
        }

ml_client = MLClient()
import asyncio # For sleep in retry
