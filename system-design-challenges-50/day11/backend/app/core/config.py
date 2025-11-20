import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "Auto-Scaler Visualizer"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/autoscaler")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery settings
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    
    # API settings
    API_V1_STR: str = "/api/v1"

settings = Settings()