from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Index
from app.models.base import BaseModel
from datetime import datetime

class MetadataRollup(BaseModel):
    __tablename__ = "metadata_rollup"
    
    entity_type = Column(String(50), nullable=False)  # 'user', 'post', 'feed', etc.
    entity_id = Column(Integer, nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(BigInteger, nullable=False)
    rollup_period = Column(String(20), nullable=False)  # 'hourly', 'daily', 'weekly'
    timestamp = Column(DateTime, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_metadata_rollup_entity', 'entity_type', 'entity_id'),
        Index('idx_metadata_rollup_metric', 'metric_name'),
        Index('idx_metadata_rollup_timestamp', 'timestamp'),
    )