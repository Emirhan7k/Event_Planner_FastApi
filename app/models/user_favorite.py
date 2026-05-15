from sqlalchemy import Column, ForeignKey, Table
from app.db.base import Base

user_favorite_events = Table(
    "user_favorite_events",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
)
