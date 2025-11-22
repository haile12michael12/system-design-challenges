from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EventSchema(BaseModel):
    """Base schema for events."""
    event_id: str
    event_type: str
    timestamp: datetime = datetime.now()
    
    class Config:
        orm_mode = True


class PostCreatedEventSchema(EventSchema):
    """Schema for post created events."""
    post_id: str
    user_id: str
    content: str
    
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


class FollowerAddedEventSchema(EventSchema):
    """Schema for follower added events."""
    follower_id: str
    followed_id: str
    
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