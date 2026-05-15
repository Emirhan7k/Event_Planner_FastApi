from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, optional_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.event import (
    EventCreate,
    EventDetailRead,
    EventListResponse,
    EventRead,
    EventUpdate,
)
from app.services.event_service import EventService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=EventListResponse)
async def list_events(
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=50),
    category: str | None = Query(None),
    search: str | None = Query(None),
    upcoming_only: bool = Query(True),
    session: AsyncSession = Depends(get_db),
):
    service = EventService(session)
    return await service.get_events_paginated(
        page=page, size=size, category=category,
        search=search, upcoming_only=upcoming_only
    )


@router.post("", response_model=EventRead, status_code=201)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = EventService(session)
    event = await service.create_event(data, current_user)
    return EventRead.model_validate(event)


@router.get("/{event_id}", response_model=EventDetailRead)
async def get_event(
    event_id: int,
    current_user: User | None = Depends(optional_current_user),
    session: AsyncSession = Depends(get_db),
):
    event_service = EventService(session)
    event = await event_service.get_event(event_id)

    is_registered = False
    recommendation_score = None

    if current_user:
        from app.repositories.registration_repo import RegistrationRepository
        reg_repo = RegistrationRepository(session)
        is_registered = await reg_repo.is_registered(current_user.id, event_id)

        rec_service = RecommendationService(session)
        recommendation_score = await rec_service.score_event_for_user(current_user.id, event_id)

    return EventDetailRead(
        **EventRead.model_validate(event).model_dump(),
        owner_username=event.owner.username if event.owner else None,
        is_registered=is_registered,
        recommendation_score=recommendation_score,
    )


@router.put("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int,
    data: EventUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = EventService(session)
    event = await service.update_event(event_id, data, current_user)
    return EventRead.model_validate(event)


@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = EventService(session)
    await service.delete_event(event_id, current_user)


@router.post("/{event_id}/image", response_model=EventRead)
async def upload_event_image(
    event_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = EventService(session)
    event = await service.upload_event_image(event_id, file, current_user)
    return EventRead.model_validate(event)
