from app.repositories.event_repo import event_repository
from app.repositories.preference_repo import preference_repository
from app.schemas.recommendation import Recommendation


class RecommendationService:
    def for_user(self, user_id: int, mood: str) -> list[Recommendation]:
        preferences = preference_repository.for_user(user_id)
        recommendations: list[Recommendation] = []
        for event in event_repository.list():
            preference_boost = int(preferences.get(event.category, 0.4) * 10)
            score = min(99, event.match_score + preference_boost)
            recommendations.append(
                Recommendation(
                    event=event,
                    score=score,
                    reason=f"Gecmisteki katilimlarin ve {event.category} ilgi alanina gore secildi.",
                    tags=[event.category, mood, "AI"],
                )
            )
        return sorted(recommendations, key=lambda item: item.score, reverse=True)


recommendation_service = RecommendationService()
