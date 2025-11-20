from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    payment_method = Column(String)
    transaction_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentEvent(Base):
    __tablename__ = "payment_events"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, index=True)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(String)  # JSON string for event details