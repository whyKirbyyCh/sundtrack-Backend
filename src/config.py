from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

#TODO: refactor this into multiple class
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    app_name: Optional[str] = None
    app_version: Optional[str] = None
    agent_interaction_uri: Optional[str] = None
    api_retries: int = 3
    number_of_pages: int = 1
    database_uri: Optional[str] = None
    main_database: str = "sundtrack"
