"""ORM models for requirement versions"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Version(Base):
    __tablename__ = "versions"
    
    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(50), default="medium")
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())