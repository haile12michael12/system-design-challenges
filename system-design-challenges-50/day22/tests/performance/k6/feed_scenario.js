import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test options
export const options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up to 10 users
    { duration: '1m', target: 10 },    // stay at 10 users
    { duration: '30s', target: 0 },    // ramp down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'],  // 95% of requests should be below 500ms
    'errors': ['rate<0.1'],             // error rate should be less than 10%
  },
};

// Base URL
const BASE_URL = 'http://localhost:8000';

// Test data
const userData = {
  username: `user_${Date.now()}`,
  email: `user_${Date.now()}@example.com`,
  password: 'testpassword123',
};

let authToken = '';
let userId = '';

export function setup() {
  // Register a new user
  const registerRes = http.post(`${BASE_URL}/auth/register`, JSON.stringify(userData), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(registerRes, {
    'user registered successfully': (r) => r.status === 200,
  }) || errorRate.add(1);
  
  if (registerRes.status === 200) {
    userId = registerRes.json('id');
    
    // Login to get auth token
    const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
      username: userData.username,
      password: userData.password,
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    check(loginRes, {
      'user logged in successfully': (r) => r.status === 200,
    }) || errorRate.add(1);
    
    if (loginRes.status === 200) {
      authToken = loginRes.json('access_token');
    }
  }
  
  return { authToken, userId };
}

export default function (data) {
  const { authToken, userId } = data;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`,
  };
  
  // Get personalized feed
  const feedRes = http.get(`${BASE_URL}/feed/personalized`, { headers });
  check(feedRes, {
    'personalized feed retrieved': (r) => r.status === 200,
  }) || errorRate.add(1);
  
  // Get explore feed
  const exploreRes = http.get(`${BASE_URL}/feed/explore`);
  check(exploreRes, {
    'explore feed retrieved': (r) => r.status === 200,
  }) || errorRate.add(1);
  
  // Create a post (every 10 iterations)
  if (__ITER % 10 === 0) {
    const content = `Test post content ${Date.now()}`;
    const postRes = http.post(`${BASE_URL}/posts/`, JSON.stringify({ content }), {
      headers: { ...headers },
    });
    check(postRes, {
      'post created successfully': (r) => r.status === 201,
    }) || errorRate.add(1);
  }
  
  // Health check
  const healthRes = http.get(`${BASE_URL}/health/`);
  check(healthRes, {
    'health check passed': (r) => r.status === 200,
  }) || errorRate.add(1);
  
  sleep(1);
}

export function teardown(data) {
  // Cleanup if needed
  console.log('Test completed');
}