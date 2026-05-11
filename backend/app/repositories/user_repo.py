class UserRepository:
    def get_by_email(self, email: str) -> dict | None:
        return {"id": 1, "name": "Ali Yilmaz", "email": email}


user_repository = UserRepository()
