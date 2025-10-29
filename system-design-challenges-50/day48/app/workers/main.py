import asyncio
import logging
from datetime import datetime
from typing import List

from ..config.database import SessionLocal, init_database
from ..services.ingestion_service import IngestionService
from ..models.ingestion import IngestionJob, JobStatus

logger = logging.getLogger(__name__)

class WorkerManager:
    """Manages background workers for data ingestion"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.running = False
    
    async def start(self):
        """Start the worker manager"""
        self.running = True
        logger.info("Worker manager started")
        
        while self.running:
            try:
                await self.process_pending_jobs()
                await asyncio.sleep(10)  # Check every 10 seconds
            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    async def stop(self):
        """Stop the worker manager"""
        self.running = False
        logger.info("Worker manager stopped")
    
    async def process_pending_jobs(self):
        """Process pending ingestion jobs"""
        try:
            # Get pending jobs
            pending_jobs = self.db.query(IngestionJob).filter(
                IngestionJob.status == JobStatus.PENDING
            ).limit(5).all()
            
            if not pending_jobs:
                return
            
            logger.info(f"Found {len(pending_jobs)} pending jobs")
            
            # Process jobs concurrently
            tasks = []
            for job in pending_jobs:
                task = asyncio.create_task(self.process_job(job))
                tasks.append(task)
            
            # Wait for all tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"Error processing pending jobs: {e}")
    
    async def process_job(self, job: IngestionJob):
        """Process a single job"""
        try:
            logger.info(f"Processing job: {job.job_name} (ID: {job.id})")
            
            # Update job status
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            self.db.commit()
            
            # Create ingestion service and process job
            service = IngestionService(self.db)
            await service._process_job(job)
            
            logger.info(f"Completed job: {job.job_name} (ID: {job.id})")
            
        except Exception as e:
            logger.error(f"Failed to process job {job.id}: {e}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            self.db.commit()

async def main():
    """Main worker entry point"""
    # Initialize database
    init_database()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start worker manager
    worker_manager = WorkerManager()
    
    try:
        await worker_manager.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        await worker_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())
