from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class ChangeType(PyEnum):
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    RENAME_COLUMN = "rename_column"
    CHANGE_TYPE = "change_type"
    ADD_CONSTRAINT = "add_constraint"
    DROP_CONSTRAINT = "drop_constraint"

class ChangeStatus(PyEnum):
    PENDING = "pending"
    APPLIED = "applied"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class SchemaVersion(Base):
    """Represents a version of a table schema"""
    __tablename__ = "schema_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("data_lake_tables.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    schema_definition = Column(JSON, nullable=False)
    is_current = Column(Boolean, default=False)
    
    # Migration info
    migration_script = Column(Text)  # SQL or code for migration
    migration_duration_seconds = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))
    description = Column(Text)
    
    # Relationships
    table = relationship("DataLakeTable")
    changes = relationship("SchemaChange", back_populates="schema_version")

class SchemaChange(Base):
    """Represents a specific change in schema evolution"""
    __tablename__ = "schema_changes"
    
    id = Column(Integer, primary_key=True, index=True)
    schema_version_id = Column(Integer, ForeignKey("schema_versions.id"), nullable=False)
    change_type = Column(Enum(ChangeType), nullable=False)
    status = Column(Enum(ChangeStatus), default=ChangeStatus.PENDING)
    
    # Change details
    column_name = Column(String(255))
    old_value = Column(JSON)  # Previous column definition
    new_value = Column(JSON)  # New column definition
    change_description = Column(Text)
    
    # Execution tracking
    applied_at = Column(DateTime)
    applied_by = Column(String(100))
    error_message = Column(Text)
    
    # Rollback info
    rollback_script = Column(Text)
    rolled_back_at = Column(DateTime)
    rolled_back_by = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    schema_version = relationship("SchemaVersion", back_populates="changes")
