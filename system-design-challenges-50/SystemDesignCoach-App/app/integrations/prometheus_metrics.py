from prometheus_client import Counter, Histogram, Gauge, Summary
import time

# Define metrics
REQUEST_COUNT = Counter('system_design_coach_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('system_design_coach_request_duration_seconds', 'Request duration', ['method', 'endpoint'])
ACTIVE_USERS = Gauge('system_design_coach_active_users', 'Number of active users')
SUBMISSIONS_COUNT = Counter('system_design_coach_submissions_total', 'Total submissions', ['difficulty'])
GRADING_DURATION = Summary('system_design_coach_grading_duration_seconds', 'Time spent grading submissions')

class MetricsCollector:
    @staticmethod
    def record_request(method: str, endpoint: str, status: int, duration: float):
        """
        Record HTTP request metrics
        """
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
        
    @staticmethod
    def set_active_users(count: int):
        """
        Set the number of active users
        """
        ACTIVE_USERS.set(count)
        
    @staticmethod
    def record_submission(difficulty: str):
        """
        Record a new submission
        """
        SUBMISSIONS_COUNT.labels(difficulty=difficulty).inc()
        
    @staticmethod
    def time_grading():
        """
        Decorator to time grading operations
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                with GRADING_DURATION.time():
                    return func(*args, **kwargs)
            return wrapper
        return decorator