from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderBase(BaseModel):
    user_id: int
    items: List[OrderItem]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    updated_at: datetime

# Mock data storage
orders = []

@router.get("/", response_model=List[Order])
async def list_orders(skip: int = 0, limit: int = 100):
    """List all orders"""
    return orders[skip : skip + limit]

@router.post("/", response_model=Order)
async def create_order(order: OrderCreate):
    """Create a new order"""
    total_amount = sum(item.quantity * item.price for item in order.items)
    new_order = Order(
        id=len(orders) + 1,
        **order.dict(),
        status="pending",
        total_amount=total_amount,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    orders.append(new_order)
    return new_order

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):
    """Get an order by ID"""
    for order in orders:
        if order.id == order_id:
            return order
    return {"error": "Order not found"}

@router.put("/{order_id}/cancel", response_model=Order)
async def cancel_order(order_id: int):
    """Cancel an order"""
    for order in orders:
        if order.id == order_id:
            order.status = "cancelled"
            order.updated_at = datetime.now()
            return order
    return {"error": "Order not found"}