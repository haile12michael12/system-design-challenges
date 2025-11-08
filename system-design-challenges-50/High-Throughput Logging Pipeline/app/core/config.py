import os
from typing import Optional

class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/logging_db")
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    API_KEY: str = os.getenv("API_KEY", "your-api-key-here")
    
    # Application settings
    PROJECT_NAME: str = "High-Throughput Logging Pipeline"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Redis queue settings
    REDIS_QUEUE_NAME: str = os.getenv("REDIS_QUEUE_NAME", "log_queue")
    
    # Database batch settings
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "1000"))
    BATCH_TIMEOUT: int = int(os.getenv("BATCH_TIMEOUT", "5"))  # seconds
    
    # Retention settings
    LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", "30"))

settings = Settings()