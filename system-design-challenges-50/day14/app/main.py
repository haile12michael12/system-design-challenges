from fastapi import FastAPI
from .api.routes import catalog, orders, users, payments
from .core.config import settings

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Include routers
    app.include_router(catalog.router, prefix="/api/v1/catalog")
    app.include_router(orders.router, prefix="/api/v1/orders")
    app.include_router(users.router, prefix="/api/v1/users")
    app.include_router(payments.router, prefix="/api/v1/payments")
    
    @app.get("/")
    async def root():
        return {"message": "E-commerce Platform API"}
    
    return app

app = create_app()