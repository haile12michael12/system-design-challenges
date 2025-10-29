from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..config.database import get_database
from ..models.data_lake import DataLakeTable

router = APIRouter(prefix="/api/v1/tables", tags=["tables"])

# Pydantic models for API
class TableCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    partition_strategy: str = "date"
    partition_columns: Optional[List[str]] = None
    storage_format: str = "parquet"
    compression: str = "snappy"

class TableResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    schema_version: int
    partition_strategy: str
    partition_columns: Optional[List[str]]
    storage_format: str
    compression: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class TableUpdateRequest(BaseModel):
    description: Optional[str] = None
    partition_strategy: Optional[str] = None
    partition_columns: Optional[List[str]] = None
    storage_format: Optional[str] = None
    compression: Optional[str] = None

@router.post("/", response_model=TableResponse)
async def create_table(
    request: TableCreateRequest,
    db: Session = Depends(get_database)
):
    """Create a new data lake table"""
    
    # Check if table already exists
    existing = db.query(DataLakeTable).filter(DataLakeTable.name == request.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Table with this name already exists")
    
    table = DataLakeTable(
        name=request.name,
        description=request.description,
        partition_strategy=request.partition_strategy,
        partition_columns=request.partition_columns or [],
        storage_format=request.storage_format,
        compression=request.compression
    )
    
    db.add(table)
    db.commit()
    db.refresh(table)
    
    return TableResponse(
        id=table.id,
        name=table.name,
        description=table.description,
        schema_version=table.schema_version,
        partition_strategy=table.partition_strategy,
        partition_columns=table.partition_columns,
        storage_format=table.storage_format,
        compression=table.compression,
        is_active=table.is_active,
        created_at=table.created_at,
        updated_at=table.updated_at
    )

@router.get("/{table_id}", response_model=TableResponse)
async def get_table(
    table_id: int,
    db: Session = Depends(get_database)
):
    """Get a table by ID"""
    table = db.query(DataLakeTable).filter(DataLakeTable.id == table_id).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    return TableResponse(
        id=table.id,
        name=table.name,
        description=table.description,
        schema_version=table.schema_version,
        partition_strategy=table.partition_strategy,
        partition_columns=table.partition_columns,
        storage_format=table.storage_format,
        compression=table.compression,
        is_active=table.is_active,
        created_at=table.created_at,
        updated_at=table.updated_at
    )

@router.get("/", response_model=List[TableResponse])
async def list_tables(
    limit: int = 100,
    offset: int = 0,
    active_only: bool = True,
    db: Session = Depends(get_database)
):
    """List tables"""
    query = db.query(DataLakeTable)
    
    if active_only:
        query = query.filter(DataLakeTable.is_active == True)
    
    tables = query.offset(offset).limit(limit).all()
    
    return [
        TableResponse(
            id=table.id,
            name=table.name,
            description=table.description,
            schema_version=table.schema_version,
            partition_strategy=table.partition_strategy,
            partition_columns=table.partition_columns,
            storage_format=table.storage_format,
            compression=table.compression,
            is_active=table.is_active,
            created_at=table.created_at,
            updated_at=table.updated_at
        )
        for table in tables
    ]

@router.put("/{table_id}", response_model=TableResponse)
async def update_table(
    table_id: int,
    request: TableUpdateRequest,
    db: Session = Depends(get_database)
):
    """Update a table"""
    table = db.query(DataLakeTable).filter(DataLakeTable.id == table_id).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Update fields
    if request.description is not None:
        table.description = request.description
    if request.partition_strategy is not None:
        table.partition_strategy = request.partition_strategy
    if request.partition_columns is not None:
        table.partition_columns = request.partition_columns
    if request.storage_format is not None:
        table.storage_format = request.storage_format
    if request.compression is not None:
        table.compression = request.compression
    
    table.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(table)
    
    return TableResponse(
        id=table.id,
        name=table.name,
        description=table.description,
        schema_version=table.schema_version,
        partition_strategy=table.partition_strategy,
        partition_columns=table.partition_columns,
        storage_format=table.storage_format,
        compression=table.compression,
        is_active=table.is_active,
        created_at=table.created_at,
        updated_at=table.updated_at
    )

@router.delete("/{table_id}")
async def delete_table(
    table_id: int,
    db: Session = Depends(get_database)
):
    """Soft delete a table"""
    table = db.query(DataLakeTable).filter(DataLakeTable.id == table_id).first()
    
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    table.is_active = False
    table.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Table deleted successfully"}
