"""
Scheduler Worker
"""
import asyncio
from app.services.metrics_simulator import metrics_simulator
from app.services.autoscaler import autoscaler
from app.services.metrics_exporter import metrics_exporter

class Scheduler:
    def __init__(self):
        self.running = False
    
    async def start_scheduler(self):
        """Start the scheduling loop"""
        self.running = True
        print("Scheduler started")
        
        while self.running:
            # Generate metrics
            metrics = await metrics_simulator.generate_metrics()
            
            # Export metrics
            await metrics_exporter.export_metrics(metrics)
            
            # Evaluate scaling
            scaling_decision = await autoscaler.evaluate_scaling(metrics)
            
            # If scaling action was taken, export the event
            if scaling_decision["action"] != "no_scale":
                await metrics_exporter.export_scaling_event({
                    "action": scaling_decision["action"],
                    "reason": "cpu_threshold",
                    "old_replicas": autoscaler.current_replicas - (1 if scaling_decision["action"] == "scale_up" else -1),
                    "new_replicas": autoscaler.current_replicas,
                    "cost_impact": scaling_decision.get("cost_impact", 0)
                })
                
                # Update metrics simulator with new replica count
                metrics_simulator.update_replicas(autoscaler.current_replicas)
            
            # Wait before next cycle
            await asyncio.sleep(5)
    
    def stop_scheduler(self):
        """Stop the scheduling loop"""
        self.running = False
        print("Scheduler stopped")

# Global scheduler instance
scheduler = Scheduler()