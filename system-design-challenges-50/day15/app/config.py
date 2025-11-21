import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "Post Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()