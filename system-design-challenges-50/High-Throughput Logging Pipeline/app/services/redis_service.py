import redis
import json
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger("redis_service")

class RedisService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.queue_name = settings.REDIS_QUEUE_NAME
        
    def push_log(self, log_data: Dict[str, Any]) -> bool:
        """
        Push a single log entry to Redis queue
        """
        try:
            log_json = json.dumps(log_data)
            self.redis_client.lpush(self.queue_name, log_json)
            logger.info(f"Pushed log to queue: {log_data.get('id', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to push log to queue: {str(e)}")
            return False
            
    def push_logs_batch(self, logs_data: List[Dict[str, Any]]) -> bool:
        """
        Push a batch of log entries to Redis queue
        """
        try:
            pipe = self.redis_client.pipeline()
            for log_data in logs_data:
                log_json = json.dumps(log_data)
                pipe.lpush(self.queue_name, log_json)
            pipe.execute()
            logger.info(f"Pushed batch of {len(logs_data)} logs to queue")
            return True
        except Exception as e:
            logger.error(f"Failed to push batch of logs to queue: {str(e)}")
            return False
            
    def pop_log(self) -> Dict[str, Any] | None:
        """
        Pop a single log entry from Redis queue
        """
        try:
            log_json = self.redis_client.rpop(self.queue_name)
            if log_json:
                log_data = json.loads(log_json)
                logger.info(f"Popped log from queue: {log_data.get('id', 'unknown')}")
                return log_data
            return None
        except Exception as e:
            logger.error(f"Failed to pop log from queue: {str(e)}")
            return None
            
    def get_queue_length(self) -> int:
        """
        Get the current length of the Redis queue
        """
        try:
            length = self.redis_client.llen(self.queue_name)
            return length
        except Exception as e:
            logger.error(f"Failed to get queue length: {str(e)}")
            return 0