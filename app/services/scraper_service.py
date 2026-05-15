import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.user import User
from app.repositories.event_repo import EventRepository
from app.repositories.user_repo import UserRepository
from app.schemas.event import EventCreate
from app.services.event_service import EventService

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = EventRepository(session)
        self.user_repo = UserRepository(session)

    async def _get_admin(self):
        """Finds an admin or fallback user to own scraped events."""
        admin = await self.user_repo.get_by_email("admin@example.com")
        if not admin:
            users, _ = await self.user_repo.get_paginated(limit=1)
            if not users:
                logger.error("No users found in DB. Cannot own scraped events.")
                return None
            admin = users[0]
        return admin

    async def scrape_tech_events(self) -> int:
        """Scrapes tech events from YCombinator Show HN."""
        url = "https://news.ycombinator.com/show"
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
            
            items = soup.select(".athing")[:10]
            admin = await self._get_admin()
            if not admin:
                return 0

            count = 0
            event_service = EventService(self.session)
            for item in items:
                title_elem = item.select_one(".titleline > a")
                if not title_elem:
                    continue
                
                title = title_elem.get_text()
                link = title_elem.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://news.ycombinator.com/" + link
                
                # Check if event already exists
                existing, _ = await self.event_repo.get_paginated(search=title, limit=1)
                if existing:
                    continue
                
                new_event = EventCreate(
                    title=title,
                    description=f"Automated event from YCombinator Show HN: {link}",
                    location="Online / Tech Hub",
                    event_date=datetime.now() + timedelta(days=7),
                    capacity=100,
                    category="tech",
                    tags=["tech", "startup", "showcase"],
                    source_url=link
                )
                
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Tech scraping failed: {str(e)}")
            raise

    async def scrape_culture_events(self) -> int:
        """Scrapes culture events from TimeOut Istanbul."""
        url = "https://www.timeout.com/istanbul/en/things-to-do"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
            
            items = soup.select("article")[:10]
            admin = await self._get_admin()
            if not admin:
                return 0

            count = 0
            event_service = EventService(self.session)
            for item in items:
                title_elem = item.select_one("h3")
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()
                link_elem = item.select_one("a")
                link = ""
                if link_elem:
                    link = link_elem.get("href", "")
                    if link and not link.startswith("http"):
                        link = "https://www.timeout.com" + link
                
                # Check if event already exists
                existing, _ = await self.event_repo.get_paginated(search=title, limit=1)
                if existing:
                    continue
                
                new_event = EventCreate(
                    title=title,
                    description=f"Cultural event via TimeOut Istanbul: {title}. More info at source: {link}",
                    location="Istanbul / Cultural Center",
                    event_date=datetime.now() + timedelta(days=14),
                    capacity=200,
                    category="art",
                    tags=["culture", "art", "istanbul", "featured"],
                    source_url=link
                )
                
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Culture scraping failed: {str(e)}")
            raise
