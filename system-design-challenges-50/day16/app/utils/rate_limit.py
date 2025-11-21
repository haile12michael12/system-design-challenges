import time
from collections import defaultdict
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_size: int = 60):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if a client is allowed to make a request."""
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_size
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.max_requests:
            return False
            
        # Add current request
        self.requests[client_id].append(now)
        return True

    def get_remaining_requests(self, client_id: str) -> int:
        """Get the number of remaining requests for a client."""
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_size
        ]
        
        return max(0, self.max_requests - len(self.requests[client_id]))