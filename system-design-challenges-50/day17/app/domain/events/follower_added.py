from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class FollowerAddedEvent(BaseModel):
    """Event triggered when a user follows another user."""
    event_id: str = str(uuid.uuid4())
    event_type: str = "follower_added"
    follower_id: str
    followed_id: str
    timestamp: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "follower_added",
                "follower_id": "550e8400-e29b-41d4-a716-446655440001",
                "followed_id": "550e8400-e29b-41d4-a716-446655440002",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }