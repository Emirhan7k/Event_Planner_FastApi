from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(Event, session)

    async def get_active(self, id: int) -> Event | None:
        result = await self.session.execute(
            select(Event)
            .where(Event.id == id, Event.is_active == True)
            .options(selectinload(Event.owner))
        )
        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        *,
        skip: int = 0,
        limit: int = 12,
        category: str | None = None,
        search: str | None = None,
        upcoming_only: bool = True,
    ) -> tuple[list[Event], int]:
        query = select(Event).where(Event.is_active == True)
        count_query = select(func.count()).select_from(Event).where(Event.is_active == True)

        if upcoming_only:
            now = datetime.now(timezone.utc)
            query = query.where(Event.event_date >= now)
            count_query = count_query.where(Event.event_date >= now)

        if category:
            query = query.where(Event.category == category)
            count_query = count_query.where(Event.category == category)

        if search:
            pattern = f"%{search}%"
            search_filter = or_(
                Event.title.ilike(pattern),
                Event.description.ilike(pattern),
                Event.location.ilike(pattern),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        query = query.order_by(Event.event_date.asc()).offset(skip).limit(limit)

        result = await self.session.execute(query)
        count_result = await self.session.execute(count_query)

        return list(result.scalars().all()), count_result.scalar_one()

    async def get_all_active_for_recommendation(self) -> list[Event]:
        """Return all active upcoming events for recommendation engine."""
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(Event)
            .where(Event.is_active == True, Event.event_date >= now)
            .order_by(Event.event_date.asc())
        )
        return list(result.scalars().all())

    async def get_by_owner(self, owner_id: int) -> list[Event]:
        result = await self.session.execute(
            select(Event).where(Event.owner_id == owner_id).order_by(Event.created_at.desc())
        )
        return list(result.scalars().all())
