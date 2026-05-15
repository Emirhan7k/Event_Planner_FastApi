from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthError, ConflictError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, data: RegisterRequest) -> TokenResponse:
        if await self.user_repo.email_exists(data.email):
            raise ConflictError("Email already registered.")
        if await self.user_repo.username_exists(data.username):
            raise ConflictError("Username already taken.")

        user = await self.user_repo.create({
            "email": data.email.lower(),
            "username": data.username.lower(),
            "hashed_password": hash_password(data.password),
            "full_name": data.full_name,
            "interests": [i.strip().lower() for i in data.interests],
        })
        await self.session.commit()

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthError("Invalid email or password.")
        if not user.is_active:
            raise AuthError("Account is deactivated.")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str) -> str:
        user_id = decode_refresh_token(refresh_token)
        if not user_id:
            raise AuthError("Invalid or expired refresh token.")
        user = await self.user_repo.get(int(user_id))
        if not user or not user.is_active:
            raise AuthError("User not found or inactive.")
        return create_access_token(subject=str(user.id))
