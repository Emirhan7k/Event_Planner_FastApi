from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas.recommendation import Recommendation
from app.services.recommendation_service import recommendation_service

router = APIRouter()


@router.get("", response_model=list[Recommendation])
def recommendations(user_id: int = Depends(get_current_user_id), mood: str = "focused") -> list[Recommendation]:
    return recommendation_service.for_user(user_id=user_id, mood=mood)
