from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.registration import RegistrationRead, RegistrationWithEvent
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.post("/{event_id}", response_model=RegistrationRead, status_code=201)
async def register_to_event(
    event_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = RegistrationService(session)
    reg = await service.register_to_event(event_id, current_user)
    return RegistrationRead.model_validate(reg)


@router.delete("/{event_id}", status_code=204)
async def cancel_registration(
    event_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = RegistrationService(session)
    await service.cancel_registration(event_id, current_user)


@router.get("/my", response_model=list[RegistrationWithEvent])
async def my_registrations(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = RegistrationService(session)
    return await service.get_my_registrations(current_user)
