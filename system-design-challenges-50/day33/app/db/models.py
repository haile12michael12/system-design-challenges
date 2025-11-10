"""
SQLAlchemy Models
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class KeyValueEntry(Base):
    __tablename__ = "key_value_entries"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String, index=True)
    value = Column(Text)
    region_id = Column(String, index=True)
    ttl = Column(Integer)  # Time to live in seconds
    version = Column(Integer, default=1)
    vector_clock = Column(Text)  # JSON string representation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_key_region', 'key', 'region_id'),
    )

class ReplicationLog(Base):
    __tablename__ = "replication_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String, index=True)
    source_region = Column(String)
    target_region = Column(String)
    status = Column(String)  # pending, completed, failed
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    error_message = Column(Text, nullable=True)