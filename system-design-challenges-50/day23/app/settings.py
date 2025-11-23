import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/orders_db")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # RabbitMQ
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env"

settings = Settings()