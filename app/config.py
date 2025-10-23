from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file.

    Only include settings that are broadly useful across the app. Service-specific
    options should live near their services with reasonable defaults.
    """

    # General
    environment: str = "dev"

    # Networking / HTTP
    request_timeout_seconds: int = 20
    cache_ttl_seconds: int = 12 * 60 * 60  # 12 hours

    # OpenAI
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
