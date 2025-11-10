"""
Prometheus Metrics Setup
"""
# Metrics storage
class MetricsStore:
    def __init__(self):
        self.request_count = {}
        self.request_duration = {}
        self.active_connections = 0
        self.key_operations = {}
        self.replication_events = {}
    
    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics"""
        key = f"{method}:{endpoint}:{status}"
        self.request_count[key] = self.request_count.get(key, 0) + 1
        self.request_duration[key] = self.request_duration.get(key, []) + [duration]
    
    def record_key_operation(self, operation: str, region: str):
        """Record key operation metrics"""
        key = f"{operation}:{region}"
        self.key_operations[key] = self.key_operations.get(key, 0) + 1
    
    def record_replication_event(self, source_region: str, target_region: str, status: str):
        """Record replication event metrics"""
        key = f"{source_region}:{target_region}:{status}"
        self.replication_events[key] = self.replication_events.get(key, 0) + 1
    
    def update_active_connections(self, count: int):
        """Update active connections gauge"""
        self.active_connections = count

# Global metrics store
metrics_store = MetricsStore()

def record_request(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics"""
    metrics_store.record_request(method, endpoint, status, duration)

def record_key_operation(operation: str, region: str):
    """Record key operation metrics"""
    metrics_store.record_key_operation(operation, region)

def record_replication_event(source_region: str, target_region: str, status: str):
    """Record replication event metrics"""
    metrics_store.record_replication_event(source_region, target_region, status)

def update_active_connections(count: int):
    """Update active connections gauge"""
    metrics_store.update_active_connections(count)