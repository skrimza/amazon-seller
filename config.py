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

    HOST: str
    ID_OWNER: int
    BOT_TOKEN: SecretStr


settings = Settings()
