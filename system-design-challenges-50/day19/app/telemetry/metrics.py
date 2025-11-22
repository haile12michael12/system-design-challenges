from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from typing import Dict, Any


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

FILE_OPERATIONS = Counter(
    'app_file_operations_total',
    'Total number of file operations',
    ['operation', 'status']
)

STORAGE_USAGE = Gauge(
    'app_storage_usage_bytes',
    'Current storage usage in bytes',
    ['location']
)

REPLICA_LAG = Gauge(
    'app_replica_lag_seconds',
    'Replication lag in seconds',
    ['replica']
)

WAL_SEGMENT_COUNT = Gauge(
    'app_wal_segments_total',
    'Total number of WAL segments'
)

# Business metrics
FILES_UPLOADED = Counter(
    'app_files_uploaded_total',
    'Total number of files uploaded'
)

FILES_DOWNLOADED = Counter(
    'app_files_downloaded_total',
    'Total number of files downloaded'
)

FILES_DELETED = Counter(
    'app_files_deleted_total',
    'Total number of files deleted'
)

STORAGE_SAVED_BYTES = Counter(
    'app_storage_saved_bytes_total',
    'Total bytes saved to storage'
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
    
    def record_file_operation(self, operation: str, status: str = "success"):
        """Record a file operation"""
        FILE_OPERATIONS.labels(operation=operation, status=status).inc()
    
    def update_storage_usage(self, location: str, bytes_used: int):
        """Update storage usage metric"""
        STORAGE_USAGE.labels(location=location).set(bytes_used)
    
    def update_replica_lag(self, replica: str, lag_seconds: float):
        """Update replica lag metric"""
        REPLICA_LAG.labels(replica=replica).set(lag_seconds)
    
    def update_wal_segment_count(self, count: int):
        """Update WAL segment count"""
        WAL_SEGMENT_COUNT.set(count)
    
    def increment_files_uploaded(self):
        """Increment files uploaded counter"""
        FILES_UPLOADED.inc()
    
    def increment_files_downloaded(self):
        """Increment files downloaded counter"""
        FILES_DOWNLOADED.inc()
    
    def increment_files_deleted(self):
        """Increment files deleted counter"""
        FILES_DELETED.inc()
    
    def add_storage_saved_bytes(self, bytes_count: int):
        """Add to storage saved bytes counter"""
        STORAGE_SAVED_BYTES.inc(bytes_count)


# Global metrics collector instance
metrics_collector = MetricsCollector()