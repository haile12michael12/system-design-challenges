import time
import random
from ..db.models import SimulationRequest, MetricsData
from ..core.logging_config import setup_logging

logger = setup_logging()

def run_simulation(simulation_id: str, request: SimulationRequest):
    """Run a simulation and generate metrics data"""
    logger.info(f"Starting simulation {simulation_id} with {request.instances} instances and {request.workload} workload")
    
    # Simulate processing
    time.sleep(2)  # Simulate computation time
    
    # Generate mock metrics data
    metrics_data = []
    for i in range(10):
        metrics = MetricsData(
            timestamp=time.time(),
            latency=random.uniform(10, 100),
            cost=request.instances * random.uniform(0.1, 0.5),
            instances=request.instances
        )
        metrics_data.append(metrics)
        
    logger.info(f"Completed simulation {simulation_id}")
    return metrics_data