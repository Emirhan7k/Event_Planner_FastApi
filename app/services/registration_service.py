from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, CapacityError, ConflictError, NotFoundError
from app.models.registration import Registration, RegistrationStatus
from app.models.user import User
from app.repositories.event_repo import EventRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.registration import RegistrationWithEvent


class RegistrationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = EventRepository(session)
        self.reg_repo = RegistrationRepository(session)

    async def register_to_event(self, event_id: int, current_user: User) -> Registration:
        event = await self.event_repo.get_active(event_id)
        if not event:
            raise NotFoundError("Event")

        existing = await self.reg_repo.get_by_user_and_event(current_user.id, event_id)
        if existing:
            if existing.status == RegistrationStatus.CONFIRMED:
                raise ConflictError("You are already registered for this event.")
            # Re-activate cancelled registration
            existing.status = RegistrationStatus.CONFIRMED
            self.session.add(existing)
            await self.session.commit()
            return existing

        if event.is_full:
            raise CapacityError()

        reg = await self.reg_repo.create({
            "user_id": current_user.id,
            "event_id": event_id,
            "status": RegistrationStatus.CONFIRMED,
        })
        await self.session.commit()
        return reg

    async def cancel_registration(self, event_id: int, current_user: User) -> None:
        reg = await self.reg_repo.get_by_user_and_event(current_user.id, event_id)
        if not reg or reg.status == RegistrationStatus.CANCELLED:
            raise NotFoundError("Registration")
        reg.status = RegistrationStatus.CANCELLED
        self.session.add(reg)
        await self.session.commit()

    async def is_registered(self, user_id: int, event_id: int) -> bool:
        return await self.reg_repo.is_registered(user_id, event_id)

    async def mark_registration_status(self, events: list, user_id: int | None) -> None:
        if not user_id or not events:
            return

        registered_ids = set(await self.reg_repo.get_user_confirmed_event_ids(user_id))
        for event in events:
            event_id = getattr(event, "id", None)
            setattr(event, "is_registered", event_id in registered_ids)

    async def get_my_registrations(self, current_user: User) -> list[RegistrationWithEvent]:
        regs = await self.reg_repo.get_user_registrations(
            current_user.id, status=RegistrationStatus.CONFIRMED
        )
        result = []
        for reg in regs:
            event = await self.event_repo.get(reg.event_id)
            result.append(RegistrationWithEvent(
                id=reg.id,
                user_id=reg.user_id,
                event_id=reg.event_id,
                status=reg.status,
                registered_at=reg.registered_at,
                event_title=event.title if event else None,
                event_date=event.event_date if event else None,
                event_location=event.location if event else None,
                event_category=event.category if event else None,
                event_image_url=event.image_url if event else None,
            ))
        return result
