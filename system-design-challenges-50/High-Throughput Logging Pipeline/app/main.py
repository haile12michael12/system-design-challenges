from fastapi import FastAPI
from pydantic import BaseModel
from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="High-Throughput Logging Pipeline"
)

# Import routers
from app.routers import health, ingest, query

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
app.include_router(query.router, prefix="/query", tags=["query"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.on_event("startup")
async def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully")
