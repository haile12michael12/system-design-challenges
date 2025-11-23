#!/usr/bin/env python3

"""
Script to generate fake data for testing and development
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

def generate_fake_users(count: int = 100) -> List[Dict[str, Any]]:
    """Generate fake user data"""
    users = []
    for i in range(count):
        username = f"user_{i}_{random_string(5)}"
        users.append({
            "id": i + 1,
            "username": username,
            "email": f"{username}@example.com",
            "hashed_password": f"hashed_password_{random_string(20)}",
            "is_active": True,
            "is_superuser": i < 5,  # First 5 users are superusers
            "bio": f"This is the bio for user {username}",
            "created_at": random_past_date(),
            "updated_at": random_past_date()
        })
    return users

def generate_fake_posts(users: List[Dict[str, Any]], count: int = 1000) -> List[Dict[str, Any]]:
    """Generate fake post data"""
    posts = []
    for i in range(count):
        author = random.choice(users)
        content = f"This is post #{i+1} by {author['username']}. {random_string(100)}"
        
        posts.append({
            "id": i + 1,
            "author_id": author["id"],
            "content": content,
            "media_url": f"https://example.com/media/{random_string(10)}.jpg" if random.random() > 0.7 else None,
            "likes_count": random.randint(0, 1000),
            "comments_count": random.randint(0, 100),
            "created_at": random_past_date(),
            "updated_at": random_past_date()
        })
    return posts

def generate_fake_feed_cache(users: List[Dict[str, Any]], count: int = 500) -> List[Dict[str, Any]]:
    """Generate fake feed cache data"""
    feed_cache = []
    for i in range(count):
        user = random.choice(users)
        cache_key = f"user_feed:{user['id']}:{random_string(10)}"
        
        feed_cache.append({
            "id": i + 1,
            "user_id": user["id"],
            "feed_data": json.dumps([{"id": j, "content": f"Feed item {j}"} for j in range(10)]),
            "cache_key": cache_key,
            "expires_at": (datetime.now() + timedelta(hours=random.randint(1, 24))).isoformat(),
            "created_at": random_past_date(),
            "updated_at": random_past_date()
        })
    return feed_cache

def generate_fake_metadata_rollup(count: int = 1000) -> List[Dict[str, Any]]:
    """Generate fake metadata rollup data"""
    rollups = []
    entity_types = ["user", "post", "feed"]
    metric_names = ["views", "likes", "comments", "shares", "engagement_rate"]
    rollup_periods = ["hourly", "daily", "weekly"]
    
    for i in range(count):
        rollups.append({
            "id": i + 1,
            "entity_type": random.choice(entity_types),
            "entity_id": random.randint(1, 1000),
            "metric_name": random.choice(metric_names),
            "metric_value": random.randint(0, 10000),
            "rollup_period": random.choice(rollup_periods),
            "timestamp": random_past_date(),
            "created_at": random_past_date(),
            "updated_at": random_past_date()
        })
    return rollups

def random_string(length: int) -> str:
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_past_date() -> str:
    """Generate a random date in the past year"""
    days_ago = random.randint(0, 365)
    return (datetime.now() - timedelta(days=days_ago)).isoformat()

def main():
    """Generate all fake data and save to files"""
    print("Generating fake data...")
    
    # Generate users
    users = generate_fake_users(100)
    with open("fake_users.json", "w") as f:
        json.dump(users, f, indent=2)
    print(f"Generated {len(users)} users")
    
    # Generate posts
    posts = generate_fake_posts(users, 1000)
    with open("fake_posts.json", "w") as f:
        json.dump(posts, f, indent=2)
    print(f"Generated {len(posts)} posts")
    
    # Generate feed cache
    feed_cache = generate_fake_feed_cache(users, 500)
    with open("fake_feed_cache.json", "w") as f:
        json.dump(feed_cache, f, indent=2)
    print(f"Generated {len(feed_cache)} feed cache entries")
    
    # Generate metadata rollup
    metadata_rollup = generate_fake_metadata_rollup(1000)
    with open("fake_metadata_rollup.json", "w") as f:
        json.dump(metadata_rollup, f, indent=2)
    print(f"Generated {len(metadata_rollup)} metadata rollup entries")
    
    print("✅ Fake data generation complete!")

if __name__ == "__main__":
    main()