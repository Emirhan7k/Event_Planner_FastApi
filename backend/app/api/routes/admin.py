from fastapi import APIRouter

from app.services.analytics_service import analytics_service

router = APIRouter()


@router.get("/metrics")
def metrics() -> dict[str, int | float]:
    return analytics_service.metrics()
