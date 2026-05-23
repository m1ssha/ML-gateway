import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from app.core.session_manager import SessionManager
from app.config import settings

async def test_bypass():
    print("🚀 Starting First Message Bypass Verification...")
    
    with patch("app.core.session_manager.AsyncSessionLocal") as mock_db, \
         patch("app.core.session_manager.SessionRepository") as mock_session_repo, \
         patch("app.core.session_manager.MessageRepository") as mock_message_repo, \
         patch("app.core.session_manager.ml_client.predict") as mock_ml_predict, \
         patch("app.core.session_manager.context_builder.build_context") as mock_build_context, \
         patch("app.core.session_manager.llm_provider.get_adapter") as mock_get_llm, \
         patch("app.core.session_manager.event_logger.log") as mock_log, \
         patch("app.core.session_manager.get_redis") as mock_get_redis:

        # Setup Redis mock
        mock_redis = AsyncMock()
        mock_get_redis.return_value = mock_redis
        
        session_id = uuid.uuid4()
        mock_session = MagicMock()
        mock_session.id = session_id
        mock_session.cumulative_risk = 0.0
        mock_session.is_blocked = False
        
        mock_session_repo_inst = mock_session_repo.return_value
        mock_session_repo_inst.get_by_id = AsyncMock(return_value=mock_session)
        
        mock_message_repo_inst = mock_message_repo.return_value
        mock_message_repo_inst.add_message = AsyncMock()
        
        mock_llm_adapter = AsyncMock()
        mock_llm_adapter.generate.return_value = "Assistant reply"
        mock_get_llm.return_value = mock_llm_adapter

        sm = SessionManager()

        # Тест 1: ПЕРВОЕ сообщение
        print("\nTest 1: First message should bypass ML")
        mock_message_repo_inst.get_session_history = AsyncMock(return_value=[]) # Empty history = step 1
        
        response = await sm.process_chat_message(session_id, "First message")
        
        print(f"Response status: {response['status']}")
        print(f"Model used: {response['model']}")
        assert response["status"] == "passed"
        assert response["model"] == settings.LLM_MODEL
        assert mock_ml_predict.call_count == 0, "ML predict should NOT be called on step 1"
        assert mock_redis.delete.called, "Redis cache should be deleted"
        print("✅ Step 1 bypass confirmed")

        # Тест 2: ВТОРОЕ сообщение
        print("\nTest 2: Second message should call ML")
        # Mock history for step 2
        mock_msg = MagicMock()
        mock_msg.step = 2 # Last message was step 2 (assistant reply)
        mock_message_repo_inst.get_session_history = AsyncMock(return_value=[mock_msg])
        
        mock_ml_predict.return_value = {
            "is_attack": False,
            "risk_score": 0.1
        }
        
        response = await sm.process_chat_message(session_id, "Second message")
        
        print(f"Response status: {response['status']}")
        assert mock_ml_predict.call_count == 1, "ML predict SHOULD be called on step 2"
        print("✅ Step 2 ML call confirmed")

    print("\n✅ Verification completed successfully!")

if __name__ == "__main__":
    import sys
    import os
    # Add app to path
    sys.path.append(os.path.join(os.getcwd(), "backend"))
    asyncio.run(test_bypass())
