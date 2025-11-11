"""
Metrics Exporter
"""
from typing import Dict, Any
from app.db.models import MetricsRecord, ScalingEvent
from app.db.session import AsyncSessionLocal

class MetricsExporter:
    def __init__(self):
        pass
    
    async def export_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Export metrics to database"""
        async with AsyncSessionLocal() as session:
            try:
                record = MetricsRecord(
                    cpu_usage=metrics.get("cpu_usage"),
                    memory_usage=metrics.get("memory_usage"),
                    replicas=metrics.get("replicas"),
                    cost_per_hour=metrics.get("cost_per_hour")
                )
                session.add(record)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"Error exporting metrics: {e}")
                return False
    
    async def export_scaling_event(self, event: Dict[str, Any]) -> bool:
        """Export scaling event to database"""
        async with AsyncSessionLocal() as session:
            try:
                record = ScalingEvent(
                    action=event.get("action"),
                    reason=event.get("reason", "cpu_threshold"),
                    old_replicas=event.get("old_replicas"),
                    new_replicas=event.get("new_replicas"),
                    cost_impact=event.get("cost_impact", 0)
                )
                session.add(record)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"Error exporting scaling event: {e}")
                return False

# Global metrics exporter instance
metrics_exporter = MetricsExporter()