"""Event web views: list, detail, create."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.core.exceptions import AppError
from app.db.session import get_db
from app.services.event_service import EventService
from app.web.deps import get_current_user_from_cookie, require_login_cookie

router = APIRouter(prefix="/events", tags=["web-events"])


@router.get("", response_class=HTMLResponse)
async def event_list(
    request: Request,
    page: int = 1,
    category: str | None = None,
    search: str | None = None,
    session: AsyncSession = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(
        access_token=request.cookies.get("access_token"), session=session
    )
    service = EventService(session)
    result = await service.get_events_paginated(
        page=page, size=12, category=category, search=search
    )
    return templates.TemplateResponse(
        request=request,
        name="events/list.html",
        context={
            "current_user": current_user,
            "events": result.items,
            "total": result.total,
            "page": page,
            "pages": result.pages,
            "category": category,
            "search": search,
        },
    )


@router.get("/create", response_class=HTMLResponse)
async def event_create_page(
    request: Request,
    current_user=Depends(require_login_cookie),
):
    return templates.TemplateResponse(
        request=request, name="events/create.html", context={"current_user": current_user}
    )


@router.get("/{event_id}", response_class=HTMLResponse)
async def event_detail(
    request: Request,
    event_id: int,
    session: AsyncSession = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(
        access_token=request.cookies.get("access_token"), session=session
    )
    service = EventService(session)
    try:
        event = await service.get_event(event_id)
    except AppError as e:
        return templates.TemplateResponse(
            request=request, name="404.html", context={"current_user": current_user}, status_code=404
        )
    return templates.TemplateResponse(
        request=request,
        name="events/detail.html",
        context={"current_user": current_user, "event": event},
    )
