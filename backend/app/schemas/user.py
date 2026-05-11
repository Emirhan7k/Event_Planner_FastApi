from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    id: int
    name: str
    email: EmailStr
    interests: list[str]
