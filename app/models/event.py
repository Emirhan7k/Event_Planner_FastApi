from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.registration import Registration


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(300), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # JSON list of tags for TF-IDF recommendation e.g. ["jazz", "live music", "outdoor"]
    tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # FK
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="events")
    registrations: Mapped[list["Registration"]] = relationship(
        "Registration", back_populates="event", lazy="selectin"
    )

    @property
    def registered_count(self) -> int:
        return sum(1 for r in self.registrations if r.status == "confirmed")

    @property
    def is_full(self) -> bool:
        return self.registered_count >= self.capacity

    def __repr__(self) -> str:
        return f"<Event id={self.id} title={self.title!r}>"
