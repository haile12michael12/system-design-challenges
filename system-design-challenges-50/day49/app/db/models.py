"""
SQLAlchemy Models
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class MetricsRecord(Base):
    __tablename__ = "metrics_records"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    replicas = Column(Integer)
    cost_per_hour = Column(Float)

class ScalingEvent(Base):
    __tablename__ = "scaling_events"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String)  # scale_up, scale_down
    reason = Column(String)  # cpu_threshold, memory_threshold, etc.
    old_replicas = Column(Integer)
    new_replicas = Column(Integer)
    cost_impact = Column(Float)