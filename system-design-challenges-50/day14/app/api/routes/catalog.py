from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Mock data storage
products = []

@router.get("/", response_model=List[Product])
async def list_products(skip: int = 0, limit: int = 100):
    """List all products"""
    return products[skip : skip + limit]

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    """Create a new product"""
    new_product = Product(
        id=len(products) + 1,
        **product.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    products.append(new_product)
    return new_product

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a product by ID"""
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}