from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Geo-Distributed Key-Value Store"
)

# Import routers
from app.api import health, kv, replication, admin

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(kv.router, prefix="/kv", tags=["kv"])
app.include_router(replication.router, prefix="/replicate", tags=["replication"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to Day 33 - Geo-Distributed Key-Value Store"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day33"}
