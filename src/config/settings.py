# app/config/settings.py
from pydantic import BaseSettings, Field, AnyHttpUrl

class Settings(BaseSettings):
    APP_NAME: str = "Women Public Safety Chat"
    API_V1_PREFIX: str = "/api/v1"

    MISTRAL_API_KEY: str = Field(..., min_length=10)
    MISTRAL_API_BASE: AnyHttpUrl = "https://api.mistral.ai/v1"
    REQUEST_TIMEOUT_SECONDS: int = 30
    HISTORY_MAXLEN: int = 6

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
