from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.registration import Registration, RegistrationStatus
from app.repositories.base import BaseRepository


class RegistrationRepository(BaseRepository[Registration]):
    def __init__(self, session: AsyncSession):
        super().__init__(Registration, session)

    async def get_by_user_and_event(self, user_id: int, event_id: int) -> Registration | None:
        result = await self.session.execute(
            select(Registration).where(
                Registration.user_id == user_id,
                Registration.event_id == event_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_user_registrations(
        self, user_id: int, status: RegistrationStatus | None = None
    ) -> list[Registration]:
        query = select(Registration).where(Registration.user_id == user_id)
        if status:
            query = query.where(Registration.status == status)
        query = query.order_by(Registration.registered_at.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_event_registration_count(self, event_id: int) -> int:
        result = await self.session.execute(
            select(Registration).where(
                Registration.event_id == event_id,
                Registration.status == RegistrationStatus.CONFIRMED,
            )
        )
        return len(result.scalars().all())

    async def is_registered(self, user_id: int, event_id: int) -> bool:
        reg = await self.get_by_user_and_event(user_id, event_id)
        return reg is not None and reg.status == RegistrationStatus.CONFIRMED

    async def get_user_confirmed_event_ids(self, user_id: int) -> list[int]:
        result = await self.session.execute(
            select(Registration.event_id).where(
                Registration.user_id == user_id,
                Registration.status == RegistrationStatus.CONFIRMED,
            )
        )
        return list(result.scalars().all())
