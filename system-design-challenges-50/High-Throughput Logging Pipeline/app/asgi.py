"""
ASGI entrypoint for deployment with ASGI servers like Uvicorn or Hypercorn
"""
from app.main import app

# For ASGI servers, we just need to expose the app
application = app