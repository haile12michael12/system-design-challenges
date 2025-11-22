import asyncio
import aiohttp
import time
import random
import string
from typing import List
import argparse


async def upload_file(session: aiohttp.ClientSession, base_url: str, file_content: bytes) -> dict:
    """Upload a file"""
    try:
        files = {"file": ("test_file.txt", file_content, "text/plain")}
        async with session.post(f"{base_url}/upload", data=files) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}


async def download_file(session: aiohttp.ClientSession, base_url: str, file_id: str) -> dict:
    """Download a file"""
    try:
        async with session.get(f"{base_url}/download/{file_id}") as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}


async def delete_file(session: aiohttp.ClientSession, base_url: str, file_id: str) -> dict:
    """Delete a file"""
    try:
        async with session.delete(f"{base_url}/files/{file_id}") as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}


async def run_load_test(base_url: str, num_requests: int, concurrent_users: int):
    """Run load test"""
    print(f"Starting load test with {num_requests} requests and {concurrent_users} concurrent users")
    
    start_time = time.time()
    
    # Generate test data
    test_files = []
    for i in range(num_requests):
        # Generate random content
        content_size = random.randint(100, 1000)
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=content_size))
        test_files.append(content.encode())
    
    # Create session
    async with aiohttp.ClientSession() as session:
        # Upload files
        print("Uploading files...")
        upload_tasks = []
        for i, content in enumerate(test_files):
            task = upload_file(session, base_url, content)
            upload_tasks.append(task)
            
            # Control concurrency
            if len(upload_tasks) >= concurrent_users:
                results = await asyncio.gather(*upload_tasks)
                upload_tasks = []
                print(f"Uploaded {i+1} files...")
        
        # Handle remaining tasks
        if upload_tasks:
            results = await asyncio.gather(*upload_tasks)
        
        # Extract file IDs
        file_ids = [result.get("file_id") for result in results if "file_id" in result]
        
        # Download files
        print("Downloading files...")
        download_tasks = []
        for i, file_id in enumerate(file_ids):
            if file_id:
                task = download_file(session, base_url, file_id)
                download_tasks.append(task)
                
                # Control concurrency
                if len(download_tasks) >= concurrent_users:
                    results = await asyncio.gather(*download_tasks)
                    download_tasks = []
                    print(f"Downloaded {i+1} files...")
        
        # Handle remaining tasks
        if download_tasks:
            results = await asyncio.gather(*download_tasks)
        
        # Delete files
        print("Deleting files...")
        delete_tasks = []
        for i, file_id in enumerate(file_ids):
            if file_id:
                task = delete_file(session, base_url, file_id)
                delete_tasks.append(task)
                
                # Control concurrency
                if len(delete_tasks) >= concurrent_users:
                    results = await asyncio.gather(*delete_tasks)
                    delete_tasks = []
                    print(f"Deleted {i+1} files...")
        
        # Handle remaining tasks
        if delete_tasks:
            results = await asyncio.gather(*delete_tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Load test completed in {total_time:.2f} seconds")
    print(f"Requests per second: {num_requests / total_time:.2f}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Load test for file storage service")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the service")
    parser.add_argument("--requests", type=int, default=100, help="Number of requests to make")
    parser.add_argument("--concurrent", type=int, default=10, help="Number of concurrent users")
    
    args = parser.parse_args()
    
    # Run load test
    asyncio.run(run_load_test(args.url, args.requests, args.concurrent))


if __name__ == "__main__":
    main()