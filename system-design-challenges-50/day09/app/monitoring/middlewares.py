"""
Monitoring Middlewares
"""
from fastapi import Request
import time
from app.monitoring.metrics import record_request, update_active_connections

class MonitoringMiddleware:
    def __init__(self, app):
        self.app = app
        self.active_connections = 0

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Increment active connections
        self.active_connections += 1
        update_active_connections(self.active_connections)

        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Record request metrics
                duration = time.time() - start_time
                # In a real implementation, you would extract method, endpoint, and status from the scope
                record_request("GET", "/", message["status"], duration)
            
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Decrement active connections
            self.active_connections -= 1
            update_active_connections(self.active_connections)