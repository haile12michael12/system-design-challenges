# Celery configuration
from .app.core.config import settings

broker_url = settings.REDIS_URL
result_backend = settings.REDIS_URL

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Worker settings
worker_prefetch_multiplier = 1
task_acks_late = True