"""
Celery Configuration
"""
from app.core.config import settings

# Worker configuration
class WorkerConfig:
    def __init__(self):
        self.broker_url = settings.REDIS_URL
        self.result_backend = settings.REDIS_URL
        self.task_serializer = 'json'
        self.accept_content = ['json']
        self.result_serializer = 'json'
        self.timezone = 'UTC'
        self.enable_utc = True

# Global worker config
worker_config = WorkerConfig()