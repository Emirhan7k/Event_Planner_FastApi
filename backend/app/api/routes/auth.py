from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = user_repository.get_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-posta veya şifre hatalı")

    access_token = create_access_token(user.email)
    return TokenResponse(access_token=access_token, user_name=user.name)


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    if user_repository.get_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu e-posta ile zaten kayıtlı kullanıcı var")

    password_hash = hash_password(payload.password)
    user = user_repository.create_user(db, payload.name, payload.email, password_hash)
    access_token = create_access_token(user.email)
    return TokenResponse(access_token=access_token, user_name=user.name)
