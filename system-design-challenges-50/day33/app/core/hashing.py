"""
Consistent Hashing and Partitioning
"""
import hashlib
from typing import List, Dict, Optional

class ConsistentHasher:
    def __init__(self, nodes: List[str], replicas: int = 3):
        self.replicas = replicas
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
        
        for node in nodes:
            self.add_node(node)
    
    def _hash(self, key: str) -> int:
        """Generate hash for a key"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node: str) -> None:
        """Add a node to the hash ring"""
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()
    
    def remove_node(self, node: str) -> None:
        """Remove a node from the hash ring"""
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]
            if key in self.sorted_keys:
                self.sorted_keys.remove(key)
    
    def get_node(self, key: str) -> Optional[str]:
        """Get the node responsible for a key"""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        for ring_key in self.sorted_keys:
            if hash_key <= ring_key:
                return self.ring[ring_key]
        
        # Wrap around to the first node
        return self.ring[self.sorted_keys[0]]