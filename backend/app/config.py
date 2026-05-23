from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class LLMProvider(str, Enum):
    MOCK = "mock"
    OPENAI = "openai"
    YANDEX = "yandex"
    GIGACHAT = "gigachat"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "ML Gateway"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/ml_gateway"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # ML Service
    ML_SERVICE_URL: str = "http://ml-service:8001/predict"

    # LLM Settings
    LLM_PROVIDER: LLMProvider = LLMProvider.MOCK
    OPENAI_API_KEY: str | None = None

    # Gateway Thresholds
    THRESHOLD_LOW: float = 0.30
    THRESHOLD_HIGH: float = 0.70
    CUMULATIVE_THRESHOLD: float = 0.50
    CUMULATIVE_BLOCK_THRESHOLD: float = 1.0
    CUMULATIVE_SESSIONS_BLOCK_THRESHOLD: float = 1.5

    # Safe notification
    SAFE_NOTIFICATION: str = "Ваш запрос не может быть обработан из-за политики безопасности."

settings = Settings()
