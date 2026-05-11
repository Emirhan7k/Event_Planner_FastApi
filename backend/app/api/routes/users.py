from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.core.database import get_db
from app.repositories.user_repo import user_repository
from app.schemas.user import UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile)
def me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserProfile:
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        interests=["Teknoloji", "Veri Bilimi", "Girişimcilik"],
    )
