from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from app.core.config import settings
from app.core.observability import setup_logging
from app.db.session import init_db
from app.api.v1 import recommend, metrics, config_apply, simulate
from app.api import deps

# Set up logging
setup_logging()

# Get logger
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Day 20 - Cost Optimization Recommendation Engine",
    description="A system for generating cost optimization recommendations with SLA validation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommend.router, prefix="/v1")
app.include_router(metrics.router, prefix="/v1")
app.include_router(config_apply.router, prefix="/v1")
app.include_router(simulate.router, prefix="/v1")

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
async def root():
    """Root endpoint"""
    return {
        "message": "Cost Optimization Recommendation Engine",
        "version": "1.0.0",
        "status": "running" if startup_complete else "starting"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-11-22T00:00:00Z",
        "service": "cost-optimizer"
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready" if startup_complete else "starting",
        "timestamp": "2025-11-22T00:00:00Z",
        "dependencies": {
            "database": "ok" if startup_complete else "initializing",
            "cache": "ok",
            "telemetry": "ok"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )