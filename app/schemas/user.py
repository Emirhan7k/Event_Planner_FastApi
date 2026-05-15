from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    interests: list[str] = []


class UserRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: str
    username: str
    full_name: str
    bio: str | None
    avatar_url: str | None
    interests: list[str]
    role: UserRole
    is_active: bool
    created_at: datetime


class UserPublic(BaseModel):
    """Public profile — no sensitive fields."""
    model_config = {"from_attributes": True}

    id: int
    username: str
    full_name: str
    bio: str | None
    avatar_url: str | None
    interests: list[str]
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None

    @field_validator("full_name")
    @classmethod
    def not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("full_name cannot be empty.")
        return v


class UserInterestsUpdate(BaseModel):
    interests: list[str]

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: list[str]) -> list[str]:
        cleaned = [i.strip().lower() for i in v if i.strip()]
        if len(cleaned) > 20:
            raise ValueError("Maximum 20 interests allowed.")
        return cleaned


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class UserWithStats(UserRead):
    events_created: int = 0
    events_registered: int = 0
