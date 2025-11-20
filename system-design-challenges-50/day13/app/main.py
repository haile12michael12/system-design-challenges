from fastapi import FastAPI
from .routes import payments
from .config import settings
from .prometheus_middleware import PrometheusMiddleware

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)
    
    # Include routers
    app.include_router(payments.router, prefix=settings.API_V1_STR)
    
    @app.get("/")
    async def root():
        return {"message": "Payment Processing Service"}
    
    @app.get("/metrics")
    async def metrics():
        # This would integrate with Prometheus client
        return {"message": "Metrics endpoint"}
    
    return app

app = create_app()