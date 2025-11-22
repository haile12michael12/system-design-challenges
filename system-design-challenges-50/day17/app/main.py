from fastapi import FastAPI
from pydantic import BaseModel

from .core.config import settings
from .core.logging_config import setup_logging
from .core.monitoring import metrics_middleware
from .core.exceptions import setup_exception_handlers
from .api.routes_feed_write import router as feed_write_router
from .api.routes_feed_read import router as feed_read_router
from .api.routes_users import router as users_router
from .api.routes_debug import router as debug_router

# Set up logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Day 17 - Eventually Consistent Social Feed",
    description="An eventually consistent social feed system with asynchronous processing",
    version="1.0.0"
)

# Add middleware
metrics_middleware(app)

# Add exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(feed_write_router)
app.include_router(feed_read_router)
app.include_router(users_router)
app.include_router(debug_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Day 17 - Eventually Consistent Social Feed",
        "docs": "/docs",
        "health": "/debug/health"
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "feed-service",
        "version": "1.0.0"
    }
