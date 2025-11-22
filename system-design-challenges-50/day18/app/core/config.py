import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/news_db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Cache
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", 300))  # 5 minutes default
    
    # Prefetch
    PREFETCH_LIMIT: int = int(os.getenv("PREFETCH_LIMIT", 10))
    
    class Config:
        case_sensitive = True


settings = Settings()