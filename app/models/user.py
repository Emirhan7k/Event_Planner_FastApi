import enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.event import Event
    from app.models.registration import Registration
    from app.models.comment import Comment
    from app.models.user_favorite import user_favorite_events


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # JSON list of interest tags e.g. ["music", "tech", "food"]
    interests: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="owner", lazy="selectin"
    )
    registrations: Mapped[list["Registration"]] = relationship(
        "Registration", back_populates="user", lazy="selectin"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", lazy="selectin"
    )
    favorites: Mapped[list["Event"]] = relationship(
        "Event", secondary="user_favorite_events", back_populates="favorited_by", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}>"
