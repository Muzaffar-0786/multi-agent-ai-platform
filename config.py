from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application configuration.

    Values are automatically loaded
    from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # ==================================================
    # Application
    # ==================================================

    APP_NAME: str = "Multi-Agent AI Platform"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = False

    API_PREFIX: str = "/api"

    # ==================================================
    # Database
    # ==================================================

    DATABASE_URL: str = "sqlite:///multi_agent.db"

    # ==================================================
    # Authentication
    # ==================================================

    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION"
    )

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==================================================
    # Gemini AI
    # ==================================================

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    TEMPERATURE: float = 0.7

    MAX_OUTPUT_TOKENS: int = 2048

    # ==================================================
    # Agent Settings
    # ==================================================

    MAX_AGENT_STEPS: int = 4

    ENABLE_AGENT_LOGS: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """

    return Settings()


settings = get_settings()
