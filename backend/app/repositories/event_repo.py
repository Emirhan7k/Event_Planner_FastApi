from app.schemas.event import Event, EventCreate


class EventRepository:
    def __init__(self) -> None:
        self._events = [
            Event(id=1, title="Veri Bilimi ve Gelecek: Seminer", description="AI ve veri bilimi kariyer trendleri.", date="14 Mayis", time="18:30", location="Online", category="Teknoloji", match_score=92),
            Event(id=2, title="Yazilim Mimari Atolyesi", description="Olceklenebilir servis tasarimi.", date="14 Mayis", time="18:30", location="Online", category="Teknoloji", match_score=87),
            Event(id=3, title="Veri Bilimi ve Gelecek: Sanat", description="Yaratici uretimde veri kullanimi.", date="15 Mayis", time="16:00", location="Kultur Merkezi", category="Sanat", match_score=73),
        ]

    def list(self) -> list[Event]:
        return self._events

    def get(self, event_id: int) -> Event:
        return next(event for event in self._events if event.id == event_id)

    def create(self, payload: EventCreate) -> Event:
        event = Event(id=len(self._events) + 1, **payload.model_dump())
        self._events.append(event)
        return event


event_repository = EventRepository()
