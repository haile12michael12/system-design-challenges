from celery import Celery
import os

# Create Celery app
celery_app = Celery(
    "system_design_coach",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.tasks.grading_tasks.evaluate_submission": {"queue": "grading"},
        "app.workers.tasks.notification_tasks.send_feedback_notification": {"queue": "notifications"},
    }
)

if __name__ == "__main__":
    celery_app.start()