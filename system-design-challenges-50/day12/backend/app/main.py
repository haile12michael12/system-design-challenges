from fastapi import FastAPI
from .api import health, cap
from .core.config import settings

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Include routers
    app.include_router(health.router, prefix=settings.API_V1_STR)
    app.include_router(cap.router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    async def root():
        return {"message": "Welcome to Day 12 - CAP Theorem Visualizer"}
    
    return app

app = create_app()