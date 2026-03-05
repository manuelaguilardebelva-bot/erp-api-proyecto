from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    DATABASE_URL: str
    SECRET_KEY: str = "cambia-esta-clave-secreta-en-produccion"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
