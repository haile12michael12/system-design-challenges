from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/datalake"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_pool_size: int = 10
    
    # Data Lake Storage
    storage_bucket: str = "datalake-storage"
    storage_region: str = "us-east-1"
    storage_endpoint: Optional[str] = None  # For S3-compatible storage
    
    # Ingestion
    default_batch_size: int = 10000
    max_concurrent_jobs: int = 5
    job_timeout_seconds: int = 3600
    
    # Schema Evolution
    enable_schema_evolution: bool = True
    auto_apply_schema_changes: bool = False
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    log_level: str = "INFO"
    
    # API
    api_title: str = "Data Lake Ingestion Framework"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
