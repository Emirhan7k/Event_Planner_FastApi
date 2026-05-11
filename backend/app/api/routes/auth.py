from fastapi import APIRouter

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    return TokenResponse(access_token=create_access_token(payload.email), user_name="Ali Yilmaz")


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest) -> TokenResponse:
    return TokenResponse(access_token=create_access_token(payload.email), user_name=payload.name)
