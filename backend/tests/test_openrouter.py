import asyncio
import json
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
import pytest
from app.services.llm_adapters.openrouter_adapter import OpenRouterAdapter
from app.core.exceptions import LLMProviderError
from app.config import settings

async def test_openrouter_success():
    print("Testing OpenRouter success case...")
    adapter = OpenRouterAdapter()
    adapter.api_key = "test_key"
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Test response"
                }
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        
        response = await adapter.generate("Hello", [], "Be helpful")
        
        assert response == "Test response"
        mock_post.assert_called_once()
        print("✅ Success case passed")

async def test_openrouter_rate_limit_retry():
    print("Testing OpenRouter rate limit retry...")
    adapter = OpenRouterAdapter()
    adapter.api_key = "test_key"
    adapter.max_retries = 1
    
    # First response is 429, second is 200
    mock_response_429 = MagicMock()
    mock_response_429.status_code = 429
    
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "choices": [{"message": {"content": "Retry success"}}]
    }
    mock_response_200.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = [mock_response_429, mock_response_200]
        
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            response = await adapter.generate("Hello", [])
            
            assert response == "Retry success"
            assert mock_post.call_count == 2
            mock_sleep.assert_called_with(2) # 2**(0+1)
            print("✅ Rate limit retry passed")

async def test_openrouter_server_error_retry():
    print("Testing OpenRouter server error retry...")
    adapter = OpenRouterAdapter()
    adapter.api_key = "test_key"
    adapter.max_retries = 1
    
    mock_response_500 = MagicMock()
    mock_response_500.status_code = 500
    
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "choices": [{"message": {"content": "Server error retry success"}}]
    }
    mock_response_200.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = [mock_response_500, mock_response_200]
        
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            response = await adapter.generate("Hello", [])
            
            assert response == "Server error retry success"
            assert mock_post.call_count == 2
            mock_sleep.assert_called_with(2)
            print("✅ Server error retry passed")

async def test_openrouter_timeout_retry():
    print("Testing OpenRouter timeout retry...")
    adapter = OpenRouterAdapter()
    adapter.api_key = "test_key"
    adapter.max_retries = 1
    
    mock_response_200 = MagicMock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "choices": [{"message": {"content": "Timeout retry success"}}]
    }
    mock_response_200.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = [httpx.TimeoutException("Timeout"), mock_response_200]
        
        response = await adapter.generate("Hello", [])
        
        assert response == "Timeout retry success"
        assert mock_post.call_count == 2
        print("✅ Timeout retry passed")

async def test_openrouter_auth_error():
    print("Testing OpenRouter auth error...")
    adapter = OpenRouterAdapter()
    adapter.api_key = "invalid_key"
    
    mock_response_401 = MagicMock()
    mock_response_401.status_code = 401
    # Simulate raise_for_status for 401
    mock_response_401.raise_for_status.side_effect = httpx.HTTPStatusError("Auth error", request=MagicMock(), response=mock_response_401)

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response_401
        
        with pytest.raises(LLMProviderError) as excinfo:
            await adapter.generate("Hello", [])
        
        assert "authentication failed: 401" in str(excinfo.value)
        print("✅ Auth error handling passed")

async def run_all_tests():
    try:
        await test_openrouter_success()
        await test_openrouter_rate_limit_retry()
        await test_openrouter_server_error_retry()
        await test_openrouter_timeout_retry()
        await test_openrouter_auth_error()
        print("\nAll OpenRouter tests passed! 🚀")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
