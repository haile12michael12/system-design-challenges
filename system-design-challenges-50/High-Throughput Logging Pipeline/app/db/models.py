from sqlalchemy import Column, String, Text, DateTime, Integer, Enum, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from app.schemas.logs import LogLevel
from datetime import datetime
import uuid

class LogEntry(Base):
    __tablename__ = "log_entries"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    level = Column(Enum(LogLevel), index=True)
    message = Column(Text)
    service = Column(String, index=True)
    tenant_id = Column(String, index=True)
    trace_id = Column(String, index=True)
    span_id = Column(String)
    metadata_ = Column(JSONB)  # Renamed from 'metadata' to avoid conflict
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_log_entries_service_timestamp', 'service', 'timestamp'),
        Index('idx_log_entries_tenant_timestamp', 'tenant_id', 'timestamp'),
        Index('idx_log_entries_level_timestamp', 'level', 'timestamp'),
    )

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())