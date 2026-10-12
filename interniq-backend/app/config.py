from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    APP_NAME: str = "InternIQ"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite+aiosqlite:///./interniq.db"
    DATABASE_URL_SYNC: Optional[str] = None

    SECRET_KEY: str = Field(min_length=32)

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret(cls, value: str) -> str:
        if "change-me" in value.lower() or "dev-secret" in value.lower() or len(set(value)) < 12:
            raise ValueError("SECRET_KEY must be a randomly generated secret")
        return value
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "doc", "docx"]

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
