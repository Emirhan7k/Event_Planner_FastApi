"""
Web dependency: Extract current user from HttpOnly cookie for Jinja2 pages.
No 401 raised — returns None for anonymous users.
"""
from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repo import UserRepository


async def get_current_user_from_cookie(
    access_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_db),
) -> User | None:
    if not access_token:
        return None
    user_id = decode_access_token(access_token)
    if not user_id:
        return None
    repo = UserRepository(session)
    user = await repo.get(int(user_id))
    return user if user and user.is_active else None


async def require_login_cookie(
    user: User | None = Depends(get_current_user_from_cookie),
) -> User:
    """Use in web routes that require authentication — redirects to login if not set."""
    if not user:
        from fastapi import HTTPException
        from fastapi.responses import RedirectResponse
        raise HTTPException(status_code=307, headers={"Location": "/login"})
    return user


async def require_admin(
    user: User = Depends(require_login_cookie),
) -> User:
    if user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
