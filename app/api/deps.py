from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthError, ForbiddenError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    if not token:
        raise AuthError("Not authenticated.")
    user_id = decode_access_token(token)
    if not user_id:
        raise AuthError("Invalid or expired token.")
    repo = UserRepository(session)
    user = await repo.get(int(user_id))
    if not user or not user.is_active:
        raise AuthError("User not found or inactive.")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise ForbiddenError("Inactive account.")
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Admin access required.")
    return current_user


async def optional_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User | None:
    """Returns user if authenticated, None otherwise. No error raised."""
    if not token:
        return None
    user_id = decode_access_token(token)
    if not user_id:
        return None
    repo = UserRepository(session)
    user = await repo.get(int(user_id))
    return user if user and user.is_active else None
