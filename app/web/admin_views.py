from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.templates import templates
from app.db.session import get_db
from app.services.scraper_service import ScraperService
from app.web.deps import require_admin

router = APIRouter(prefix="/admin", tags=["web-admin"])

@router.post("/scrape")
async def trigger_scrape(
    request: Request,
    session: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    scraper = ScraperService(session)
    results = await scraper.scrape_all()
    
    # Return a snippet or a message (HTMX friendly)
    return HTMLResponse(
        content=f'<div style="color: var(--success); margin-top: 1rem;">Successfully scraped {results["total"]} new events (Tech: {results["tech"]}, Istanbul: {results["istanbul"]})!</div>'
    )
