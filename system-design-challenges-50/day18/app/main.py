from fastapi import FastAPI
from pydantic import BaseModel

from .core.logging import setup_logging
from .api.v1 import health, articles

# Set up logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Day 18 - Latency-Aware News App",
    description="A latency-aware news application with caching and prefetching capabilities",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(articles.router, prefix="/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Day 18 - Latency-Aware News App",
        "docs": "/docs",
        "health": "/v1/health/"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "news-service",
        "version": "1.0.0"
    }
