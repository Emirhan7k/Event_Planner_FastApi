from fastapi import APIRouter

from app.schemas.event import Event, EventCreate
from app.services.event_service import event_service

router = APIRouter()


@router.get("", response_model=list[Event])
def list_events() -> list[Event]:
    return event_service.list_events()


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int) -> Event:
    return event_service.get_event(event_id)


@router.post("", response_model=Event)
def create_event(payload: EventCreate) -> Event:
    return event_service.create_event(payload)
