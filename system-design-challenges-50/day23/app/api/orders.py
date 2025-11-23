from fastapi import APIRouter, HTTPException, status
from app.schemas.order_schemas import OrderCreate, OrderResponse
from app.services.publisher import publish_order_event
from app.db.session import get_db
from app.db.models import Order
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order and publish event to queue"""
    # In a real implementation, we would:
    # 1. Save order to database
    # 2. Publish order created event to RabbitMQ
    # 3. Return order details
    
    # For now, we'll simulate the process
    order_id = 1  # This would come from the database
    order_data = {
        "id": order_id,
        "customer_id": order.customer_id,
        "items": order.items,
        "total_amount": sum(item.price * item.quantity for item in order.items),
        "status": "pending"
    }
    
    # Publish event to queue
    await publish_order_event("order_created", order_data)
    
    return OrderResponse(**order_data)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """Get order by ID"""
    # In a real implementation, we would fetch from database
    # For now, we'll return a mock order
    order_data = {
        "id": order_id,
        "customer_id": 1,
        "items": [],
        "total_amount": 100.0,
        "status": "completed"
    }
    
    return OrderResponse(**order_data)

@router.get("/", response_model=List[OrderResponse])
async def list_orders():
    """List all orders"""
    # In a real implementation, we would fetch from database
    # For now, we'll return mock orders
    orders = [
        {
            "id": 1,
            "customer_id": 1,
            "items": [],
            "total_amount": 100.0,
            "status": "completed"
        },
        {
            "id": 2,
            "customer_id": 2,
            "items": [],
            "total_amount": 150.0,
            "status": "pending"
        }
    ]
    
    return [OrderResponse(**order) for order in orders]