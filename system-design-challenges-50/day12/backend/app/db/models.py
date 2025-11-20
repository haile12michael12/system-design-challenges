from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SimulationModel(Base):
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(String, unique=True, index=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CAPStateModel(Base):
    __tablename__ = "cap_states"
    
    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(String, index=True)
    timestamp = Column(DateTime)
    consistency = Column(Float)
    availability = Column(Float)
    partition_status = Column(Boolean)
    latency = Column(Float)