from datetime import datetime

from pydantic import BaseModel


class RecommendedEvent(BaseModel):
    """An event with its recommendation score for a user."""
    model_config = {"from_attributes": True}

    id: int
    title: str
    description: str
    location: str
    event_date: datetime
    category: str
    tags: list[str]
    image_url: str | None
    source_url: str | None = None
    capacity: int
    registered_count: int
    is_full: bool
    is_favorited: bool = False
    score: float  # cosine similarity 0.0–1.0
    score_percent: int  # score * 100 rounded


class RecommendationResult(BaseModel):
    """Full recommendation response for a user."""
    user_id: int
    recommendations: list[RecommendedEvent]
    based_on_interests: list[str]
    total_events_analyzed: int


class SimilarEvent(BaseModel):
    """Similar event result."""
    id: int
    title: str
    category: str
    tags: list[str]
    image_url: str | None
    source_url: str | None = None
    event_date: datetime
    is_favorited: bool = False
    score: float
    score_percent: int
