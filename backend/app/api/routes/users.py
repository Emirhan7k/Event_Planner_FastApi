from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas.user import UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile)
def me(user_id: int = Depends(get_current_user_id)) -> UserProfile:
    return UserProfile(id=user_id, name="Ali Yilmaz", email="ali@example.com", interests=["Teknoloji", "Veri Bilimi", "Girişimcilik"])
