from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uvicorn
import os

from app.core.logging import setup_logging, get_logger
from app.core.config import settings
from app.db.session import init_db
from app.api.routes import health, files, admin
from app.services.recovery_service import RecoveryService
from app.telemetry.metrics import metrics_collector
from app.telemetry.tracing import instrument_fastapi

# Set up logging
setup_logging()

# Get logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Day 19 - Distributed File Storage System",
    description="A distributed file storage system with WAL, replication, and recovery",
    version="1.0.0"
)

# Instrument app for tracing
instrument_fastapi(app)

# Include routers
app.include_router(health.router)
app.include_router(files.router)
app.include_router(admin.router, prefix="/admin")

# Global state
startup_complete = False


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    global startup_complete
    
    logger.info("Starting application...")
    
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Bootstrap system
        recovery_service = RecoveryService()
        bootstrap_result = recovery_service.bootstrap_system()
        logger.info(f"System bootstrapped: {bootstrap_result}")
        
        startup_complete = True
        logger.info("Application startup complete")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down application...")
    # Cleanup operations would go here


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": "Distributed File Storage System",
        "version": "1.0.0",
        "status": "running" if startup_complete else "starting"
    }


@app.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """Expose application metrics"""
    # In a real implementation, this would return Prometheus metrics
    # For now, we'll return a simple status
    return {
        "status": "ok",
        "timestamp": "2025-11-22T00:00:00Z"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )