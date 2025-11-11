"""
Autoscaler Service
"""
from typing import Dict, Any
import asyncio

class Autoscaler:
    def __init__(self):
        self.enabled = True
        self.target_cpu = 70.0
        self.min_replicas = 1
        self.max_replicas = 10
        self.current_replicas = 3
        self.cost_per_replica_hour = 0.05
    
    async def evaluate_scaling(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if scaling is needed based on metrics"""
        cpu_usage = metrics.get("cpu_usage", 0)
        memory_usage = metrics.get("memory_usage", 0)
        
        # Simple scaling logic based on CPU usage
        if cpu_usage > self.target_cpu * 1.2 and self.current_replicas < self.max_replicas:
            return self.scale_up()
        elif cpu_usage < self.target_cpu * 0.8 and self.current_replicas > self.min_replicas:
            return self.scale_down()
        
        return {"action": "no_scale", "replicas": self.current_replicas}
    
    def scale_up(self) -> Dict[str, Any]:
        """Scale up the service"""
        self.current_replicas += 1
        print(f"Scaling up to {self.current_replicas} replicas")
        return {
            "action": "scale_up",
            "replicas": self.current_replicas,
            "cost_impact": self.cost_per_replica_hour
        }
    
    def scale_down(self) -> Dict[str, Any]:
        """Scale down the service"""
        self.current_replicas -= 1
        print(f"Scaling down to {self.current_replicas} replicas")
        return {
            "action": "scale_down",
            "replicas": self.current_replicas,
            "cost_savings": self.cost_per_replica_hour
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current autoscaler status"""
        return {
            "enabled": self.enabled,
            "target_cpu": self.target_cpu,
            "min_replicas": self.min_replicas,
            "max_replicas": self.max_replicas,
            "current_replicas": self.current_replicas
        }
    
    def get_cost_per_hour(self) -> float:
        """Calculate current hourly cost"""
        return self.current_replicas * self.cost_per_replica_hour

# Global autoscaler instance
autoscaler = Autoscaler()