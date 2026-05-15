import math
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.models.event import Event
from app.models.user import User, UserRole
from app.repositories.event_repo import EventRepository
from app.schemas.event import EventCreate, EventListResponse, EventRead, EventUpdate


class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = EventRepository(session)

    async def create_event(self, data: EventCreate, owner: User) -> Event:
        event = await self.event_repo.create({
            **data.model_dump(),
            "owner_id": owner.id,
        })
        await self.session.commit()
        return event

    async def get_event(self, event_id: int) -> Event:
        event = await self.event_repo.get_active(event_id)
        if not event:
            raise NotFoundError("Event")
        return event

    async def get_events_paginated(
        self,
        *,
        page: int = 1,
        size: int = 12,
        category: str | None = None,
        search: str | None = None,
        upcoming_only: bool = True,
    ) -> EventListResponse:
        skip = (page - 1) * size
        events, total = await self.event_repo.get_paginated(
            skip=skip,
            limit=size,
            category=category,
            search=search,
            upcoming_only=upcoming_only,
        )
        pages = math.ceil(total / size) if total > 0 else 1
        return EventListResponse(
            items=[EventRead.model_validate(e) for e in events],
            total=total,
            page=page,
            size=size,
            pages=pages,
        )

    async def update_event(self, event_id: int, data: EventUpdate, current_user: User) -> Event:
        event = await self.event_repo.get_active(event_id)
        if not event:
            raise NotFoundError("Event")
        if event.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise ForbiddenError("You can only edit your own events.")
        updates = data.model_dump(exclude_none=True)
        updated_event = await self.event_repo.update(event, updates)
        await self.session.commit()
        return updated_event

    async def delete_event(self, event_id: int, current_user: User) -> None:
        event = await self.event_repo.get_active(event_id)
        if not event:
            raise NotFoundError("Event")
        if event.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise ForbiddenError("You can only delete your own events.")
        # Soft delete
        await self.event_repo.update(event, {"is_active": False})

    async def upload_event_image(self, event_id: int, file: UploadFile, current_user: User) -> Event:
        event = await self.event_repo.get_active(event_id)
        if not event:
            raise NotFoundError("Event")
        if event.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise ForbiddenError()

        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise BadRequestError(f"File too large. Max {settings.MAX_UPLOAD_SIZE_MB}MB.")

        ext = Path(file.filename or "image.jpg").suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp"):
            raise BadRequestError("Invalid file type.")

        upload_dir = Path(settings.UPLOAD_DIR) / "events"
        upload_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4()}{ext}"
        file_path = upload_dir / filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        image_url = f"/{settings.UPLOAD_DIR}/events/{filename}"
        return await self.event_repo.update(event, {"image_url": image_url})
