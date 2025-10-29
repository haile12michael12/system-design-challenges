from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from .config.database import get_database, init_database
from .config.settings import settings
from .api import ingestion_router, tables_router, partitions_router, schema_router

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="A comprehensive data lake ingestion framework with schema evolution and partitioning"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ingestion_router)
app.include_router(tables_router)
app.include_router(partitions_router)
app.include_router(schema_router)

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "data-lake-ingestion"
    version: str = settings.api_version

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@app.get("/health", response_model=HealthResp)
async def health():
    """Health check endpoint"""
    return HealthResp()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Data Lake Ingestion Framework",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "title": settings.api_title,
        "version": settings.api_version,
        "description": "A comprehensive data lake ingestion framework",
        "features": [
            "Data ingestion with batch processing",
            "Schema evolution and versioning",
            "Partition management and optimization",
            "Storage abstraction layer",
            "RESTful API with comprehensive endpoints"
        ],
        "endpoints": {
            "ingestion": "/api/v1/ingestion",
            "tables": "/api/v1/tables",
            "partitions": "/api/v1/partitions",
            "schema": "/api/v1/schema"
        }
    }
