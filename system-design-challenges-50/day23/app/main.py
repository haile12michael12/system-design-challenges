from fastapi import FastAPI
from app.api.orders import router as orders_router

app = FastAPI(title="Order Processing System", version="0.1.0")

# Include routers
app.include_router(orders_router, prefix="/orders", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Order Processing System"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}