"""
Metrics Simulator
"""
import random
import asyncio
from typing import Dict, Any

class MetricsSimulator:
    def __init__(self):
        self.base_cpu = 50.0
        self.base_memory = 60.0
        self.replicas = 3
    
    async def generate_metrics(self) -> Dict[str, Any]:
        """Generate simulated metrics"""
        # Simulate some variation in metrics
        cpu_variation = random.uniform(-10, 10)
        memory_variation = random.uniform(-5, 5)
        
        cpu_usage = max(0, min(100, self.base_cpu + cpu_variation))
        memory_usage = max(0, min(100, self.base_memory + memory_variation))
        
        return {
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "replicas": self.replicas,
            "cost_per_hour": round(self.replicas * 0.05, 2)
        }
    
    def update_replicas(self, replicas: int):
        """Update replica count"""
        self.replicas = replicas
        # Adjust base metrics based on replica count
        self.base_cpu = max(20, 50 - (replicas - 3) * 2)
        self.base_memory = max(30, 60 - (replicas - 3) * 1)

# Global metrics simulator instance
metrics_simulator = MetricsSimulator()