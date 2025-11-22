import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data/primary")
    REPLICA1_PATH: str = os.getenv("REPLICA1_PATH", "./data/replica1")
    REPLICA2_PATH: str = os.getenv("REPLICA2_PATH", "./data/replica2")
    
    # WAL
    WAL_PATH: str = os.getenv("WAL_PATH", "./wal")
    WAL_SEGMENT_SIZE: int = int(os.getenv("WAL_SEGMENT_SIZE", 1024 * 1024))  # 1MB default
    
    class Config:
        case_sensitive = True


settings = Settings()