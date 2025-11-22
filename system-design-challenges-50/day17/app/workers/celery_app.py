from celery import Celery
from typing import Optional

from ..core.config import settings
from ..core.logging_config import logger


def create_celery_app() -> Celery:
    """
    Create and configure Celery app.
    
    Returns:
        Celery: Configured Celery app
    """
    app = Celery("feed_service")
    
    # Configure Celery
    app.conf.update(
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_routes={
            "feed_propagation_task": {"queue": "feed"},
            "cache_invalidation_task": {"queue": "cache"},
            "metrics_reporting_task": {"queue": "metrics"},
        },
    )
    
    return app


# Global Celery app instance
celery_app: Optional[Celery] = None


def get_celery_app() -> Celery:
    """
    Get Celery app instance.
    
    Returns:
        Celery: Celery app instance
    """
    global celery_app
    if celery_app is None:
        celery_app = create_celery_app()
        logger.info("Celery app created and configured")
    return celery_app


# Create the app instance
app = get_celery_app()