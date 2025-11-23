import redis
import json
from typing import Dict, List, Optional

class RegionState:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
    
    def get_region_status(self, region: str) -> Dict:
        """Get the current status of a region"""
        status_key = f"region:{region}:status"
        lag_key = f"region:{region}:lag"
        is_primary_key = f"region:{region}:is_primary"
        last_heartbeat_key = f"region:{region}:last_heartbeat"
        
        return {
            "region": region,
            "status": self.redis.get(status_key) or "unknown",
            "lag_seconds": float(self.redis.get(lag_key) or 0),
            "is_primary": self.redis.get(is_primary_key) == "true",
            "last_heartbeat": self.redis.get(last_heartbeat_key)
        }
    
    def set_region_status(self, region: str, status: str, lag_seconds: float = 0.0, is_primary: bool = False):
        """Set the status of a region"""
        status_key = f"region:{region}:status"
        lag_key = f"region:{region}:lag"
        is_primary_key = f"region:{region}:is_primary"
        last_heartbeat_key = f"region:{region}:last_heartbeat"
        
        self.redis.set(status_key, status)
        self.redis.set(lag_key, lag_seconds)
        self.redis.set(is_primary_key, "true" if is_primary else "false")
        self.redis.set(last_heartbeat_key, self._get_current_timestamp())
    
    def get_all_regions(self) -> List[Dict]:
        """Get status of all regions"""
        # In a real implementation, we would have a predefined list of regions
        # For now, we'll get regions from Redis keys
        region_keys = self.redis.keys("region:*:status")
        regions = []
        
        for key in region_keys:
            region = key.split(":")[1]
            regions.append(self.get_region_status(region))
        
        return regions
    
    def update_heartbeat(self, region: str):
        """Update the heartbeat timestamp for a region"""
        last_heartbeat_key = f"region:{region}:last_heartbeat"
        self.redis.set(last_heartbeat_key, self._get_current_timestamp())
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as string"""
        import time
        return str(int(time.time()))
    
    def initialize_regions(self, regions: List[str]):
        """Initialize regions with default status"""
        for region in regions:
            # Check if region already exists
            status_key = f"region:{region}:status"
            if not self.redis.exists(status_key):
                self.set_region_status(region, "active", 0.0, region == regions[0])  # First region is primary