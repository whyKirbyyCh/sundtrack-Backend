from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    app_name: Optional[str] = None
    app_version: Optional[str] = None

if __name__ == "__main__":
    settings = Settings()
