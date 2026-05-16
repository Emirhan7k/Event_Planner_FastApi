"""
AI Recommendation Engine — Content-Based Filtering
===================================================
Algorithm:
  1. Build a USER PROFILE TEXT from:
       - User's interest tags (from profile)
       - Tags + category of events the user previously attended
  2. Build an EVENT CORPUS — one text document per active event:
       - event.title + event.category + event.tags + event.description (first 200 chars)
  3. Apply TF-IDF vectorization on the corpus (including the user profile).
  4. Compute cosine similarity between the user vector and each event vector.
  5. Return top-K events sorted by score descending, excluding already-registered events.

For "similar events": treat the target event text as the "user" vector.
"""

import logging
from dataclasses import dataclass, field

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.user import User
from app.repositories.event_repo import EventRepository
from app.repositories.registration_repo import RegistrationRepository
from app.repositories.user_repo import UserRepository
from app.schemas.recommendation import RecommendationResult, RecommendedEvent, SimilarEvent

logger = logging.getLogger(__name__)


@dataclass
class RecommendationEngine:
    """
    Stateless recommendation engine — built fresh per request using live DB data.
    No mock data. All text sourced from real user profiles and events.
    """

    session: AsyncSession
    event_repo: EventRepository = field(init=False)
    user_repo: UserRepository = field(init=False)
    reg_repo: RegistrationRepository = field(init=False)

    def __post_init__(self):
        self.event_repo = EventRepository(self.session)
        self.user_repo = UserRepository(self.session)
        self.reg_repo = RegistrationRepository(self.session)

    # ──────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────

    def _event_to_text(self, event: Event) -> str:
        """Convert an event to a single TF-IDF document string."""
        tags_text = " ".join(event.tags) if event.tags else ""
        desc_snippet = (event.description or "")[:500]
        return f"{event.title} {event.category} {tags_text} {desc_snippet}".lower().strip()

    def _build_user_profile_text(self, user: User, reference_events: list[Event]) -> str:
        """Build the user's interest text for TF-IDF based on interests, bio, and interactions."""
        parts: list[str] = []
        
        # 1. Explicit Interests (High weight)
        if user.interests:
            parts.extend([i.lower() for i in user.interests] * 4)
            
        # 2. User Bio (Medium weight)
        if user.bio:
            parts.append(user.bio.lower())
            
        # 3. Interacted Events (Registered + Favorited)
        for event in reference_events:
            tags_text = " ".join(event.tags) if event.tags else ""
            # Category and tags are very important for similarity
            parts.append(f"{event.category} {tags_text} {event.title}")
            
        return " ".join(parts).lower().strip()

    def _calculate_hybrid_score(
        self, 
        event: Event, 
        content_score: float, 
        user_interests: list[str], 
        attended_categories: dict[str, int]
    ) -> tuple[float, str]:
        """
        Calculate a hybrid score (0.0 - 1.0+) and a reason.
        Components:
        1. Content Similarity (TF-IDF): 40%
        2. Interest Match (Explicit): 30%
        3. Category Preference: 20%
        4. Popularity: 10%
        """
        score = content_score * 0.4
        reason = "Matched your interests"

        # 1. Interest Match
        matching_interests = []
        event_tags = [t.lower() for t in (event.tags or [])]
        for interest in user_interests:
            if interest.lower() in event_tags or interest.lower() in event.title.lower():
                matching_interests.append(interest)
        
        if matching_interests:
            score += 0.3 * (len(matching_interests) / max(len(user_interests), 1))
            reason = f"Based on your interest in {matching_interests[0]}"

        # 2. Category Match
        if event.category in attended_categories:
            score += 0.2
            if not matching_interests:
                reason = f"Fits your preference for {event.category} events"

        # 3. Popularity / Filling Up
        if event.capacity > 0:
            fill_ratio = event.registered_count / event.capacity
            if fill_ratio > 0.8:
                score += 0.1
                reason = f"Trending now: {reason}" if reason else "Trending in your area"
            elif fill_ratio > 0.5:
                score += 0.05

        return min(float(score), 1.0), reason

    def _run_tfidf(self, query_text: str, event_texts: list[str]) -> np.ndarray:
        if not query_text or not event_texts:
            return np.zeros(len(event_texts))
        corpus = [query_text] + event_texts
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=5000, sublinear_tf=True)
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            user_vector = tfidf_matrix[0]
            event_matrix = tfidf_matrix[1:]
            return cosine_similarity(user_vector, event_matrix).flatten()
        except Exception:
            return np.zeros(len(event_texts))

    # ──────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────

    async def get_recommendations(self, user_id: int, top_k: int = 10) -> RecommendationResult:
        user = await self.user_repo.get(user_id)
        if not user:
            return RecommendationResult(user_id=user_id, recommendations=[], based_on_interests=[], total_events_analyzed=0)

        # 1. Gather User Interactions
        registered_ids = set(await self.reg_repo.get_user_confirmed_event_ids(user_id))
        favorite_ids = {e.id for e in user.favorites} if user.favorites else set()
        interacted_ids = registered_ids.union(favorite_ids)
        
        all_events = await self.event_repo.get_all_active_for_recommendation()
        
        # 2. Filter Candidates (Only show events the user hasn't registered for or favorited)
        candidate_events = [e for e in all_events if e.id not in interacted_ids]
        
        if not candidate_events:
            return RecommendationResult(user_id=user_id, recommendations=[], based_on_interests=user.interests or [], total_events_analyzed=0)

        # 3. Reference Events for Scoring
        # Combine attended and favorited events as "reference" for what the user likes
        reference_events = [e for e in all_events if e.id in interacted_ids]
        
        attended_categories = {}
        for e in reference_events:
            attended_categories[e.category] = attended_categories.get(e.category, 0) + 1

        # 4. Content Scoring
        profile_text = self._build_user_profile_text(user, reference_events)
        event_texts = [self._event_to_text(e) for e in candidate_events]
        content_scores = self._run_tfidf(profile_text, event_texts)

        # 5. Hybrid Scoring
        hybrid_results = []
        for event, c_score in zip(candidate_events, content_scores):
            score, reason = self._calculate_hybrid_score(event, float(c_score), user.interests or [], attended_categories)
            hybrid_results.append((event, score, reason))

        hybrid_results.sort(key=lambda x: x[1], reverse=True)
        scored = hybrid_results[:top_k]

        recommendations = [
            RecommendedEvent(
                id=event.id,
                title=event.title,
                description=event.description,
                location=event.location,
                event_date=event.event_date,
                category=event.category,
                tags=event.tags or [],
                image_url=event.image_url,
                source_url=event.source_url,
                capacity=event.capacity,
                registered_count=event.registered_count,
                is_full=event.is_full,
                score=round(score, 4),
                score_percent=round(score * 100),
                recommendation_reason=reason
            )
            for event, score, reason in scored
        ]

        return RecommendationResult(
            user_id=user_id,
            recommendations=recommendations,
            based_on_interests=user.interests or [],
            total_events_analyzed=len(candidate_events),
        )

    async def get_similar_events(self, event_id: int, top_k: int = 5) -> list[SimilarEvent]:
        all_events = await self.event_repo.get_all_active_for_recommendation()
        target_event = next((e for e in all_events if e.id == event_id), None)
        if not target_event: return []

        other_events = [e for e in all_events if e.id != event_id]
        if not other_events: return []

        target_text = self._event_to_text(target_event)
        event_texts = [self._event_to_text(e) for e in other_events]
        scores = self._run_tfidf(target_text, event_texts)

        scored = sorted(zip(other_events, scores), key=lambda x: x[1], reverse=True)[:top_k]

        return [
            SimilarEvent(
                id=event.id, title=event.title, category=event.category,
                tags=event.tags or [], image_url=event.image_url,
                source_url=event.source_url, event_date=event.event_date,
                score=round(float(score), 4), score_percent=round(float(score) * 100),
            )
            for event, score in scored
        ]

    async def score_event_for_user(self, user_id: int, event_id: int) -> float:
        user = await self.user_repo.get(user_id)
        if not user: return 0.0
        event = await self.event_repo.get_active(event_id)
        if not event: return 0.0
        
        registered_ids = set(await self.reg_repo.get_user_confirmed_event_ids(user_id))
        favorite_ids = {e.id for e in user.favorites} if user.favorites else set()
        interacted_ids = registered_ids.union(favorite_ids)
        
        all_events = await self.event_repo.get_all_active_for_recommendation()
        reference_events = [e for e in all_events if e.id in interacted_ids]
        attended_categories = {e.category: 1 for e in reference_events}

        profile_text = self._build_user_profile_text(user, reference_events)
        event_text = self._event_to_text(event)
        c_scores = self._run_tfidf(profile_text, [event_text])
        
        score, _ = self._calculate_hybrid_score(event, float(c_scores[0]), user.interests or [], attended_categories)
        return round(float(score), 4)


