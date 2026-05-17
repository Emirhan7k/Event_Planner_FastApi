from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Smart Event Planner"
    APP_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-it-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/event_planner.db"
    
    # Uploads
    UPLOAD_DIR: str = "static/uploads"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Extra settings from .env
    DEBUG: bool = False
    MAX_UPLOAD_SIZE_MB: int = 5

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "production", "prod"}:
                return False
            if normalized in {"development", "dev"}:
                return True
        return value
    
    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'  # Ignore extra fields in .env
    )

settings = Settings()
