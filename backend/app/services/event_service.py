from fastapi import HTTPException

from app.repositories.event_repo import event_repository
from app.schemas.event import Event, EventCreate


class EventService:
    def list_events(self) -> list[Event]:
        return event_repository.list()

    def get_event(self, event_id: int) -> Event:
        try:
            return event_repository.get(event_id)
        except StopIteration as exc:
            raise HTTPException(status_code=404, detail="Event not found") from exc

    def create_event(self, payload: EventCreate) -> Event:
        return event_repository.create(payload)


event_service = EventService()
