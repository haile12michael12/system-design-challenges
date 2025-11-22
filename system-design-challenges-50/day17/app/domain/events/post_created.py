from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class PostCreatedEvent(BaseModel):
    """Event triggered when a post is created."""
    event_id: str = str(uuid.uuid4())
    event_type: str = "post_created"
    post_id: str
    user_id: str
    content: str
    timestamp: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "event_id": "550e8400-e29b-41d4-a716-446655440000",
                "event_type": "post_created",
                "post_id": "550e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440002",
                "content": "This is a sample post content",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }