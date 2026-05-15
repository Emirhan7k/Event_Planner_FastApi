from datetime import datetime

from pydantic import BaseModel

from app.models.registration import RegistrationStatus


class RegistrationRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    event_id: int
    status: RegistrationStatus
    registered_at: datetime


class RegistrationWithEvent(RegistrationRead):
    """Registration with embedded event info for dashboard."""
    event_title: str | None = None
    event_date: datetime | None = None
    event_location: str | None = None
    event_category: str | None = None
    event_image_url: str | None = None
