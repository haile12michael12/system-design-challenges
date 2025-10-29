from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class JobStatus(PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class DataSourceType(PyEnum):
    S3 = "s3"
    KAFKA = "kafka"
    DATABASE = "database"
    API = "api"
    FILE = "file"

class IngestionJob(Base):
    """Represents a data ingestion job"""
    __tablename__ = "ingestion_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String(255), nullable=False, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("data_lake_tables.id"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    priority = Column(Integer, default=5)  # 1-10, higher is more important
    
    # Configuration
    batch_size = Column(Integer, default=10000)
    max_retries = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=60)
    
    # Scheduling
    schedule_cron = Column(String(100))  # Cron expression for scheduled jobs
    is_scheduled = Column(Boolean, default=False)
    
    # Execution tracking
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_run_at = Column(DateTime)
    next_run_at = Column(DateTime)
    
    # Results
    records_processed = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    data_source = relationship("DataSource", back_populates="jobs")
    batches = relationship("IngestionBatch", back_populates="job")

class IngestionBatch(Base):
    """Represents a batch within an ingestion job"""
    __tablename__ = "ingestion_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("ingestion_jobs.id"), nullable=False)
    batch_number = Column(Integer, nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    
    # Data tracking
    source_file_path = Column(String(1000))
    source_offset = Column(Integer)  # For streaming sources
    record_count = Column(Integer, default=0)
    size_bytes = Column(Integer, default=0)
    
    # Processing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    processing_time_seconds = Column(Integer)
    
    # Results
    records_processed = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text)
    
    # Storage
    output_partition_path = Column(String(500))
    output_files = Column(JSON)  # List of output file paths
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("IngestionJob", back_populates="batches")

class DataSource(Base):
    """Represents a data source configuration"""
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    source_type = Column(Enum(DataSourceType), nullable=False)
    
    # Connection configuration
    connection_config = Column(JSON, nullable=False)  # Source-specific config
    
    # Authentication
    auth_type = Column(String(50))  # none, basic, oauth, api_key
    auth_config = Column(JSON)  # Authentication details
    
    # Data configuration
    data_format = Column(String(20), default="json")  # json, csv, avro, parquet
    schema_definition = Column(JSON)  # Expected schema
    
    # Monitoring
    is_active = Column(Boolean, default=True)
    last_accessed = Column(DateTime)
    last_error = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    jobs = relationship("IngestionJob", back_populates="data_source")
