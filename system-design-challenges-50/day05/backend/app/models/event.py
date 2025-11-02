"""ORM models for events"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    event_type = Column(String(100), nullable=False)  # created, updated, deleted, versioned
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())