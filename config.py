from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.
    Values are loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # =========================
    # Application
    # =========================

    APP_NAME: str = "Multi-Agent AI Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # =========================
    # API
    # =========================

    API_PREFIX: str = "/api"

    # =========================
    # Database
    # =========================

    DATABASE_URL: str = Field(
        default="sqlite:///multi_agent.db"
    )

    # =========================
    # JWT
    # =========================

    SECRET_KEY: str = Field(
        default="CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    )

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =========================
    # Gemini
    # =========================

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    TEMPERATURE: float = 0.7

    MAX_OUTPUT_TOKENS: int = 2048

    # =========================
    # Agent Configuration
    # =========================

    MAX_AGENT_ITERATIONS: int = 5

    ENABLE_LOGS: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings object.
    """
    return Settings()


settings = get_settings()
