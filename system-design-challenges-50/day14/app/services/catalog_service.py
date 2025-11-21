from typing import List, Optional
from datetime import datetime

class Product:
    def __init__(self, id: int, name: str, description: str, price: float, category: str):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class CatalogService:
    def __init__(self):
        # In a real implementation, this would be a database
        self.products = {}
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        return self.products.get(product_id)
    
    def list_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """List all products"""
        products = list(self.products.values())
        return products[skip : skip + limit]
    
    def create_product(self, name: str, description: str, price: float, category: str) -> Product:
        """Create a new product"""
        product_id = len(self.products) + 1
        product = Product(product_id, name, description, price, category)
        self.products[product_id] = product
        return product
    
    def update_product(self, product_id: int, name: str = None, description: str = None, 
                      price: float = None, category: str = None) -> Optional[Product]:
        """Update a product"""
        product = self.products.get(product_id)
        if not product:
            return None
        
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if category is not None:
            product.category = category
        
        product.updated_at = datetime.now()
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False