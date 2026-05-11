from pydantic import BaseModel


class UserPreferences(BaseModel):
    interests: dict[str, float]
    keywords: list[str]


class PreferenceUpdate(UserPreferences):
    pass
