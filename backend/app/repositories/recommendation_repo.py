class RecommendationRepository:
    def log(self, user_id: int, event_id: int, score: int, reason: str) -> dict:
        return {"user_id": user_id, "event_id": event_id, "score": score, "reason": reason}


recommendation_repository = RecommendationRepository()
