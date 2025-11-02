"""ORM models for locks"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Lock(Base):
    __tablename__ = "locks"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False, unique=True)
    locked_by = Column(String(255), nullable=False)  # user or service that locked the requirement
    locked_at = Column(DateTime(timezone=True), server_default=func.now())