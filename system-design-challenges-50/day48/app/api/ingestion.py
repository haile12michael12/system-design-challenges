from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..config.database import get_database
from ..services.ingestion_service import IngestionService
from ..models.ingestion import JobStatus

router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])

# Pydantic models for API
class JobCreateRequest(BaseModel):
    job_name: str
    data_source_id: int
    table_id: int
    batch_size: Optional[int] = None
    priority: int = 5
    schedule_cron: Optional[str] = None
    created_by: str = "api"

class JobResponse(BaseModel):
    id: int
    job_name: str
    data_source_id: int
    table_id: int
    status: str
    priority: int
    batch_size: int
    is_scheduled: bool
    schedule_cron: Optional[str]
    records_processed: int
    records_failed: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

class BatchResponse(BaseModel):
    id: int
    job_id: int
    batch_number: int
    status: str
    record_count: int
    records_processed: int
    records_failed: int
    processing_time_seconds: Optional[int]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

@router.post("/jobs", response_model=JobResponse)
async def create_job(
    request: JobCreateRequest,
    db: Session = Depends(get_database)
):
    """Create a new ingestion job"""
    service = IngestionService(db)
    
    job = await service.create_job(
        job_name=request.job_name,
        data_source_id=request.data_source_id,
        table_id=request.table_id,
        batch_size=request.batch_size,
        priority=request.priority,
        schedule_cron=request.schedule_cron,
        created_by=request.created_by
    )
    
    return JobResponse(
        id=job.id,
        job_name=job.job_name,
        data_source_id=job.data_source_id,
        table_id=job.table_id,
        status=job.status.value,
        priority=job.priority,
        batch_size=job.batch_size,
        is_scheduled=job.is_scheduled,
        schedule_cron=job.schedule_cron,
        records_processed=job.records_processed,
        records_failed=job.records_failed,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message
    )

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: Session = Depends(get_database)
):
    """Get a job by ID"""
    service = IngestionService(db)
    job = await service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse(
        id=job.id,
        job_name=job.job_name,
        data_source_id=job.data_source_id,
        table_id=job.table_id,
        status=job.status.value,
        priority=job.priority,
        batch_size=job.batch_size,
        is_scheduled=job.is_scheduled,
        schedule_cron=job.schedule_cron,
        records_processed=job.records_processed,
        records_failed=job.records_failed,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        error_message=job.error_message
    )

@router.get("/jobs", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[JobStatus] = None,
    table_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_database)
):
    """List jobs with optional filtering"""
    service = IngestionService(db)
    jobs = await service.list_jobs(status, table_id, limit, offset)
    
    return [
        JobResponse(
            id=job.id,
            job_name=job.job_name,
            data_source_id=job.data_source_id,
            table_id=job.table_id,
            status=job.status.value,
            priority=job.priority,
            batch_size=job.batch_size,
            is_scheduled=job.is_scheduled,
            schedule_cron=job.schedule_cron,
            records_processed=job.records_processed,
            records_failed=job.records_failed,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message
        )
        for job in jobs
    ]

@router.post("/jobs/{job_id}/start")
async def start_job(
    job_id: int,
    db: Session = Depends(get_database)
):
    """Start a job execution"""
    service = IngestionService(db)
    success = await service.start_job(job_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to start job")
    
    return {"message": "Job started successfully"}

@router.post("/jobs/{job_id}/cancel")
async def cancel_job(
    job_id: int,
    db: Session = Depends(get_database)
):
    """Cancel a running job"""
    service = IngestionService(db)
    success = await service.cancel_job(job_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel job")
    
    return {"message": "Job cancelled successfully"}

@router.get("/jobs/{job_id}/batches", response_model=List[BatchResponse])
async def get_job_batches(
    job_id: int,
    db: Session = Depends(get_database)
):
    """Get batches for a job"""
    service = IngestionService(db)
    job = await service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    batches = job.batches
    
    return [
        BatchResponse(
            id=batch.id,
            job_id=batch.job_id,
            batch_number=batch.batch_number,
            status=batch.status.value,
            record_count=batch.record_count,
            records_processed=batch.records_processed,
            records_failed=batch.records_failed,
            processing_time_seconds=batch.processing_time_seconds,
            created_at=batch.created_at,
            started_at=batch.started_at,
            completed_at=batch.completed_at,
            error_message=batch.error_message
        )
        for batch in batches
    ]
