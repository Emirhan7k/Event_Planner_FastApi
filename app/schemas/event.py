from datetime import datetime

from pydantic import BaseModel, field_validator


VALID_CATEGORIES = [
    "music", "tech", "food", "sports", "art", "education",
    "business", "health", "travel", "gaming", "film", "fashion", "other"
]


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    event_date: datetime
    capacity: int = 100
    category: str
    tags: list[str] = []
    source_url: str | None = None
    image_url: str | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty.")
        if len(v) > 200:
            raise ValueError("Title max 200 chars.")
        return v.strip()

    @field_validator("capacity")
    @classmethod
    def capacity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Capacity must be at least 1.")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return v

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: list[str]) -> list[str]:
        return [t.strip().lower() for t in v if t.strip()][:15]


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    event_date: datetime | None = None
    capacity: int | None = None
    category: str | None = None
    tags: list[str] | None = None
    source_url: str | None = None
    is_active: bool | None = None


class EventRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    title: str
    description: str
    location: str
    event_date: datetime
    capacity: int
    category: str
    tags: list[str]
    image_url: str | None
    source_url: str | None
    is_active: bool
    owner_id: int
    created_at: datetime
    registered_count: int
    is_full: bool
    is_favorited: bool = False


class EventListResponse(BaseModel):
    items: list[EventRead]
    total: int
    page: int
    size: int
    pages: int


class EventDetailRead(EventRead):
    """Event with owner info and registration status."""
    owner_username: str | None = None
    is_registered: bool = False
    is_favorited: bool = False
    recommendation_score: float | None = None
