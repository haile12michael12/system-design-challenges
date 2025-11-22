import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/cost_optimizer")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Telemetry
    PROMETHEUS_URL: str = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
    GRAFANA_URL: str = os.getenv("GRAFANA_URL", "http://localhost:3000")
    
    # Billing
    BILLING_API_URL: str = os.getenv("BILLING_API_URL", "http://billing-service:8000")
    BILLING_API_KEY: str = os.getenv("BILLING_API_KEY", "secret-key")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cost-optimizer-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    class Config:
        case_sensitive = True


settings = Settings()