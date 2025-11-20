from .celery_app import celery_app
from ..services.simulator import run_simulation
from ..db.models import SimulationRequest

@celery_app.task
def run_simulation_task(simulation_id: str, request: SimulationRequest):
    """Celery task to run simulation"""
    return run_simulation(simulation_id, request)