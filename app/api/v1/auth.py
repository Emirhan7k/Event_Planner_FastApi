from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: RegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    tokens = await service.register(data)
    # Set HttpOnly cookies for web usage
    response.set_cookie("access_token", tokens.access_token, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True, samesite="lax")
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    tokens = await service.login(data)
    response.set_cookie("access_token", tokens.access_token, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True, samesite="lax")
    return tokens


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    data: RefreshRequest,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    new_access_token = await service.refresh(data.refresh_token)
    response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax")
    return AccessTokenResponse(access_token=new_access_token)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully."}