# ─── Factory function (for dependency injection) ───

class RecommendationService:
    """Thin wrapper to instantiate the engine — used in FastAPI Depends."""

    def __init__(self, session: AsyncSession):
        self.engine = RecommendationEngine(session=session)

    async def get_recommendations(self, user_id: int, top_k: int = 10) -> RecommendationResult:
        return await self.engine.get_recommendations(user_id, top_k)

    async def get_similar_events(self, event_id: int, top_k: int = 5) -> list[SimilarEvent]:
        return await self.engine.get_similar_events(event_id, top_k)

    async def score_event_for_user(self, user_id: int, event_id: int) -> float:
        return await self.engine.score_event_for_user(user_id, event_id)

    async def mark_scores(self, events: list[Event], user_id: int) -> None:
        """Batch mark events with their recommendation scores for the UI."""
        if not events or not user_id:
            return
            
        user = await self.user_repo.get(user_id)
        if not user:
            return
            
        registered_ids = set(await self.reg_repo.get_user_confirmed_event_ids(user_id))
        favorite_ids = {e.id for e in user.favorites} if user.favorites else set()
        interacted_ids = registered_ids.union(favorite_ids)
        
        all_active = await self.event_repo.get_all_active_for_recommendation()
        reference_events = [e for e in all_active if e.id in interacted_ids]
        attended_categories = {e.category: 1 for e in reference_events}
        
        profile_text = self.engine._build_user_profile_text(user, reference_events)
        event_texts = [self.engine._event_to_text(e) for e in events]
        
        content_scores = self.engine._run_tfidf(profile_text, event_texts)
        
        for event, c_score in zip(events, content_scores):
            score, reason = self.engine._calculate_hybrid_score(
                event, float(c_score), user.interests or [], attended_categories
            )
            setattr(event, "score_percent", round(float(score) * 100))
            setattr(event, "recommendation_reason", reason)
