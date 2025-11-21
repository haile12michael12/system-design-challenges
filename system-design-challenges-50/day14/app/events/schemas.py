from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreatedEvent(BaseModel):
    order_id: int
    user_id: int
    total_amount: float
    items: list
    timestamp: datetime = datetime.now()

class PaymentProcessedEvent(BaseModel):
    payment_id: int
    order_id: int
    amount: float
    status: str
    timestamp: datetime = datetime.now()

class InventoryUpdatedEvent(BaseModel):
    product_id: int
    old_quantity: int
    new_quantity: int
    timestamp: datetime = datetime.now()

class UserRegisteredEvent(BaseModel):
    user_id: int
    username: str
    email: str
    timestamp: datetime = datetime.now()