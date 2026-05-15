from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.event import Event
from app.models.user_favorite import user_favorite_events
from app.core.exceptions import NotFoundError

class FavoriteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def toggle_favorite(self, user: User, event_id: int) -> bool:
        """Toggle favorite status for an event. Returns True if favorited, False if unfavorited."""
        # Check if event exists
        result = await self.session.execute(select(Event).where(Event.id == event_id, Event.is_active == True))
        event = result.scalar_one_or_none()
        if not event:
            raise NotFoundError("Event")

        # Check if already favorited
        query = select(user_favorite_events).where(
            user_favorite_events.c.user_id == user.id,
            user_favorite_events.c.event_id == event_id
        )
        existing = await self.session.execute(query)
        
        if existing.first():
            # Remove from favorites
            await self.session.execute(
                delete(user_favorite_events).where(
                    user_favorite_events.c.user_id == user.id,
                    user_favorite_events.c.event_id == event_id
                )
            )
            await self.session.commit()
            return False
        else:
            # Add to favorites
            await self.session.execute(
                user_favorite_events.insert().values(user_id=user.id, event_id=event_id)
            )
            await self.session.commit()
            return True

    async def get_user_favorites(self, user_id: int) -> list[Event]:
        """Get all favorited events for a user."""
        query = select(Event).join(
            user_favorite_events, Event.id == user_favorite_events.c.event_id
        ).where(user_favorite_events.c.user_id == user_id, Event.is_active == True)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def is_favorited(self, user_id: int, event_id: int) -> bool:
        """Check if an event is favorited by a user."""
        query = select(user_favorite_events).where(
            user_favorite_events.c.user_id == user_id,
            user_favorite_events.c.event_id == event_id
        )
        result = await self.session.execute(query)
        return result.first() is not None

    async def mark_favorites(self, events: list, user_id: int | None) -> None:
        """Mark events in a list as favorited by a user."""
        if not user_id or not events:
            return

        event_ids = [getattr(e, "id", None) for e in events if getattr(e, "id", None)]
        if not event_ids:
            return

        query = select(user_favorite_events.c.event_id).where(
            user_favorite_events.c.user_id == user_id,
            user_favorite_events.c.event_id.in_(event_ids)
        )
        result = await self.session.execute(query)
        favorited_ids = {r[0] for r in result.all()}

        for event in events:
            event_id = getattr(event, "id", None)
            setattr(event, "is_favorited", event_id in favorited_ids)
