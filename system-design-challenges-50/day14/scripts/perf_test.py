#!/usr/bin/env python3

import time
import random
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService

def run_performance_test():
    """Run performance tests"""
    # Create services
    catalog_service = CatalogService()
    order_service = OrderService()
    payment_service = PaymentService()
    
    # Create test products
    print("Creating test products...")
    for i in range(100):
        catalog_service.create_product(
            f"Product {i}", 
            f"Description for product {i}", 
            random.uniform(10, 1000), 
            "Test"
        )
    
    # Measure product listing performance
    print("Testing product listing performance...")
    start_time = time.time()
    products = catalog_service.list_products()
    end_time = time.time()
    print(f"Listed {len(products)} products in {end_time - start_time:.4f} seconds")
    
    # Measure product creation performance
    print("Testing product creation performance...")
    start_time = time.time()
    for i in range(100):
        catalog_service.create_product(
            f"Perf Product {i}", 
            f"Performance test product {i}", 
            random.uniform(10, 1000), 
            "Performance"
        )
    end_time = time.time()
    print(f"Created 100 products in {end_time - start_time:.4f} seconds")
    
    print("Performance testing completed!")

if __name__ == "__main__":
    run_performance_test()