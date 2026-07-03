from app.auth.types import CurrentUser


class CognitoAuthVerifier:
    def __init__(self, region: str, user_pool_id: str, client_id: str):
        self.region = region
        self.user_pool_id = user_pool_id
        self.client_id = client_id

    def resolve_user(self, authorization: str | None) -> CurrentUser | None:
        # 1) validate "Bearer <token>"
        # 2) decode + verify JWT (issuer/audience/signature/exp)
        # 3) extract claims: sub, email
        # 4) return CurrentUser(...)
        if not authorization:
            return None
        return CurrentUser(id=123, email="user@example.com", auth_id="cognito-sub")
