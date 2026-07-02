from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = (
    Path(__file__).resolve().parents[3]
)  # this is how we get to the root directory


class Settings(BaseSettings):
    database_url: str
    auth_mode: Literal["mock", "cognito"] = "mock"
    mock_user_id: int = 1
    mock_user_email: str = "dev@internbase.local"
    cognito_user_pool_id: str | None = None
    cognito_client_id: str | None = None
    cognito_region: str | None = None

    bedrock_enabled: bool = True
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
