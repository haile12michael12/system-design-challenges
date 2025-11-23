from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReplicaStatus(Base):
    __tablename__ = "replica_status"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # active, lagging, failed
    lag_seconds = Column(Float, default=0.0)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class History(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False)
    event_type = Column(String(50), nullable=False)  # lag, failover, recovery
    value = Column(Float, nullable=True)  # lag seconds or other metrics
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)