"""Service layer for queue operations"""
import asyncio
from typing import Any, Callable
from app.core.config import settings

class QueueService:
    """Service class for handling queue operations"""
    
    def __init__(self):
        self.queue = asyncio.Queue()
    
    async def enqueue(self, item: Any) -> bool:
        """Add item to queue"""
        try:
            await self.queue.put(item)
            return True
        except Exception:
            return False
    
    async def dequeue(self) -> Any:
        """Get item from queue"""
        try:
            return await self.queue.get()
        except Exception:
            return None
    
    async def process_queue(self, handler: Callable):
        """Process items in queue"""
        while True:
            item = await self.dequeue()
            if item:
                await handler(item)
            await asyncio.sleep(0.1)  # Prevent busy waiting