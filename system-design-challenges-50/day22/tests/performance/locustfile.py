from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import random
import string
import json

class FeedUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Called when a Locust user starts running"""
        # Register a new user
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{username}@example.com"
        password = "testpassword123"
        
        response = self.client.post("/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            self.user_id = response.json()["id"]
            # Login to get token
            login_response = self.client.post("/auth/login", json={
                "username": username,
                "password": password
            })
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.auth_header = {"Authorization": f"Bearer {self.token}"}
    
    @task(10)
    def get_personalized_feed(self):
        """Get personalized feed"""
        if hasattr(self, 'auth_header'):
            self.client.get("/feed/personalized", headers=self.auth_header)
    
    @task(5)
    def get_explore_feed(self):
        """Get explore feed"""
        self.client.get("/feed/explore")
    
    @task(3)
    def create_post(self):
        """Create a new post"""
        if hasattr(self, 'auth_header'):
            content = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=100))
            self.client.post("/posts/", json={"content": content}, headers=self.auth_header)
    
    @task(1)
    def health_check(self):
        """Health check endpoint"""
        self.client.get("/health/")
    
    @task(1)
    def readiness_check(self):
        """Readiness check endpoint"""
        self.client.get("/health/ready")

# Custom event handlers for monitoring
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    """Event handler for each request"""
    if exception:
        print(f"Request failed: {request_type} {name} - {exception}")
    else:
        if response.status_code >= 400:
            print(f"Request failed with status {response.status_code}: {request_type} {name}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Event handler for test start"""
    print("Load test started")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Event handler for test stop"""
    print("Load test finished")