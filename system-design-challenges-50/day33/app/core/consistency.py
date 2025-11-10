"""
Consistency Strategies
"""
from enum import Enum
from typing import Dict, Any

class ConsistencyLevel(Enum):
    EVENTUAL = "eventual"
    STRONG = "strong"
    SEQUENTIAL = "sequential"

class ConsistencyStrategy:
    def __init__(self, level: ConsistencyLevel):
        self.level = level
    
    def should_replicate_immediately(self) -> bool:
        return self.level == ConsistencyLevel.STRONG
    
    def get_replication_delay(self) -> int:
        if self.level == ConsistencyLevel.EVENTUAL:
            return 1000  # 1 second
        elif self.level == ConsistencyLevel.SEQUENTIAL:
            return 100   # 100ms
        return 0  # Strong consistency - no delay