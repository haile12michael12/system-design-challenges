from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    items: List[OrderItemResponse] = []
    total_amount: float
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True