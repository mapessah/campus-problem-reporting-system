from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Campus Maintenance API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()  # pyright: ignore[reportCallIssue]

