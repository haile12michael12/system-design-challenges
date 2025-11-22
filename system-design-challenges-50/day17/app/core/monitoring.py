from typing import Callable, Optional
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

from .logging_config import logger


# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)


def metrics_middleware(app: FastAPI) -> None:
    """Add Prometheus metrics middleware to the FastAPI app."""
    
    @app.middleware("http")
    async def add_prometheus_metrics(request: Request, call_next: Callable) -> Response:
        """Middleware to collect Prometheus metrics."""
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Record metrics
        method = request.method
        endpoint = request.url.path
        status = response.status_code
        
        # Update counters
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        
        # Update histogram
        duration = time.time() - start_time
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
        
        return response
    
    @app.get("/metrics")
    async def metrics_endpoint():
        """Endpoint to expose Prometheus metrics."""
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )


# Exception handlers for monitoring
def setup_exception_handlers(app: FastAPI) -> None:
    """Set up exception handlers for better monitoring."""
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        # Re-raise the exception to let FastAPI handle it normally
        raise exc