from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

Base = declarative_base()

class DataLakeTable(Base):
    """Represents a table in the data lake"""
    __tablename__ = "data_lake_tables"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    schema_version = Column(Integer, default=1)
    partition_strategy = Column(String(50), default="date")  # date, hash, range
    partition_columns = Column(JSON)  # List of column names for partitioning
    storage_format = Column(String(20), default="parquet")  # parquet, avro, json
    compression = Column(String(20), default="snappy")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    partitions = relationship("DataLakePartition", back_populates="table")
    schemas = relationship("DataLakeSchema", back_populates="table")

class DataLakePartition(Base):
    """Represents a partition within a data lake table"""
    __tablename__ = "data_lake_partitions"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("data_lake_tables.id"), nullable=False)
    partition_path = Column(String(500), nullable=False)  # e.g., year=2024/month=01/day=15
    partition_values = Column(JSON)  # Key-value pairs for partition columns
    record_count = Column(Integer, default=0)
    size_bytes = Column(Integer, default=0)
    file_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    table = relationship("DataLakeTable", back_populates="partitions")

class DataLakeSchema(Base):
    """Represents the schema definition for a data lake table"""
    __tablename__ = "data_lake_schemas"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("data_lake_tables.id"), nullable=False)
    version = Column(Integer, nullable=False)
    schema_definition = Column(JSON, nullable=False)  # Avro/JSON schema
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    table = relationship("DataLakeTable", back_populates="schemas")
