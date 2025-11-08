import asyncio
import json
from typing import List
from app.services.redis_service import RedisService
from app.services.db_service import DBService
from app.services.metrics_service import MetricsService
from app.db.base import get_db
from app.db.models import LogEntry
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging
from app.schemas.logs import LogIn

# Setup logging
setup_logging()

logger = get_logger("redis_worker")

class RedisWorker:
    def __init__(self):
        self.redis_service = RedisService()
        self.db_service = DBService()
        self.batch_size = settings.BATCH_SIZE
        self.batch_timeout = settings.BATCH_TIMEOUT
        
    async def process_logs_batch(self, logs_data: List[dict]) -> bool:
        """
        Process a batch of logs and write them to the database
        """
        try:
            # Convert dicts to LogIn objects
            logs_in = [LogIn(**log_data) for log_data in logs_data]
            
            # Record metrics
            MetricsService.record_batch_size(len(logs_in))
            
            # Write to database
            async for db in get_db():
                db_logs = await self.db_service.create_log_entries_batch(db, logs_in)
                logger.info(f"Processed batch of {len(db_logs)} logs")
                break  # Exit the async generator
                
            return True
        except Exception as e:
            logger.error(f"Failed to process logs batch: {str(e)}")
            return False
            
    async def run(self):
        """
        Main worker loop
        """
        logger.info("Starting Redis worker")
        
        while True:
            try:
                # Get queue length and update metrics
                queue_length = self.redis_service.get_queue_length()
                MetricsService.set_queue_length(queue_length)
                
                # Process logs in batches
                logs_batch = []
                start_time = asyncio.get_event_loop().time()
                
                while len(logs_batch) < self.batch_size:
                    # Check if timeout has been reached
                    elapsed_time = asyncio.get_event_loop().time() - start_time
                    if elapsed_time >= self.batch_timeout and logs_batch:
                        break
                        
                    # Pop a log from Redis queue
                    log_data = self.redis_service.pop_log()
                    if log_data:
                        logs_batch.append(log_data)
                    else:
                        # No more logs in queue, break if we have some logs
                        if logs_batch:
                            break
                        # Otherwise, wait a bit before checking again
                        await asyncio.sleep(0.1)
                        
                # Process the batch if we have logs
                if logs_batch:
                    await self.process_logs_batch(logs_batch)
                    
            except Exception as e:
                logger.error(f"Error in worker loop: {str(e)}")
                await asyncio.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    worker = RedisWorker()
    asyncio.run(worker.run())