"""
Metrics Collection
"""
# Metrics storage
class MetricsStore:
    def __init__(self):
        self.request_count = {}
        self.request_duration = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.active_connections = 0
        self.database_queries = {}
    
    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics"""
        key = f"{method}:{endpoint}:{status}"
        self.request_count[key] = self.request_count.get(key, 0) + 1
        self.request_duration[key] = self.request_duration.get(key, []) + [duration]
    
    def record_cache_hit(self):
        """Record cache hit"""
        self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        self.cache_misses += 1
    
    def update_active_connections(self, count: int):
        """Update active connections gauge"""
        self.active_connections = count
    
    def record_database_query(self, table: str, operation: str):
        """Record database query"""
        key = f"{table}:{operation}"
        self.database_queries[key] = self.database_queries.get(key, 0) + 1

# Global metrics store
metrics_store = MetricsStore()

def record_request(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics"""
    metrics_store.record_request(method, endpoint, status, duration)

def record_cache_hit():
    """Record cache hit"""
    metrics_store.record_cache_hit()

def record_cache_miss():
    """Record cache miss"""
    metrics_store.record_cache_miss()

def update_active_connections(count: int):
    """Update active connections gauge"""
    metrics_store.update_active_connections(count)

def record_database_query(table: str, operation: str):
    """Record database query"""
    metrics_store.record_database_query(table, operation)