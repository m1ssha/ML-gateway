from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class LLMProvider(str, Enum):
    MOCK = "mock"
    OPENAI = "openai"
    YANDEX = "yandex"
    GIGACHAT = "gigachat"
    OPENROUTER = "openrouter"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "ML Gateway"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/ml_gateway"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # ML Service
    ML_SERVICE_URL: str = "http://ml-service:8000/predict"

    # LLM Settings
    LLM_PROVIDER: LLMProvider = LLMProvider.OPENROUTER
    LLM_MODEL: str = "qwen/qwen3.6-35b-a3b"
    LLM_TIMEOUT: float = 15.0
    LLM_MAX_RETRIES: int = 1

    # OpenAI Credentials
    OPENAI_API_KEY: str | None = None

    # OpenRouter Credentials
    OPENROUTER_API_KEY: str | None = None
    HTTP_REFERER: str = "https://llm-gateway.local"
    APP_TITLE: str = "LLM Security Gateway Prototype"

    # Gateway Thresholds
    THRESHOLD_LOW: float = 0.30
    THRESHOLD_HIGH: float = 0.70
    CUMULATIVE_THRESHOLD: float = 0.50
    CUMULATIVE_BLOCK_THRESHOLD: float = 1.0
    CUMULATIVE_SESSIONS_BLOCK_THRESHOLD: float = 1.5

    # Safe notification
    SAFE_NOTIFICATION: str = "Ваш запрос не может быть обработан из-за политики безопасности."

settings = Settings()
