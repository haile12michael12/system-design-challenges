"""
Vector Clock Utilities
"""
from typing import Dict, List
from collections import defaultdict

class VectorClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = defaultdict(int)
        self.clock[node_id] = 0
    
    def tick(self) -> None:
        """Increment the clock for this node"""
        self.clock[self.node_id] += 1
    
    def update(self, other_clock: Dict[str, int]) -> None:
        """Update this clock with another clock"""
        for node, timestamp in other_clock.items():
            self.clock[node] = max(self.clock[node], timestamp)
        self.tick()
    
    def compare(self, other_clock: Dict[str, int]) -> int:
        """
        Compare two vector clocks
        Returns:
        -1 if this clock is older
         0 if clocks are concurrent
         1 if this clock is newer
        """
        self_newer = all(self.clock[node] >= other_clock.get(node, 0) for node in self.clock)
        other_newer = all(other_clock.get(node, 0) >= self.clock[node] for node in other_clock)
        
        if self_newer and not other_newer:
            return 1
        elif other_newer and not self_newer:
            return -1
        elif self.clock == other_clock:
            return 0
        else:
            return 0  # Concurrent
    
    def to_dict(self) -> Dict[str, int]:
        """Convert clock to dictionary"""
        return dict(self.clock)
    
    @classmethod
    def from_dict(cls, node_id: str, clock_dict: Dict[str, int]) -> 'VectorClock':
        """Create VectorClock from dictionary"""
        vc = cls(node_id)
        vc.clock = defaultdict(int, clock_dict)
        return vc