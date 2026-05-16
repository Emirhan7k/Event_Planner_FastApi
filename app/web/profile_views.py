"""Profile web views."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.core.exceptions import AppError
from app.db.session import get_db
from app.schemas.user import UserUpdate
from app.services.user_service import UserService
from app.services.favorite_service import FavoriteService
from app.web.deps import require_login_cookie

router = APIRouter(prefix="/profile", tags=["web-profile"])


from app.services.registration_service import RegistrationService

@router.get("", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    current_user=Depends(require_login_cookie),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    fav_service = FavoriteService(session)
    reg_service = RegistrationService(session)
    
    stats = await service.get_user_stats(current_user.id)
    saved_events = await fav_service.get_user_favorites(current_user.id)
    registered_events = await reg_service.get_my_registrations(current_user)
    
    # Mark as favorited for template logic
    for event in saved_events:
        setattr(event, "is_favorited", True)

    return templates.TemplateResponse(
        request=request,
        name="profile/index.html",
        context={
            "current_user": current_user, 
            "stats": stats,
            "saved_events": saved_events,
            "registered_events": registered_events
        },
    )


@router.post("/update")
async def profile_update(
    request: Request,
    full_name: str = Form(...),
    bio: str = Form(""),
    interests: str = Form(""),
    current_user=Depends(require_login_cookie),
    session: AsyncSession = Depends(get_db),
):
    try:
        service = UserService(session)
        
        # Process interests string into a list
        interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]
        
        await service.update_profile(
            current_user.id, 
            UserUpdate(
                full_name=full_name, 
                bio=bio or None,
                interests=interest_list
            )
        )
        return RedirectResponse(url="/profile?updated=1", status_code=302)
    except AppError as e:
        stats = await UserService(session).get_user_stats(current_user.id)
        return templates.TemplateResponse(
            request=request,
            name="profile/index.html",
            context={"current_user": current_user, "stats": stats, "error": e.detail},
            status_code=400,
        )
