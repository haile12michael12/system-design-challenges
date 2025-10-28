import time
import logging
from typing import Dict, List, Callable, Any
from collections import defaultdict, deque
from typing import DefaultDict
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collects and stores application metrics"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.endpoint_metrics: DefaultDict[str, Dict[str, Any]] = defaultdict(lambda: {
            'count': 0,
            'errors': 0,
            'response_times': deque(maxlen=100)
        })
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, response_time: float, success: bool = True):
        """Record a request"""
        self.request_count += 1
        self.response_times.append(response_time)
        
        # Record endpoint-specific metrics
        self.endpoint_metrics[endpoint]['count'] += 1
        self.endpoint_metrics[endpoint]['response_times'].append(response_time)
        
        if not success:
            self.error_count += 1
            self.endpoint_metrics[endpoint]['errors'] += 1
    
    def get_request_rate(self, window_seconds: int = 60) -> float:
        """Get requests per second over the specified window"""
        # This is a simplified implementation
        # In a real system, you'd track timestamps of requests
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            return self.request_count / elapsed_time
        return 0.0
    
    def get_error_rate(self) -> float:
        """Get error rate as a percentage"""
        if self.request_count > 0:
            return (self.error_count / self.request_count) * 100
        return 0.0
    
    def get_average_response_time(self) -> float:
        """Get average response time in seconds"""
        if self.response_times:
            return sum(self.response_times) / len(self.response_times)
        return 0.0
    
    def get_uptime(self) -> str:
        """Get uptime as a formatted string"""
        uptime_seconds = time.time() - self.start_time
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        return f"{days}d {hours}h {minutes}m {seconds}s"
    
    def get_metrics_summary(self) -> Dict:
        """Get a summary of all metrics"""
        return {
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.get_error_rate(),
            'average_response_time': self.get_average_response_time(),
            'request_rate': self.get_request_rate(),
            'uptime': self.get_uptime(),
            'endpoint_metrics': dict(self.endpoint_metrics)
        }

class HealthChecker:
    """Performs health checks on various system components"""
    
    def __init__(self):
        self.checks = []
    
    def add_check(self, name: str, check_func: Callable[[], Any]):
        """Add a health check function"""
        self.checks.append((name, check_func))
    
    async def run_checks(self) -> Dict[str, str]:
        """Run all health checks"""
        results = {}
        for name, check_func in self.checks:
            try:
                result = await check_func()
                results[name] = "healthy" if result else "unhealthy"
            except Exception as e:
                logger.error(f"Health check {name} failed: {str(e)}")
                results[name] = f"error: {str(e)}"
        return results

# Global instances
metrics_collector = MetricsCollector()
health_checker = HealthChecker()