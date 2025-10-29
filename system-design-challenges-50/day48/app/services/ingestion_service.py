from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
import json
import logging

from ..models.ingestion import IngestionJob, IngestionBatch, DataSource, JobStatus
from ..models.data_lake import DataLakeTable
from ..config.settings import settings

logger = logging.getLogger(__name__)

class IngestionService:
    """Service for managing data ingestion jobs"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_job(
        self,
        job_name: str,
        data_source_id: int,
        table_id: int,
        batch_size: int = None,
        priority: int = 5,
        schedule_cron: str = None,
        created_by: str = "system"
    ) -> IngestionJob:
        """Create a new ingestion job"""
        
        job = IngestionJob(
            job_name=job_name,
            data_source_id=data_source_id,
            table_id=table_id,
            batch_size=batch_size or settings.default_batch_size,
            priority=priority,
            schedule_cron=schedule_cron,
            is_scheduled=bool(schedule_cron),
            created_by=created_by
        )
        
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        logger.info(f"Created ingestion job: {job_name} (ID: {job.id})")
        return job
    
    async def get_job(self, job_id: int) -> Optional[IngestionJob]:
        """Get a job by ID"""
        return self.db.query(IngestionJob).filter(IngestionJob.id == job_id).first()
    
    async def list_jobs(
        self,
        status: JobStatus = None,
        table_id: int = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[IngestionJob]:
        """List jobs with optional filtering"""
        
        query = self.db.query(IngestionJob)
        
        if status:
            query = query.filter(IngestionJob.status == status)
        if table_id:
            query = query.filter(IngestionJob.table_id == table_id)
        
        return query.offset(offset).limit(limit).all()
    
    async def start_job(self, job_id: int) -> bool:
        """Start a job execution"""
        job = await self.get_job(job_id)
        if not job:
            return False
        
        if job.status != JobStatus.PENDING:
            logger.warning(f"Job {job_id} is not in PENDING status")
            return False
        
        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        job.last_run_at = datetime.utcnow()
        
        self.db.commit()
        
        # Start background processing
        asyncio.create_task(self._process_job(job))
        
        logger.info(f"Started job: {job.job_name} (ID: {job.id})")
        return True
    
    async def _process_job(self, job: IngestionJob):
        """Process a job in the background"""
        try:
            # Get data source and table info
            data_source = self.db.query(DataSource).filter(DataSource.id == job.data_source_id).first()
            table = self.db.query(DataLakeTable).filter(DataLakeTable.id == job.table_id).first()
            
            if not data_source or not table:
                raise ValueError("Data source or table not found")
            
            # Create batches based on data source
            batches = await self._create_batches(job, data_source)
            
            # Process each batch
            total_processed = 0
            total_failed = 0
            
            for batch in batches:
                try:
                    result = await self._process_batch(batch, data_source, table)
                    total_processed += result.get("processed", 0)
                    total_failed += result.get("failed", 0)
                except Exception as e:
                    logger.error(f"Batch {batch.id} failed: {str(e)}")
                    batch.status = JobStatus.FAILED
                    batch.error_message = str(e)
                    self.db.commit()
            
            # Update job status
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.records_processed = total_processed
            job.records_failed = total_failed
            
        except Exception as e:
            logger.error(f"Job {job.id} failed: {str(e)}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
        
        finally:
            self.db.commit()
    
    async def _create_batches(self, job: IngestionJob, data_source: DataSource) -> List[IngestionBatch]:
        """Create batches for a job based on data source"""
        batches = []
        
        # This is a simplified implementation
        # In reality, you'd query the data source to determine batch boundaries
        
        batch = IngestionBatch(
            job_id=job.id,
            batch_number=1,
            source_file_path=f"s3://{settings.storage_bucket}/input/{job.job_name}/data.json",
            record_count=job.batch_size
        )
        
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)
        
        batches.append(batch)
        return batches
    
    async def _process_batch(
        self,
        batch: IngestionBatch,
        data_source: DataSource,
        table: DataLakeTable
    ) -> Dict[str, int]:
        """Process a single batch"""
        
        batch.status = JobStatus.RUNNING
        batch.started_at = datetime.utcnow()
        self.db.commit()
        
        try:
            # Simulate data processing
            # In reality, you'd:
            # 1. Read data from source
            # 2. Apply schema validation
            # 3. Transform data
            # 4. Write to partitioned storage
            
            processed = batch.record_count
            failed = 0
            
            # Update batch status
            batch.status = JobStatus.COMPLETED
            batch.completed_at = datetime.utcnow()
            batch.records_processed = processed
            batch.records_failed = failed
            batch.processing_time_seconds = int(
                (batch.completed_at - batch.started_at).total_seconds()
            )
            
            # Set output location
            batch.output_partition_path = f"year=2024/month=01/day=15"
            batch.output_files = [f"s3://{settings.storage_bucket}/output/{table.name}/year=2024/month=01/day=15/batch_{batch.id}.parquet"]
            
            self.db.commit()
            
            return {"processed": processed, "failed": failed}
            
        except Exception as e:
            batch.status = JobStatus.FAILED
            batch.error_message = str(e)
            self.db.commit()
            raise
    
    async def cancel_job(self, job_id: int) -> bool:
        """Cancel a running job"""
        job = await self.get_job(job_id)
        if not job:
            return False
        
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            return False
        
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        self.db.commit()
        
        logger.info(f"Cancelled job: {job.job_name} (ID: {job.id})")
        return True
