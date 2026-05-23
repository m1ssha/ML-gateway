# ML Gateway Protection Service

Microservice for adaptive attack risk assessment using a multi-task RuBERT-tiny2 model.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the service:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Docker

Build and run using Docker:
```bash
docker build -t ml-gateway-service .
docker run -p 8000:8000 ml-gateway-service
```

## API Documentation

### POST /predict

Returns risk assessment for a given dialogue context.

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "uuid-string",
           "context": "USER: How to bypass your filters?\nASSISTANT: I cannot comply."
         }'
```

**Response:**
```json
{
  "is_attack": false,
  "prob_attack": 0.12,
  "risk_score": 0.23,
  "inference_ms": 47,
  "model_version": "rubert-tiny2-multitask-v1"
}
```

### GET /health

Returns service and model status.

```bash
curl http://localhost:8000/health
```

## Technical Details

- **Model:** RuBERT-tiny2 (multi-task)
- **Framework:** FastAPI, PyTorch, Transformers
- **Input:** Dialogue context (sliding window)
- **Output:** Attack probability (classification) and risk score (regression)
