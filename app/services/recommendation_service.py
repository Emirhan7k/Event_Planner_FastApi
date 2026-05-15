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
        desc_snippet = (event.description or "")[:500] # Use more description
        # Boost title and category by repeating them
        return f"{event.title} {event.title} {event.category} {event.category} {tags_text} {desc_snippet}".lower().strip()

    def _build_user_profile_text(self, user: User, attended_events: list[Event]) -> str:
        """
        Build the user's interest text from:
          - Explicit interest tags (weighted 4x)
          - Bio keywords (weighted 2x)
          - Category + tags of confirmed attended events
        """
        parts: list[str] = []

        # Explicit interests
        if user.interests:
            interest_text = " ".join(user.interests)
            parts.extend([interest_text] * 4)

        # Bio keywords
        if user.bio:
            parts.extend([user.bio] * 2)

        # Implicit interests from past event attendance
        for event in attended_events:
            tags_text = " ".join(event.tags) if event.tags else ""
            # attended events signal category and tags
            parts.append(f"{event.category} {event.category} {tags_text}")

        return " ".join(parts).lower().strip()

    def _run_tfidf(
        self, query_text: str, event_texts: list[str]
    ) -> np.ndarray:
        """
        Run TF-IDF + cosine similarity.
        Returns similarity scores array of shape (len(event_texts),).
        """
        if not query_text or not event_texts:
            return np.zeros(len(event_texts))

        corpus = [query_text] + event_texts
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            max_features=5000,
            sublinear_tf=True,
        )
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
        except ValueError:
            # All terms filtered → zero scores
            return np.zeros(len(event_texts))

        user_vector = tfidf_matrix[0]        # shape (1, n_features)
        event_matrix = tfidf_matrix[1:]       # shape (n_events, n_features)

        scores = cosine_similarity(user_vector, event_matrix).flatten()
        return scores

    # ──────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────

    async def get_recommendations(
        self, user_id: int, top_k: int = 10
    ) -> RecommendationResult:
        """
        Return top-K personalized event recommendations for a user.
        Excludes events the user already registered for.
        """
        user = await self.user_repo.get(user_id)
        if not user:
            return RecommendationResult(
                user_id=user_id,
                recommendations=[],
                based_on_interests=[],
                total_events_analyzed=0,
            )

        # Events the user already joined (exclude from recommendations)
        registered_ids = set(
            await self.reg_repo.get_user_confirmed_event_ids(user_id)
        )

        # All active upcoming events
        all_events = await self.event_repo.get_all_active_for_recommendation()
        candidate_events = [e for e in all_events if e.id not in registered_ids]

        if not candidate_events:
            return RecommendationResult(
                user_id=user_id,
                recommendations=[],
                based_on_interests=user.interests or [],
                total_events_analyzed=0,
            )

        # Build attended-event objects for implicit signal
        attended_events = [e for e in all_events if e.id in registered_ids]

        # Build user profile text
        profile_text = self._build_user_profile_text(user, attended_events)

        logger.debug(
            "Recommendation profile for user %d: %r (interests=%s, attended=%d)",
            user_id, profile_text[:100], user.interests, len(attended_events)
        )

        # Build event corpus
        event_texts = [self._event_to_text(e) for e in candidate_events]

        # Run TF-IDF cosine similarity
        scores = self._run_tfidf(profile_text, event_texts)

        # Pair events with scores and sort
        scored = sorted(
            zip(candidate_events, scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

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
                score=round(float(score), 4),
                score_percent=round(float(score) * 100),
            )
            for event, score in scored
        ]

        return RecommendationResult(
            user_id=user_id,
            recommendations=recommendations,
            based_on_interests=user.interests or [],
            total_events_analyzed=len(candidate_events),
        )

    async def get_similar_events(
        self, event_id: int, top_k: int = 5
    ) -> list[SimilarEvent]:
        """
        Return events similar to the given event (content-based).
        Uses the event's own text as the query vector.
        """
        all_events = await self.event_repo.get_all_active_for_recommendation()
        target_event = next((e for e in all_events if e.id == event_id), None)

        if not target_event:
            return []

        other_events = [e for e in all_events if e.id != event_id]
        if not other_events:
            return []

        target_text = self._event_to_text(target_event)
        event_texts = [self._event_to_text(e) for e in other_events]
        scores = self._run_tfidf(target_text, event_texts)

        scored = sorted(
            zip(other_events, scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        return [
            SimilarEvent(
                id=event.id,
                title=event.title,
                category=event.category,
                tags=event.tags or [],
                image_url=event.image_url,
                source_url=event.source_url,
                event_date=event.event_date,
                score=round(float(score), 4),
                score_percent=round(float(score) * 100),
            )
            for event, score in scored
        ]

    async def score_event_for_user(self, user_id: int, event_id: int) -> float:
        """
        Return the recommendation score (0.0–1.0) for a single event–user pair.
        """
        user = await self.user_repo.get(user_id)
        if not user:
            return 0.0

        event = await self.event_repo.get_active(event_id)
        if not event:
            return 0.0

        registered_ids = set(await self.reg_repo.get_user_confirmed_event_ids(user_id))
        all_events = await self.event_repo.get_all_active_for_recommendation()
        attended_events = [e for e in all_events if e.id in registered_ids]

        profile_text = self._build_user_profile_text(user, attended_events)
        event_text = self._event_to_text(event)
        scores = self._run_tfidf(profile_text, [event_text])
        return round(float(scores[0]), 4)


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
