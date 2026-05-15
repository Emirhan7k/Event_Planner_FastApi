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

logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.event_repo = EventRepository(session)
        self.user_repo = UserRepository(session)

    async def scrape_tech_events(self) -> int:
        """
        Scrapes events from a sample tech event site or blog.
        For demonstration, we use a reliable news site or a mock source.
        """
        # We will use a demo-friendly target or a mock response if the site is down.
        # Here we simulate scraping from a common event listing pattern.
        url = "https://news.ycombinator.com/show" # Just an example stable site to "scrape" titles from as events
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".athing")[:10] # Get top 10 show HN items
            
            # We need an admin user to own these events
            admin = await self.user_repo.get_by_email("admin@example.com")
            if not admin:
                users, _ = await self.user_repo.get_paginated(limit=1)
                if not users:
                    logger.error("No users found in DB. Cannot own scraped events.")
                    return 0
                admin = users[0]

            count = 0
            for item in items:
                title_elem = item.select_one(".titleline > a")
                if not title_elem:
                    continue
                
                title = title_elem.get_text()
                link = title_elem.get("href")
                
                # Check if event already exists
                existing = await self.event_repo.get_paginated(search=title, limit=1)
                if existing[0]:
                    continue
                
                # Create a pseudo-event
                new_event = EventCreate(
                    title=title,
                    description=f"Automated event discovered from YCombinator Show: {link}",
                    location="Online / Tech Hub",
                    event_date=datetime.now() + timedelta(days=7),
                    capacity=100,
                    category="tech",
                    tags=["tech", "startup", "showcase"],
                    source_url=link
                )
                
                # Save to DB
                # Note: We use the actual service or repo to create
                from app.services.event_service import EventService
                event_service = EventService(self.session)
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            raise Exception(f"Failed to scrape: {str(e)}")

    async def scrape_culture_events(self) -> int:
        """
        Scrapes culture and art events from a sample site.
        """
        url = "https://www.timeout.com/istanbul/en/things-to-do"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # In a real scenario, we might need headers to avoid blocks
                headers = {"User-Agent": "Mozilla/5.0"}
                response = await client.get(url, headers=headers)
                
            soup = BeautifulSoup(response.text, "html.parser")
            # This is a hypothetical selector based on common patterns
            items = soup.select("article")[:10] 
            
            admin = await self.user_repo.get_by_email("admin@example.com")
            if not admin:
                users, _ = await self.user_repo.get_paginated(limit=1)
                if not users:
                    return 0
                admin = users[0]

            count = 0
            for item in items:
                title_elem = item.select_one("h3")
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()
                link_elem = item.select_one("a")
                link = ""
                if link_elem:
                    link = link_elem.get("href")
                    if link and not link.startswith("http"):
                        link = "https://www.timeout.com" + link
                
                # Check if event already exists
                existing = await self.event_repo.get_paginated(search=title, limit=1)
                if existing[0]:
                    continue
                
                new_event = EventCreate(
                    title=title,
                    description=f"Cultural event discovered via TimeOut: {title}. More info at source.",
                    location="Istanbul / Cultural Center",
                    event_date=datetime.now() + timedelta(days=14),
                    capacity=200,
                    category="art",
                    tags=["culture", "art", "istanbul", "featured"],
                    source_url=link
                )
                
                from app.services.event_service import EventService
                event_service = EventService(self.session)
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Culture scraping failed: {str(e)}")
            return 0

    async def scrape_generic_events(self, url: str) -> list[dict[str, Any]]:
        """
        A more generic scraper that tries to find event-like structures.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            
        soup = BeautifulSoup(response.text, "html.parser")
        # Logic to find event cards would go here based on the specific site
        return []
