import asyncio
import time
from typing import Callable, Any
from app.core.logging_config import get_logger

logger = get_logger("retry_handler")

class RetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with exponential backoff retry logic
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                # If this was the last attempt, re-raise the exception
                if attempt == self.max_retries:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
                    raise e
                    
                # Calculate delay with exponential backoff
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                
    def execute_with_retry_sync(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a synchronous function with exponential backoff retry logic
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                # If this was the last attempt, re-raise the exception
                if attempt == self.max_retries:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
                    raise e
                    
                # Calculate delay with exponential backoff
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)