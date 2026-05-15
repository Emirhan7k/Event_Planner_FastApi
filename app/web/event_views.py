"""Event web views: list, detail, create."""

from datetime import datetime
import logging
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.event import EventCreate

from app.core.templates import templates

from app.core.exceptions import AppError
from app.db.session import get_db
from app.services.event_service import EventService
from app.services.comment_service import CommentService
from app.services.favorite_service import FavoriteService
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
    category_lower = category.lower() if category else None
    result = await service.get_events_paginated(
        page=page, size=12, category=category_lower, search=search
    )
    events = result.items
    
    if current_user:
        fav_service = FavoriteService(session)
        await fav_service.mark_favorites(events, current_user.id)
    return templates.TemplateResponse(
        request=request,
        name="events/list.html",
        context={
            "current_user": current_user,
            "events": events,
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
    comment_service = CommentService(session)
    comments = await comment_service.get_event_comments(event_id)
    
    if current_user:
        fav_service = FavoriteService(session)
        is_fav = await fav_service.is_favorited(current_user.id, event_id)
        setattr(event, "is_favorited", is_fav)

    return templates.TemplateResponse(
        request=request,
        name="events/detail.html",
        context={"current_user": current_user, "event": event, "comments": comments},
    )


logger = logging.getLogger(__name__)

@router.post("/create")
async def create_event_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    event_date: str = Form(...),
    capacity: int = Form(...),
    category: str = Form(...),
    tags: str = Form(""),
    image_url: str | None = Form(None),
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_login_cookie),
):
    try:
        service = EventService(session)
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        # Handle different datetime formats from HTML input
        dt = None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                dt = datetime.strptime(event_date, fmt)
                break
            except ValueError:
                continue
        
        if dt is None:
            try:
                dt = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError(f"Invalid date format: {event_date}. Expected YYYY-MM-DDTHH:MM")


        await service.create_event(
            EventCreate(
                title=title,
                description=description,
                location=location,
                event_date=dt,
                capacity=capacity,
                category=category,
                tags=tag_list,
                image_url=image_url if image_url and image_url.strip() else None,
            ),
            current_user,
        )
        return RedirectResponse(url="/events", status_code=303)
    except Exception as e:
        logger.error(f"Event creation error: {str(e)}")
        return templates.TemplateResponse(
            request=request,
            name="events/create.html",
            context={"current_user": current_user, "error": f"Error: {str(e)}"},
            status_code=400,
        )


@router.post("/{event_id}/comments")
async def add_comment_submit(
    request: Request,
    event_id: int,
    content: str = Form(...),
    rating: int = Form(5),
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_login_cookie),
):
    comment_service = CommentService(session)
    await comment_service.add_comment(
        user=current_user,
        event_id=event_id,
        content=content,
        rating=rating
    )
    
    # Return the comments list partial (HTMX)
    comments = await comment_service.get_event_comments(event_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/comment_list.html",
        context={"comments": comments}
    )
