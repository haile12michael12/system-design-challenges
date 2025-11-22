import logging
import time
from typing import Any, Dict, Optional
from functools import wraps
import traceback

from prometheus_client import Counter, Histogram, Gauge, Summary


# Application metrics
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'app_active_connections',
    'Number of active connections'
)

RECOMMENDATION_GENERATED = Counter(
    'app_recommendations_generated_total',
    'Total number of recommendations generated',
    ['service_id']
)

SIMULATION_RUN = Counter(
    'app_simulations_run_total',
    'Total number of simulations run',
    ['service_id']
)

COST_SAVINGS = Gauge(
    'app_cost_savings_dollars',
    'Estimated cost savings in dollars',
    ['service_id']
)

# Business metrics
RECOMMENDATIONS_APPLIED = Counter(
    'app_recommendations_applied_total',
    'Total number of recommendations applied',
    ['service_id']
)

CONFIG_CHANGES = Counter(
    'app_config_changes_total',
    'Total number of configuration changes',
    ['service_id', 'change_type']
)


class MetricsCollector:
    """Centralized metrics collection"""
    
    def __init__(self):
        self.request_timings = {}
    
    def start_request_timer(self, method: str, endpoint: str):
        """Start timing a request"""
        key = f"{method}:{endpoint}"
        self.request_timings[key] = time.time()
    
    def end_request_timer(self, method: str, endpoint: str, status: int):
        """End timing a request and record metrics"""
        key = f"{method}:{endpoint}"
        if key in self.request_timings:
            duration = time.time() - self.request_timings[key]
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            del self.request_timings[key]
    
    def record_recommendation_generated(self, service_id: str):
        """Record a recommendation generation"""
        RECOMMENDATION_GENERATED.labels(service_id=service_id).inc()
    
    def record_simulation_run(self, service_id: str):
        """Record a simulation run"""
        SIMULATION_RUN.labels(service_id=service_id).inc()
    
    def update_cost_savings(self, service_id: str, savings: float):
        """Update cost savings metric"""
        COST_SAVINGS.labels(service_id=service_id).set(savings)
    
    def record_recommendation_applied(self, service_id: str):
        """Record a recommendation application"""
        RECOMMENDATIONS_APPLIED.labels(service_id=service_id).inc()
    
    def record_config_change(self, service_id: str, change_type: str):
        """Record a configuration change"""
        CONFIG_CHANGES.labels(service_id=service_id, change_type=change_type).inc()


# Global metrics collector instance
metrics_collector = MetricsCollector()


def setup_logging(level: int = logging.INFO) -> None:
    """Set up structured logging"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance"""
    return logging.getLogger(name)


def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = get_logger(func.__module__)
        
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            logger.error(traceback.format_exc())
            raise
    return wrapper


def log_exceptions(func):
    """Decorator to log exceptions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            raise
    return wrapper