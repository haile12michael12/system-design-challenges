from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date

from ..config.database import get_database
from ..services.partition_service import PartitionService

router = APIRouter(prefix="/api/v1/partitions", tags=["partitions"])

# Pydantic models for API
class PartitionResponse(BaseModel):
    id: int
    table_id: int
    partition_path: str
    partition_values: dict
    record_count: int
    size_bytes: int
    file_count: int
    is_active: bool
    created_at: datetime
    last_updated: datetime

class PartitionStatsUpdate(BaseModel):
    record_count: Optional[int] = None
    size_bytes: Optional[int] = None
    file_count: Optional[int] = None

class PartitionCreateRequest(BaseModel):
    table_id: int
    partition_values: dict
    record_count: int = 0
    size_bytes: int = 0
    file_count: int = 0

@router.post("/", response_model=PartitionResponse)
async def create_partition(
    request: PartitionCreateRequest,
    db: Session = Depends(get_database)
):
    """Create a new partition"""
    service = PartitionService(db)
    
    partition = await service.create_partition(
        table_id=request.table_id,
        partition_values=request.partition_values,
        record_count=request.record_count,
        size_bytes=request.size_bytes,
        file_count=request.file_count
    )
    
    return PartitionResponse(
        id=partition.id,
        table_id=partition.table_id,
        partition_path=partition.partition_path,
        partition_values=partition.partition_values,
        record_count=partition.record_count,
        size_bytes=partition.size_bytes,
        file_count=partition.file_count,
        is_active=partition.is_active,
        created_at=partition.created_at,
        last_updated=partition.last_updated
    )

@router.get("/{partition_id}", response_model=PartitionResponse)
async def get_partition(
    partition_id: int,
    db: Session = Depends(get_database)
):
    """Get a partition by ID"""
    service = PartitionService(db)
    partition = db.query(service.db.query(PartitionService).first().__class__).filter_by(id=partition_id).first()
    
    if not partition:
        raise HTTPException(status_code=404, detail="Partition not found")
    
    return PartitionResponse(
        id=partition.id,
        table_id=partition.table_id,
        partition_path=partition.partition_path,
        partition_values=partition.partition_values,
        record_count=partition.record_count,
        size_bytes=partition.size_bytes,
        file_count=partition.file_count,
        is_active=partition.is_active,
        created_at=partition.created_at,
        last_updated=partition.last_updated
    )

@router.get("/table/{table_id}", response_model=List[PartitionResponse])
async def list_table_partitions(
    table_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_database)
):
    """List partitions for a table"""
    service = PartitionService(db)
    partitions = await service.list_partitions(table_id, limit, offset)
    
    return [
        PartitionResponse(
            id=partition.id,
            table_id=partition.table_id,
            partition_path=partition.partition_path,
            partition_values=partition.partition_values,
            record_count=partition.record_count,
            size_bytes=partition.size_bytes,
            file_count=partition.file_count,
            is_active=partition.is_active,
            created_at=partition.created_at,
            last_updated=partition.last_updated
        )
        for partition in partitions
    ]

@router.put("/{partition_id}/stats")
async def update_partition_stats(
    partition_id: int,
    request: PartitionStatsUpdate,
    db: Session = Depends(get_database)
):
    """Update partition statistics"""
    service = PartitionService(db)
    
    success = await service.update_partition_stats(
        partition_id=partition_id,
        record_count=request.record_count,
        size_bytes=request.size_bytes,
        file_count=request.file_count
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Partition not found")
    
    return {"message": "Partition statistics updated successfully"}

@router.delete("/{partition_id}")
async def delete_partition(
    partition_id: int,
    db: Session = Depends(get_database)
):
    """Delete a partition"""
    service = PartitionService(db)
    
    success = await service.delete_partition(partition_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Partition not found")
    
    return {"message": "Partition deleted successfully"}

@router.get("/table/{table_id}/date-range")
async def get_partitions_by_date_range(
    table_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_database)
):
    """Get partitions within a date range"""
    service = PartitionService(db)
    partitions = await service.get_partition_by_date_range(table_id, start_date, end_date)
    
    return [
        PartitionResponse(
            id=partition.id,
            table_id=partition.table_id,
            partition_path=partition.partition_path,
            partition_values=partition.partition_values,
            record_count=partition.record_count,
            size_bytes=partition.size_bytes,
            file_count=partition.file_count,
            is_active=partition.is_active,
            created_at=partition.created_at,
            last_updated=partition.last_updated
        )
        for partition in partitions
    ]

@router.post("/table/{table_id}/optimize")
async def optimize_partitions(
    table_id: int,
    min_size_mb: int = 128,
    db: Session = Depends(get_database)
):
    """Optimize partitions by merging small ones"""
    service = PartitionService(db)
    optimization_plan = await service.optimize_partitions(table_id, min_size_mb)
    
    return {
        "message": f"Found {len(optimization_plan)} optimization opportunities",
        "optimization_plan": optimization_plan
    }
