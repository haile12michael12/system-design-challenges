"""
Items Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.db.models import Item
from app.db.session import AsyncSessionLocal

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(ItemCreate):
    id: int

@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Create a new item"""
    # Implementation will be added later
    return ItemResponse(id=1, **item.dict())

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Get an item by ID"""
    # Implementation will be added later
    return ItemResponse(id=item_id, name="Sample Item", price=10.0)

@router.get("/", response_model=List[ItemResponse])
async def list_items(skip: int = 0, limit: int = 100):
    """List items with pagination"""
    # Implementation will be added later
    return [
        ItemResponse(id=1, name="Sample Item 1", price=10.0),
        ItemResponse(id=2, name="Sample Item 2", price=20.0)
    ]

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate):
    """Update an item"""
    # Implementation will be added later
    return ItemResponse(id=item_id, **item.dict())

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    # Implementation will be added later
    return {"message": f"Item {item_id} deleted successfully"}