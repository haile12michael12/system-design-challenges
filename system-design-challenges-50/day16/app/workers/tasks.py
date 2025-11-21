from .celery_app import celery_app
from ..services.email_service import EmailService

@celery_app.task
def send_password_reset_email_task(email: str, token: str) -> dict:
    """Send password reset email task."""
    email_service = EmailService()
    email_service.send_password_reset_email(email, token)
    return {"status": "sent", "email": email}

@celery_app.task
def send_verification_email_task(email: str, token: str) -> dict:
    """Send verification email task."""
    email_service = EmailService()
    email_service.send_verification_email(email, token)
    return {"status": "sent", "email": email}

@celery_app.task
def cleanup_expired_tokens_task() -> dict:
    """Cleanup expired tokens task."""
    # Implementation would go here
    return {"status": "completed", "message": "Token cleanup completed"}