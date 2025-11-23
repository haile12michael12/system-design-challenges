from sqlalchemy import Column, String, Text, Integer, DateTime, Index
from app.models.base import BaseModel
from datetime import datetime

class FeedCache(BaseModel):
    __tablename__ = "feed_cache"
    
    user_id = Column(Integer, index=True, nullable=False)
    feed_data = Column(Text, nullable=False)  # JSON serialized feed items
    cache_key = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_feed_cache_user_id', 'user_id'),
        Index('idx_feed_cache_expires_at', 'expires_at'),
    )