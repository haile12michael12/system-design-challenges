from celery import Celery
from app.config import settings

celery_app = Celery(
    "feed_engine",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.tasks.feed_tasks.*": {"queue": "feed"},
        "app.workers.tasks.email_tasks.*": {"queue": "email"},
        "app.workers.tasks.rollup_tasks.*": {"queue": "rollup"},
    },
)

# Auto-discover tasks
celery_app.autodiscover_tasks([
    "app.workers.tasks.feed_tasks",
    "app.workers.tasks.email_tasks",
    "app.workers.tasks.rollup_tasks",
])