import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AuthError, BadRequestError, NotFoundError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import PasswordChangeRequest, UserInterestsUpdate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def get_profile(self, user_id: int) -> User:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")
        return user

    async def update_profile(self, user_id: int, data: UserUpdate) -> User:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")
        updates = data.model_dump(exclude_none=True)
        updated_user = await self.user_repo.update(user, updates)
        await self.session.commit()
        return updated_user

    async def change_password(self, user_id: int, data: PasswordChangeRequest) -> None:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")
        if not verify_password(data.current_password, user.hashed_password):
            raise AuthError("Current password is incorrect.")
        await self.user_repo.update(user, {"hashed_password": hash_password(data.new_password)})
        await self.session.commit()

    async def update_interests(self, user_id: int, data: UserInterestsUpdate) -> User:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")
        updated_user = await self.user_repo.update(user, {"interests": data.interests})
        await self.session.commit()
        return updated_user

    async def upload_avatar(self, user_id: int, file: UploadFile) -> User:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")

        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise BadRequestError(f"File too large. Max {settings.MAX_UPLOAD_SIZE_MB}MB.")

        ext = Path(file.filename or "avatar.jpg").suffix.lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            raise BadRequestError("Invalid file type. Use JPG, PNG, WEBP or GIF.")

        upload_dir = Path(settings.UPLOAD_DIR) / "avatars"
        upload_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4()}{ext}"
        file_path = upload_dir / filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Remove old avatar
        if user.avatar_url:
            old_path = Path(user.avatar_url.lstrip("/"))
            if old_path.exists():
                old_path.unlink(missing_ok=True)

        avatar_url = f"/{settings.UPLOAD_DIR}/avatars/{filename}"
        updated_user = await self.user_repo.update(user, {"avatar_url": avatar_url})
        await self.session.commit()
        return updated_user

    async def get_user_stats(self, user_id: int) -> dict:
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundError("User")
        confirmed_regs = [r for r in user.registrations if r.status == "confirmed"]
        return {
            "events_created": len(user.events),
            "events_registered": len(confirmed_regs),
        }
