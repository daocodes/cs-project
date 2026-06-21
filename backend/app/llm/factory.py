from app.core.settings import settings
from app.llm.anthropic_provider import AnthropicProvider
from app.llm.bedrock_provider import BedrockProvider
from app.llm.provider import LLMProvider


def get_llm_provider() -> LLMProvider:
    if settings.bedrock_enabled:
        return BedrockProvider(
            region=settings.aws_region, model_id=settings.bedrock_model_id
        )

    if not settings.anthropic_api_key:
        raise RuntimeError(
            "BEDROCK_ENABLED=false requires ANTHROPIC_API_KEY for the dev fallback"
        )
    return AnthropicProvider(
        api_key=settings.anthropic_api_key, model=settings.anthropic_model
    )
