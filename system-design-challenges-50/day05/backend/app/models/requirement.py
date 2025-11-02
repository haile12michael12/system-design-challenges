"""ORM models for requirements"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(50), default="medium")
    status = Column(String(50), default="draft")
    project_id = Column(Integer, ForeignKey("projects.id"))
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())