from typing import Protocol

from app.auth.cognito import CognitoAuthVerifier
from app.auth.mock import MockAuthVerifier
from app.auth.types import CurrentUser
from app.core.settings import settings


class AuthVerifier(Protocol):
    def resolve_user(self, authorization: str | None) -> CurrentUser | None: ...


def get_auth_verifier() -> AuthVerifier:
    if settings.auth_mode == "cognito":
        if (
            not settings.cognito_region
            or not settings.cognito_user_pool_id
            or not settings.cognito_client_id
        ):
            raise ValueError(
                "Cognito auth mode requires cognito_region, "
                "cognito_user_pool_id, and cognito_client_id."
            )
        return CognitoAuthVerifier(
            region=settings.cognito_region,
            user_pool_id=settings.cognito_user_pool_id,
            client_id=settings.cognito_client_id,
        )

    return MockAuthVerifier(
        user_id=settings.mock_user_id,
        email=settings.mock_user_email,
    )
