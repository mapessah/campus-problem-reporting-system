from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Campus Maintenance API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@cache
def get_settings() -> Settings:
    return Settings() # pyright: ignore[reportCallIssue]


settings = get_settings()  # pyright: ignore[reportCallIssue]

