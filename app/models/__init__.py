# Import all models here so Alembic can discover them
from app.db.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.registration import Registration  # noqa: F401

__all__ = ["Base", "User", "Event", "Registration"]
