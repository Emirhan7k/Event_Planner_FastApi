from fastapi import APIRouter

from app.schemas.preference import PreferenceUpdate, UserPreferences

router = APIRouter()


@router.get("", response_model=UserPreferences)
def get_preferences() -> UserPreferences:
    return UserPreferences(interests={"Teknoloji": 0.9, "Sanat": 0.3, "Girişimcilik": 0.6}, keywords=["veri", "AI", "startup"])


@router.put("", response_model=UserPreferences)
def update_preferences(payload: PreferenceUpdate) -> UserPreferences:
    return UserPreferences(interests=payload.interests, keywords=payload.keywords)
