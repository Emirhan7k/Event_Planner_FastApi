"""Dashboard web views."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.db.session import get_db
from app.services.event_service import EventService
from app.services.favorite_service import FavoriteService
from app.services.recommendation_service import RecommendationService
from app.services.registration_service import RegistrationService
from app.web.deps import require_login_cookie

router = APIRouter(prefix="/dashboard", tags=["web-dashboard"])


@router.get("", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user=Depends(require_login_cookie),
    session: AsyncSession = Depends(get_db),
):
    rec_service = RecommendationService(session)
    reg_service = RegistrationService(session)
    event_service = EventService(session)
    fav_service = FavoriteService(session)

    rec_result = await rec_service.get_recommendations(current_user.id, top_k=6)
    recommendations = rec_result.recommendations
    await fav_service.mark_favorites(recommendations, current_user.id)
    await reg_service.mark_registration_status(recommendations, current_user.id)

    # User's registrations
    registrations = await reg_service.get_my_registrations(current_user)

    # Events created by the user
    my_events = await event_service.event_repo.get_by_owner(current_user.id)
    await fav_service.mark_favorites(my_events, current_user.id)
    await reg_service.mark_registration_status(my_events, current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "current_user": current_user,
            "recommendations": recommendations,
            "registrations": registrations,
            "my_events": my_events,
        },
    )
