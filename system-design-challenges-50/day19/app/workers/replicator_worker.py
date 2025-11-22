import asyncio
import time
from typing import Dict
from celery import Celery

from app.core.config import settings
from app.services.replication_service import ReplicationService
from app.db.session import init_db

# Initialize Celery
celery_app = Celery("replicator_worker")
celery_app.conf.broker_url = settings.REDIS_URL
celery_app.conf.result_backend = settings.REDIS_URL

# Initialize replication service
replication_service = ReplicationService()


@celery_app.task
def async_replicate_file(file_id: str) -> Dict[str, bool]:
    """Asynchronously replicate a file to all replicas"""
    try:
        result = replication_service.sync_file_to_replicas(file_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@celery_app.task
def async_remove_file(file_id: str) -> Dict[str, bool]:
    """Asynchronously remove a file from all replicas"""
    try:
        result = replication_service.remove_file_from_replicas(file_id)
        return result
    except Exception as e:
        return {"error": str(e)}


@celery_app.task
def periodic_replica_sync() -> Dict[str, str]:
    """Periodically synchronize all replicas"""
    try:
        result = replication_service.sync_all_replicas()
        return result
    except Exception as e:
        return {"error": str(e)}


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks"""
    # Sync replicas every 30 minutes
    sender.add_periodic_task(
        1800.0,
        periodic_replica_sync.s(),
        name='periodic replica sync'
    )


if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Start worker
    celery_app.worker_main(["worker", "--loglevel=info"])