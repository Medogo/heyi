from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    # database
    DATABASE_URL: str = "sqlite:///./heyi_mvt.db"
    SQLALCHEMY_TRACK_MODIFICATIONS: ClassVar[bool] = False  # ClassVar car non destinée à être extraite/env_file
    SQLALCHEMY_ENGINE_OPTIONS: dict = {"pool_pre_ping": True}  # Peut rester ainsi car c'est un type dict

    # application
    SECRET_KEY: str = "secret"
    DEBUG: bool = False
    TESTING: bool = False   

    # linkedin settings configuration
    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    LINKEDIN_REDIRECT_URI: str
    LINKEDIN_ACCESS_TOKEN: str
    LINKEDIN_REFRESH_TOKEN: str

    class Config:
        env_file = ".env"

# Créer une instance de Settings
settings = Settings()
