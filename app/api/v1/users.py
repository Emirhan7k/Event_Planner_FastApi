from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    PasswordChangeRequest,
    UserInterestsUpdate,
    UserRead,
    UserUpdate,
    UserWithStats,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserWithStats)
async def get_me(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    stats = await service.get_user_stats(current_user.id)
    return UserWithStats(
        **UserRead.model_validate(current_user).model_dump(),
        **stats,
    )


@router.put("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    user = await service.update_profile(current_user.id, data)
    return UserRead.model_validate(user)


@router.put("/me/interests", response_model=UserRead)
async def update_interests(
    data: UserInterestsUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    user = await service.update_interests(current_user.id, data)
    return UserRead.model_validate(user)


@router.post("/me/password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    await service.change_password(current_user.id, data)
    return {"message": "Password changed successfully."}


@router.post("/me/avatar", response_model=UserRead)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    user = await service.upload_avatar(current_user.id, file)
    return UserRead.model_validate(user)
