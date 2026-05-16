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
            # Fallback to any user
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
                    description=f"New tech startup or tool showcase from YCombinator. Learn more about {title} at the source.",
                    location="Online / Global",
                    event_date=datetime.now() + timedelta(days=7),
                    capacity=100,
                    category="tech",
                    tags=["tech", "startup", "innovation", "software"],
                    source_url=link,
                    image_url="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=800"
                )
                
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Tech scraping failed: {str(e)}")
            raise

    def _detect_category(self, title: str, category_label: str) -> str:
        """Detect best matching category from title and site label."""
        text = f"{title} {category_label}".lower()
        
        if any(k in text for k in ["concert", "music", "live", "performance", "show", "whirling", "nightlife", "jazz", "opera"]):
            return "music"
        if any(k in text for k in ["art", "museum", "exhibition", "gallery", "culture", "history", "landmark"]):
            return "art"
        if any(k in text for k in ["food", "taste", "dinner", "culinary", "restaurant", "drink", "wine", "coffee"]):
            return "food"
        if any(k in text for k in ["sport", "match", "game", "race", "run", "stadium", "football", "basketball"]):
            return "sports"
        if any(k in text for k in ["tech", "startup", "innovation", "software", "ai", "coding", "web"]):
            return "tech"
        if any(k in text for k in ["business", "workshop", "masterclass", "learning", "education", "summit", "conference"]):
            return "business"
            
        return "other"

    async def scrape_istanbul_events(self) -> int:
        """Scrapes diverse Istanbul events from istanbul.com/things-to-do."""
        url = "https://istanbul.com/things-to-do"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
            
            items = soup.select("a.item-card")[:30] # Get more items
            admin = await self._get_admin()
            if not admin:
                return 0

            count = 0
            event_service = EventService(self.session)
            for item in items:
                title_elem = item.select_one("h5")
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()
                
                # Check if it's an event or just a tour/pass
                category_label = ""
                cat_elem = item.select_one("p")
                if cat_elem:
                    category_label = cat_elem.get_text().strip()
                
                # Assign category
                category = self._detect_category(title, category_label)
                
                link = item.get("href", "")
                if link and not link.startswith("http"):
                    if link.startswith("//"):
                        link = "https:" + link
                    else:
                        link = "https://istanbul.com" + link
                
                # Check if event already exists
                existing, _ = await self.event_repo.get_paginated(search=title, limit=1)
                if existing:
                    continue
                
                # Image extraction
                image_url = None
                img_elem = item.select_one("img")
                if img_elem:
                    image_url = img_elem.get("src") or img_elem.get("data-src") or img_elem.get("data-lazy-src")
                
                # Randomize date for variety
                event_date = datetime.now() + timedelta(days=5 + count)
                
                # Generate tags based on title/category
                tags = [category, "istanbul", "featured"]
                if "concert" in title.lower(): tags.append("live")
                if "museum" in title.lower(): tags.append("museum")

                new_event = EventCreate(
                    title=title,
                    description=f"Experience the vibrant life of Istanbul with: {title}. This {category} event offers a unique glimpse into the city's rich culture and modern activities.",
                    location="Istanbul, Turkey",
                    event_date=event_date,
                    capacity=150,
                    category=category,
                    tags=tags,
                    source_url=link,
                    image_url=image_url or "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&q=80&w=800"
                )
                
                await event_service.create_event(new_event, admin)
                count += 1
                
            await self.session.commit()
            return count
            
        except Exception as e:
            logger.error(f"Istanbul events scraping failed: {str(e)}")
            raise

    async def scrape_all(self) -> dict[str, int]:
        """Runs all scraping tasks."""
        tech_count = await self.scrape_tech_events()
        istanbul_count = await self.scrape_istanbul_events()
        return {
            "tech": tech_count,
            "istanbul": istanbul_count,
            "total": tech_count + istanbul_count
        }
