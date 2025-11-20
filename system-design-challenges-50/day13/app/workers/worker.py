from celery import Celery
from ..config import settings
from ..services.payment_processor import PaymentProcessor
from ..db.database import SessionLocal

celery_app = Celery(
    "payment_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def process_payment_task(payment_id: int):
    """Celery task to process a payment"""
    # Create a new database session
    db = SessionLocal()
    
    try:
        # Process the payment
        payment_processor = PaymentProcessor(db)
        result = payment_processor.process_payment(payment_id)
        return {"payment_id": payment_id, "status": "processed"}
    except Exception as e:
        # Log the error
        print(f"Error processing payment {payment_id}: {e}")
        return {"payment_id": payment_id, "status": "error", "error": str(e)}
    finally:
        # Close the database session
        db.close()