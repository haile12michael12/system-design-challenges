from fastapi import FastAPI
from .app.api import health, simulate, autoscaler
from .app.core.config import settings

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Include routers
    app.include_router(health.router, prefix=settings.API_V1_STR)
    app.include_router(simulate.router, prefix=settings.API_V1_STR)
    app.include_router(autoscaler.router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    async def root():
        return {"message": "Welcome to Auto-Scaler Visualizer"}
    
    return app

app = create_app()
