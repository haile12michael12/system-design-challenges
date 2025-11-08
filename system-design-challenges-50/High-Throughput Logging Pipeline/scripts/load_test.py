#!/usr/bin/env python3
"""
Load test script for the logging pipeline
"""
import asyncio
import aiohttp
import time
import random
import string
from datetime import datetime
from typing import List

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "test-api-key"
NUM_REQUESTS = 1000
BATCH_SIZE = 100
CONCURRENT_REQUESTS = 10

def generate_random_string(length: int) -> str:
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_log_entry() -> dict:
    """Generate a random log entry"""
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    services = ["auth-service", "payment-service", "notification-service", "user-service"]
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "level": random.choice(levels),
        "message": f"Test log message: {generate_random_string(50)}",
        "service": random.choice(services),
        "tenant_id": f"tenant-{random.randint(1, 100)}",
        "trace_id": generate_random_string(32),
        "span_id": generate_random_string(16),
        "metadata": {
            "user_id": random.randint(1, 10000),
            "request_id": generate_random_string(8)
        }
    }

async def send_single_log(session: aiohttp.ClientSession, log_entry: dict) -> bool:
    """Send a single log entry"""
    try:
        async with session.post(
            f"{API_URL}/ingest/",
            json=log_entry,
            headers={"x-api-key": API_KEY}
        ) as response:
            return response.status == 200
    except Exception:
        return False

async def send_batch_logs(session: aiohttp.ClientSession, log_entries: List[dict]) -> bool:
    """Send a batch of log entries"""
    try:
        async with session.post(
            f"{API_URL}/ingest/batch",
            json={"logs": log_entries},
            headers={"x-api-key": API_KEY}
        ) as response:
            return response.status == 200
    except Exception:
        return False

async def load_test_single_logs():
    """Load test with single log entries"""
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        success_count = 0
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        
        async def send_with_semaphore(log_entry):
            async with semaphore:
                return await send_single_log(session, log_entry)
        
        # Generate all log entries first
        log_entries = [generate_log_entry() for _ in range(NUM_REQUESTS)]
        
        # Send all requests concurrently
        tasks = [send_with_semaphore(log_entry) for log_entry in log_entries]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(results)
        end_time = time.time()
        
        print(f"Single logs test completed in {end_time - start_time:.2f} seconds")
        print(f"Success rate: {success_count}/{NUM_REQUESTS} ({success_count/NUM_REQUESTS*100:.2f}%)")

async def load_test_batch_logs():
    """Load test with batch log entries"""
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        success_count = 0
        total_requests = NUM_REQUESTS // BATCH_SIZE
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        
        async def send_batch_with_semaphore(log_entries):
            async with semaphore:
                return await send_batch_logs(session, log_entries)
        
        # Generate all log entries first
        log_entries = [generate_log_entry() for _ in range(NUM_REQUESTS)]
        
        # Split into batches
        batches = [log_entries[i:i+BATCH_SIZE] for i in range(0, len(log_entries), BATCH_SIZE)]
        
        # Send all batch requests concurrently
        tasks = [send_batch_with_semaphore(batch) for batch in batches]
        results = await asyncio.gather(*tasks)
        
        success_count = sum(results)
        end_time = time.time()
        
        print(f"Batch logs test completed in {end_time - start_time:.2f} seconds")
        print(f"Success rate: {success_count}/{total_requests} ({success_count/total_requests*100:.2f}%)")

async def main():
    """Main function"""
    print("Starting load test...")
    
    print("\n=== Testing single log entries ===")
    await load_test_single_logs()
    
    print("\n=== Testing batch log entries ===")
    await load_test_batch_logs()
    
    print("\nLoad test completed!")

if __name__ == "__main__":
    asyncio.run(main())