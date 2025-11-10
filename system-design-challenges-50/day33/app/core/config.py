"""
Application Configuration
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Geo-Distributed Key-Value Store"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REGION_ID: str = os.getenv("REGION_ID", "us-east-1")

settings = Settings()