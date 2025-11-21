from celery import Celery
from ..core.config import settings

celery_app = Celery(
    "ecommerce_worker",
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
    """Process a payment"""
    # In a real implementation, this would process the payment
    print(f"Processing payment {payment_id}")
    return {"payment_id": payment_id, "status": "processed"}

@celery_app.task
def send_order_confirmation_task(order_id: int):
    """Send order confirmation"""
    # In a real implementation, this would send an email
    print(f"Sending order confirmation for order {order_id}")
    return {"order_id": order_id, "status": "sent"}

@celery_app.task
def update_inventory_task(product_id: int, quantity: int):
    """Update inventory"""
    # In a real implementation, this would update inventory
    print(f"Updating inventory for product {product_id} by {quantity}")
    return {"product_id": product_id, "quantity": quantity, "status": "updated"}