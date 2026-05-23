import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_NAME: str = "rubert-tiny2-multitask-v1"
    ARTIFACTS_PATH: str = os.getenv("ARTIFACTS_PATH", "ml-artifacts")
    
    CONFIG_FILENAME: str = "config.json"
    TOKENIZER_FILENAME: str = "tokenizer.json"
    TOKENIZER_CONFIG_FILENAME: str = "tokenizer-config.json"
    WEIGHTS_FILENAME: str = "model-weights.pt"
    
    MAX_LENGTH: int = 512
    ATTACK_THRESHOLD: float = 0.5
    
    MODEL_VERSION: str = "rubert-tiny2-multitask-v1"

    class Config:
        env_file = ".env"

settings = Settings()
