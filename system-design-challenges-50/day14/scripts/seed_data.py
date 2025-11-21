#!/usr/bin/env python3

import random
from app.services.catalog_service import CatalogService
from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService

def seed_data():
    """Seed the database with sample data"""
    # Create catalog service
    catalog_service = CatalogService()
    
    # Create sample products
    products = [
        ("Laptop", "High-performance laptop", 999.99, "Electronics"),
        ("Smartphone", "Latest smartphone", 699.99, "Electronics"),
        ("Book", "Bestselling novel", 19.99, "Books"),
        ("Headphones", "Wireless headphones", 149.99, "Electronics"),
        ("Coffee Mug", "Ceramic coffee mug", 12.99, "Home"),
    ]
    
    for name, description, price, category in products:
        catalog_service.create_product(name, description, price, category)
        print(f"Created product: {name}")
    
    # Create user service
    user_service = UserService()
    
    # Create sample users
    users = [
        ("john_doe", "john@example.com", "John Doe", "password123"),
        ("jane_smith", "jane@example.com", "Jane Smith", "password456"),
        ("bob_johnson", "bob@example.com", "Bob Johnson", "password789"),
    ]
    
    for username, email, full_name, password in users:
        user_service.create_user(username, email, full_name, password)
        print(f"Created user: {username}")
    
    print("Data seeding completed!")

if __name__ == "__main__":
    seed_data()