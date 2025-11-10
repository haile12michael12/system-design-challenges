from fastapi import FastAPI

app = FastAPI(title="Day 8 - Database Migration Simulator")

# Import health router
from app.api.v1 import health

# Include routers
app.include_router(health.router, prefix="/v1/health", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Welcome to Day 8 - Database Migration Simulator"}

@app.on_event("startup")
async def startup_event():
    print("Day 8 - Database Migration Simulator started successfully")
