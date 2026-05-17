from pathlib import Path
from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Smart Event Planner"
    APP_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "135e6714235de3a416698d0e3068bb46c98a8849c54ef117b245bc9f19355b23"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:4111@localhost:5432/web_project"
    
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
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str) -> str:
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v
    
    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'  # Ignore extra fields in .env
    )

settings = Settings()

if settings.DATABASE_URL.startswith("sqlite"):
    parsed = urlparse(settings.DATABASE_URL)
    db_path = parsed.path
    if settings.DATABASE_URL.startswith("sqlite:///./"):
        db_path = settings.DATABASE_URL.removeprefix("sqlite:///./")
    elif settings.DATABASE_URL.startswith("sqlite:///"):
        db_path = parsed.path.lstrip("/")

    if db_path and db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
