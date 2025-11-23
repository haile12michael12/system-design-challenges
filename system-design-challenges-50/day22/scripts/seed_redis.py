#!/usr/bin/env python3

"""
Script to seed Redis with test data
"""

import redis
import json
import random
from datetime import datetime, timedelta
from app.config import settings
from app.cache.keys import *

def seed_redis():
    """Seed Redis with test data"""
    # Connect to Redis
    r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    
    print("Seeding Redis with test data...")
    
    # Seed user profile cache
    print("Seeding user profiles...")
    for i in range(1, 101):
        user_data = {
            "id": i,
            "username": f"user_{i}",
            "email": f"user_{i}@example.com",
            "bio": f"This is the bio for user {i}",
            "followers_count": random.randint(0, 1000),
            "following_count": random.randint(0, 500),
            "posts_count": random.randint(0, 100)
        }
        key = user_profile_key(i)
        r.setex(key, 3600, json.dumps(user_data))  # 1 hour TTL
    
    # Seed post cache
    print("Seeding posts...")
    for i in range(1, 1001):
        post_data = {
            "id": i,
            "author_id": random.randint(1, 100),
            "content": f"This is test post #{i}",
            "media_url": f"https://example.com/media/{i}.jpg" if random.random() > 0.7 else None,
            "likes_count": random.randint(0, 1000),
            "comments_count": random.randint(0, 100),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
        }
        key = post_key(i)
        r.setex(key, 1800, json.dumps(post_data))  # 30 minutes TTL
    
    # Seed trending posts
    print("Seeding trending posts...")
    trending_posts = []
    for i in range(10):
        trending_posts.append({
            "id": random.randint(1, 1000),
            "score": random.randint(100, 10000)
        })
    trending_posts.sort(key=lambda x: x["score"], reverse=True)
    
    key = trending_posts_key()
    r.setex(key, 300, json.dumps(trending_posts))  # 5 minutes TTL
    
    # Seed rate limiting data
    print("Seeding rate limiting data...")
    for i in range(1, 51):
        # Simulate some rate limiting data
        for action in ["post", "like", "follow", "comment"]:
            key = rate_limit_key(i, action)
            # Add some random timestamps for rate limiting
            for j in range(random.randint(0, 5)):
                timestamp = int((datetime.now() - timedelta(minutes=random.randint(0, 59))).timestamp())
                r.zadd(key, {str(timestamp): timestamp})
            r.expire(key, 3600)  # 1 hour TTL
    
    # Seed feed cache data
    print("Seeding feed cache...")
    for i in range(1, 101):
        # Create multiple feed cache entries per user
        for j in range(3):
            feed_items = []
            for k in range(20):
                feed_items.append({
                    "id": random.randint(1, 1000),
                    "author_id": random.randint(1, 100),
                    "content": f"Feed item {k} for user {i}",
                    "created_at": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat()
                })
            
            cursor = f"cursor_{j}" if j > 0 else "initial"
            key = user_feed_key(i, cursor)
            feed_data = {
                "items": feed_items,
                "next_cursor": f"cursor_{j+1}" if j < 2 else None,
                "has_more": j < 2
            }
            r.setex(key, settings.cache_ttl_feed, json.dumps(feed_data))
    
    # Seed explore feed cache
    print("Seeding explore feed cache...")
    for i in range(0, 1000, 20):
        feed_items = []
        for j in range(20):
            feed_items.append({
                "id": i + j + 1,
                "author_id": random.randint(1, 100),
                "content": f"Explore feed item {i + j + 1}",
                "likes_count": random.randint(0, 1000),
                "created_at": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat()
            })
        
        key = explore_feed_key(i)
        feed_data = {
            "items": feed_items,
            "next_cursor": str(i + 20) if i + 20 < 1000 else None,
            "has_more": i + 20 < 1000
        }
        r.setex(key, settings.cache_ttl_feed, json.dumps(feed_data))
    
    print("✅ Redis seeding completed!")

def clear_redis():
    """Clear all test data from Redis"""
    r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    
    # Get all keys matching our patterns
    patterns = [
        "user_profile:*",
        "post:*",
        "trending_posts",
        "rate_limit:*",
        "user_feed:*",
        "explore_feed:*"
    ]
    
    total_deleted = 0
    for pattern in patterns:
        keys = r.keys(pattern)
        if keys:
            r.delete(*keys)
            total_deleted += len(keys)
    
    print(f"🗑️  Cleared {total_deleted} keys from Redis")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_redis()
    else:
        seed_redis()