from pydantic import BaseModel

from app.schemas.event import Event


class Recommendation(BaseModel):
    event: Event
    score: int
    reason: str
    tags: list[str]
