#!/usr/bin/env python3

"""
Script to benchmark database queries and API endpoints
"""

import time
import random
import statistics
from typing import List, Callable, Any
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import settings

class QueryBenchmark:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def benchmark_query(self, query: str, iterations: int = 100) -> dict:
        """Benchmark a database query"""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            
            # Execute query
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                # Consume result to ensure query is fully executed
                result.fetchall()
            
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        return self._calculate_stats(times)
    
    def benchmark_function(self, func: Callable, iterations: int = 100, *args, **kwargs) -> dict:
        """Benchmark a Python function"""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            
            # Execute function
            func(*args, **kwargs)
            
            end_time = time.time()
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        return self._calculate_stats(times)
    
    def _calculate_stats(self, times: List[float]) -> dict:
        """Calculate statistics from timing data"""
        return {
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "p95": self._percentile(times, 95),
            "p99": self._percentile(times, 99),
            "samples": len(times)
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data"""
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

class APIBenchmark:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def benchmark_endpoint(self, method: str, endpoint: str, iterations: int = 100, 
                         headers: dict = None, data: dict = None) -> dict:
        """Benchmark an API endpoint"""
        times = []
        method_func = getattr(requests, method.lower())
        
        for _ in range(iterations):
            start_time = time.time()
            
            # Execute API call
            if data:
                response = method_func(f"{self.base_url}{endpoint}", headers=headers, json=data)
            else:
                response = method_func(f"{self.base_url}{endpoint}", headers=headers)
            
            end_time = time.time()
            
            # Only count successful requests
            if response.status_code < 400:
                times.append((end_time - start_time) * 1000)  # Convert to milliseconds
            else:
                print(f"Warning: Request failed with status {response.status_code}")
        
        if not times:
            return {"error": "All requests failed"}
        
        return self._calculate_stats(times)
    
    def _calculate_stats(self, times: List[float]) -> dict:
        """Calculate statistics from timing data"""
        return {
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "p95": self._percentile(times, 95),
            "p99": self._percentile(times, 99),
            "samples": len(times),
            "success_rate": len(times) / len(times) * 100  # This is simplified
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data"""
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

def main():
    """Run benchmarks"""
    print("🚀 Starting benchmarks...")
    
    # Database query benchmarks
    print("\n📊 Database Query Benchmarks:")
    db_benchmark = QueryBenchmark()
    
    # Benchmark user lookup by ID
    user_by_id_query = "SELECT * FROM users WHERE id = 1"
    stats = db_benchmark.benchmark_query(user_by_id_query)
    print(f"User lookup by ID: {stats['mean']:.2f}ms (p95: {stats['p95']:.2f}ms)")
    
    # Benchmark post lookup by author
    posts_by_author_query = "SELECT * FROM posts WHERE author_id = 1 LIMIT 10"
    stats = db_benchmark.benchmark_query(posts_by_author_query)
    print(f"Posts by author: {stats['mean']:.2f}ms (p95: {stats['p95']:.2f}ms)")
    
    # API endpoint benchmarks
    print("\n🌐 API Endpoint Benchmarks:")
    api_benchmark = APIBenchmark()
    
    # Benchmark health endpoint
    stats = api_benchmark.benchmark_endpoint("get", "/health/")
    print(f"Health endpoint: {stats['mean']:.2f}ms (p95: {stats['p95']:.2f}ms)")
    
    print("\n✅ Benchmarks completed!")

if __name__ == "__main__":
    main()