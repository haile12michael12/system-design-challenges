"""
Custom Exception Handling
"""
class GeoKVError(Exception):
    """Base exception for Geo-KV Store"""
    pass

class KeyNotFoundError(GeoKVError):
    """Raised when a key is not found"""
    pass

class RegionUnavailableError(GeoKVError):
    """Raised when a region is unavailable"""
    pass

class ConsistencyError(GeoKVError):
    """Raised when there's a consistency issue"""
    pass

class ReplicationError(GeoKVError):
    """Raised when replication fails"""
    pass

def handle_exception(exc: Exception) -> dict:
    """Handle exceptions and return appropriate response"""
    if isinstance(exc, KeyNotFoundError):
        return {"error": "Key not found", "status_code": 404}
    elif isinstance(exc, RegionUnavailableError):
        return {"error": "Region unavailable", "status_code": 503}
    elif isinstance(exc, ConsistencyError):
        return {"error": "Consistency error", "status_code": 409}
    elif isinstance(exc, ReplicationError):
        return {"error": "Replication failed", "status_code": 500}
    else:
        return {"error": "Internal server error", "status_code": 500}