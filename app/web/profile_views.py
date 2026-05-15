"""Profile web views."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.core.exceptions import AppError
from app.db.session import get_db
from app.schemas.user import UserUpdate
from app.services.user_service import UserService
from app.web.deps import require_login_cookie

router = APIRouter(prefix="/profile", tags=["web-profile"])


@router.get("", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    current_user=Depends(require_login_cookie),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)
    stats = await service.get_user_stats(current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="profile/index.html",
        context={"current_user": current_user, "stats": stats},
    )


@router.post("/update")
async def profile_update(
    request: Request,
    full_name: str = Form(...),
    bio: str = Form(""),
    current_user=Depends(require_login_cookie),
    session: AsyncSession = Depends(get_db),
):
    try:
        service = UserService(session)
        await service.update_profile(
            current_user.id, UserUpdate(full_name=full_name, bio=bio or None)
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
