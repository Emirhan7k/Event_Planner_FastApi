from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.recommendation import RecommendationResult, SimilarEvent
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/me", response_model=RecommendationResult)
async def get_my_recommendations(
    top_k: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """Get personalized AI-powered event recommendations for the current user."""
    service = RecommendationService(session)
    return await service.get_recommendations(current_user.id, top_k=top_k)


@router.get("/similar/{event_id}", response_model=list[SimilarEvent])
async def get_similar_events(
    event_id: int,
    top_k: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_db),
):
    """Get events similar to the given event (content-based)."""
    service = RecommendationService(session)
    return await service.get_similar_events(event_id, top_k=top_k)


@router.get("/score/{event_id}")
async def get_event_score(
    event_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    """Get recommendation score (0–100) for a specific event for the current user."""
    service = RecommendationService(session)
    score = await service.score_event_for_user(current_user.id, event_id)
    return {"event_id": event_id, "user_id": current_user.id, "score": score, "score_percent": round(score * 100)}
