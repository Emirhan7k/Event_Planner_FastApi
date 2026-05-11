class PreferenceRepository:
    def for_user(self, user_id: int) -> dict[str, float]:
        return {"Teknoloji": 0.9, "Veri Bilimi": 0.85, "Sanat": 0.3, "Girişimcilik": 0.6}


preference_repository = PreferenceRepository()
