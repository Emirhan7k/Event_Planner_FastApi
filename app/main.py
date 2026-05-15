from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppError
from app.db.session import engine
from app.middleware.logging_middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Smart Event Planner with content-based recommendations",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# --------------------------------------------------------------------------- #
# Middleware
# --------------------------------------------------------------------------- #
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------- #
# Static files & templates
# --------------------------------------------------------------------------- #
app.mount("/static", StaticFiles(directory="static"), name="static")



# --------------------------------------------------------------------------- #
# API routes
# --------------------------------------------------------------------------- #
app.include_router(api_router)

# --------------------------------------------------------------------------- #
# Web routes  (import here to avoid circular imports)
# --------------------------------------------------------------------------- #
from app.web import auth_views, dashboard_views, event_views, home_views, profile_views  # noqa: E402

app.include_router(home_views.router)
app.include_router(auth_views.router)
app.include_router(event_views.router)
app.include_router(dashboard_views.router)
app.include_router(profile_views.router)


# --------------------------------------------------------------------------- #
# Global exception handler
# --------------------------------------------------------------------------- #
from fastapi.responses import JSONResponse  # noqa: E402


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
