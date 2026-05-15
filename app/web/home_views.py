from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.db.session import get_db
from app.models.user import User
from app.services.event_service import EventService
from app.services.recommendation_service import RecommendationService
from app.services.favorite_service import FavoriteService
from app.web.deps import get_current_user_from_cookie

router = APIRouter(tags=["Web - Home"])


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(
        access_token=request.cookies.get("access_token"), session=session
    )
    event_service = EventService(session)

    # Featured events (newest 6)
    featured_result = await event_service.get_events_paginated(page=1, size=6)
    featured_events = featured_result.items

    # Personalized recommendations (if logged in)
    recommended_events = []
    if current_user:
        rec_service = RecommendationService(session)
        rec_result = await rec_service.get_recommendations(current_user.id, top_k=6)
        recommended_events = rec_result.recommendations
        
        # Mark favorites
        fav_service = FavoriteService(session)
        await fav_service.mark_favorites(featured_events, current_user.id)
        await fav_service.mark_favorites(recommended_events, current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="home/index.html",
        context={
            "current_user": current_user,
            "featured_events": featured_events,
            "recommended_events": recommended_events,
        },
    )
