from celery import Celery
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery("social_media_worker")

# Configure Celery
celery_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.feed_tasks.*": {"queue": "feed"},
        "app.workers.media_tasks.*": {"queue": "media"},
    }
)

# Auto-discover tasks
celery_app.autodiscover_tasks([
    "app.workers.feed_tasks",
    "app.workers.media_tasks",
])


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup"""
    logger.info(f"Debug task executed: {self.request!r}")
    return "Debug task completed"