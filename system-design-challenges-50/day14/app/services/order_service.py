from typing import List, Optional
from datetime import datetime

class OrderItem:
    def __init__(self, product_id: int, quantity: int, price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class Order:
    def __init__(self, id: int, user_id: int, items: List[OrderItem]):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.status = "pending"
        self.total_amount = sum(item.quantity * item.price for item in items)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class OrderService:
    def __init__(self):
        # In a real implementation, this would be a database
        self.orders = {}
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        return self.orders.get(order_id)
    
    def list_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """List all orders"""
        orders = list(self.orders.values())
        return orders[skip : skip + limit]
    
    def create_order(self, user_id: int, items: List[OrderItem]) -> Order:
        """Create a new order"""
        order_id = len(self.orders) + 1
        order = Order(order_id, user_id, items)
        self.orders[order_id] = order
        return order
    
    def cancel_order(self, order_id: int) -> Optional[Order]:
        """Cancel an order"""
        order = self.orders.get(order_id)
        if not order:
            return None
        
        order.status = "cancelled"
        order.updated_at = datetime.now()
        return order
    
    def complete_order(self, order_id: int) -> Optional[Order]:
        """Complete an order"""
        order = self.orders.get(order_id)
        if not order:
            return None
        
        order.status = "completed"
        order.updated_at = datetime.now()
        return order