from prometheus_client import Counter, Histogram, Gauge

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

def record_request(method: str, endpoint: str, status: int):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

def record_request_duration(method: str, endpoint: str, duration: float):
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

def set_active_connections(count: int):
    ACTIVE_CONNECTIONS.set(count)