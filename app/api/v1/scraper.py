from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.services.scraper_service import ScraperService

router = APIRouter(prefix="/scraper", tags=["Scraper"])

@router.post("/run")
async def run_scraper(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can run the scraper.")
    
    service = ScraperService(session)
    tech_count = await service.scrape_tech_events()
    culture_count = await service.scrape_culture_events()
    total = tech_count + culture_count
    return {"message": f"Scraping completed. {total} new events added (Tech: {tech_count}, Culture: {culture_count})."}
