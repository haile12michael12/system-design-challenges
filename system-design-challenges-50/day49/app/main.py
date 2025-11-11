from fastapi import FastAPI

app = FastAPI(title="Day 49 - Cost-Aware Autoscaler")

# Import routers
from app.api import health, dashboard

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to Day 49 - Cost-Aware Autoscaler"}

@app.on_event("startup")
async def startup_event():
    print("Day 49 - Cost-Aware Autoscaler started successfully")
