from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tracksy"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = Field(default="tracksy-dev-secret-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./tracksy.db")

    # External APIs
    GOOGLE_MAPS_API_KEY: str | None = None
    OPENWEATHER_API_KEY: str | None = None
    TOMTOM_API_KEY: str | None = None
    MAPBOX_TOKEN: str | None = None
    AVIATIONSTACK_API_KEY: str | None = None
    OPENROUTE_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
