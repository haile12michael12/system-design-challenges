from celery import Celery
from app.core.config import settings

# Initialize Celery
celery_app = Celery("cost_optimizer_worker")

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
        "app.workers.tasks.recompute_costs.recompute_service_costs": {"queue": "costs"},
        "app.workers.tasks.pull_metrics.pull_service_metrics": {"queue": "telemetry"},
    }
)

# Auto-discover tasks
celery_app.autodiscover_tasks([
    "app.workers.tasks.recompute_costs",
    "app.workers.tasks.pull_metrics",
])

if __name__ == "__main__":
    celery_app.start()