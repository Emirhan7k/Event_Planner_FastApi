"""Auth web views: login, register, logout."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates

from app.core.exceptions import AppError
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService
from app.web.deps import get_current_user_from_cookie

router = APIRouter(prefix="/auth", tags=["web-auth"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth/login.html", context={"user": None})


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db),
):
    try:
        service = AuthService(session)
        tokens = await service.login(LoginRequest(email=email, password=password))
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            max_age=900,
            samesite="lax",
        )
        return response
    except AppError as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"user": None, "error": e.detail},
            status_code=400,
        )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth/register.html", context={"user": None})


@router.post("/register")
async def register_submit(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    interests: str = Form(""),
    session: AsyncSession = Depends(get_db),
):
    try:
        service = AuthService(session)
        # Convert comma separated string to list
        interest_list = [i.strip() for i in interests.split(",") if i.strip()]
        
        tokens = await service.register(
            RegisterRequest(
                email=email, 
                username=username, 
                full_name=full_name, 
                password=password,
                interests=interest_list
            )
        )
        # Auto-login after registration
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(
            key="access_token",
            value=tokens.access_token,
            httponly=True,
            max_age=3600, # 1 hour
            samesite="lax",
        )
        return response
    except (AppError, Exception) as e:
        # Handle both our AppErrors and Pydantic ValidationErrors
        error_msg = str(e)
        if hasattr(e, "detail"):
            error_msg = e.detail
        elif "value_error" in str(e).lower():
            error_msg = "Validation error: Please check your input format (e.g. password length)."
            
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"user": None, "error": error_msg},
            status_code=400,
        )



@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response
