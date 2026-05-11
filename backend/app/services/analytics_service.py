class AnalyticsService:
    def metrics(self) -> dict[str, int | float]:
        return {"users": 128, "events": 42, "avg_match_score": 86.4, "rsvps": 391}


analytics_service = AnalyticsService()
