from typing import List
from app.schemas.logs import LogIn
from app.services.redis_service import RedisService
from app.services.db_service import DBService
from app.core.logging_config import get_logger
from app.core.exceptions import LogIngestionError
import json

logger = get_logger("log_ingestion")

class LogIngestionService:
    def __init__(self):
        self.redis_service = RedisService()
        
    def validate_log(self, log_data: LogIn) -> bool:
        """
        Validate a log entry
        """
        try:
            # Check required fields
            if not log_data.message:
                raise LogIngestionError("Log message is required")
                
            if not log_data.service:
                raise LogIngestionError("Service name is required")
                
            # Validate timestamp
            if log_data.timestamp is None:
                raise LogIngestionError("Timestamp is required")
                
            return True
        except Exception as e:
            logger.error(f"Log validation failed: {str(e)}")
            return False
            
    def buffer_log(self, log_data: LogIn) -> bool:
        """
        Buffer a log entry in Redis queue
        """
        try:
            # Convert to dict for JSON serialization
            log_dict = log_data.dict()
            
            # Add to Redis queue
            success = self.redis_service.push_log(log_dict)
            if not success:
                raise LogIngestionError("Failed to buffer log in Redis")
                
            logger.info(f"Buffered log: {log_dict.get('id', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to buffer log: {str(e)}")
            return False
            
    def buffer_logs_batch(self, logs_data: List[LogIn]) -> bool:
        """
        Buffer a batch of log entries in Redis queue
        """
        try:
            # Convert to dicts for JSON serialization
            logs_dicts = [log.dict() for log in logs_data]
            
            # Add to Redis queue
            success = self.redis_service.push_logs_batch(logs_dicts)
            if not success:
                raise LogIngestionError("Failed to buffer logs batch in Redis")
                
            logger.info(f"Buffered batch of {len(logs_dicts)} logs")
            return True
        except Exception as e:
            logger.error(f"Failed to buffer logs batch: {str(e)}")
            return False