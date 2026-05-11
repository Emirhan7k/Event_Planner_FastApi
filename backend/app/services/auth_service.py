from app.core.security import create_access_token


class AuthService:
    def issue_token(self, email: str) -> str:
        return create_access_token(email)


auth_service = AuthService()
