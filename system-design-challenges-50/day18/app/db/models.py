from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import datetime

from .session import Base


class Article(Base):
    """Article model."""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    is_published = Column(Boolean, default=True)
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    # Add any relationships here if needed


class Category(Base):
    """Category model."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserPreference(Base):
    """User preference model for prefetching."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    preferred_categories = Column(Text)  # JSON string of preferred categories
    preferred_authors = Column(Text)     # JSON string of preferred authors
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Create tables
def create_tables():
    """Create all tables defined in models."""
    Base.metadata.create_all(bind=engine)