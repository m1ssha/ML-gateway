import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.chat_schemas import ChatRequest, ChatResponse
from app.core.session_manager import session_manager

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def process_message(request: ChatRequest):
    """
    Основной эндпоинт для обработки сообщений чата.
    """
    try:
        result = await session_manager.process_chat_message(request.session_id, request.message)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
