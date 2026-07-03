from app.auth.types import CurrentUser


class MockAuthVerifier:
    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = email

    def resolve_user(self, authorization: str | None) -> CurrentUser:
        return CurrentUser(id=self.user_id, email=self.email, auth_id=None)
