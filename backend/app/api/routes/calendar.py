from fastapi import APIRouter

from app.services.calendar_service import calendar_service

router = APIRouter()


@router.get("")
def calendar() -> dict:
    return calendar_service.week_view()
