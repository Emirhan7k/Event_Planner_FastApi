from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str
    date: str
    time: str
    location: str
    category: str
    image: str = "/images/event-tech.jpg"


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    match_score: int = 80
