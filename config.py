from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = [
    "settings",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        frozen=True
    )

    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: SecretStr
    HOST: str


settings = Settings()
