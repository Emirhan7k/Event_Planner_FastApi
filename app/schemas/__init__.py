# schemas package
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, AccessTokenResponse
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserPublic, UserWithStats, UserInterestsUpdate, PasswordChangeRequest
from app.schemas.event import EventCreate, EventRead, EventUpdate, EventListResponse, EventDetailRead
from app.schemas.registration import RegistrationRead, RegistrationWithEvent
from app.schemas.recommendation import RecommendedEvent, RecommendationResult, SimilarEvent

__all__ = [
    "RegisterRequest", "LoginRequest", "TokenResponse", "RefreshRequest", "AccessTokenResponse",
    "UserCreate", "UserRead", "UserUpdate", "UserPublic", "UserWithStats", "UserInterestsUpdate", "PasswordChangeRequest",
    "EventCreate", "EventRead", "EventUpdate", "EventListResponse", "EventDetailRead",
    "RegistrationRead", "RegistrationWithEvent",
    "RecommendedEvent", "RecommendationResult", "SimilarEvent",
]
