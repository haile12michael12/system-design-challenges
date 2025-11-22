#!/usr/bin/env python3

"""
Script to seed the database with initial data
"""

import asyncio
import logging
from datetime import datetime

from app.db.session import init_db
from app.db.models import User, Post
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate
from app.services.user_service import UserService
from app.services.post_service import PostService

logger = logging.getLogger(__name__)


async def seed_users(user_service: UserService) -> list:
    """Seed the database with initial users"""
    users_data = [
        UserCreate(
            username="alice",
            email="alice@example.com",
            full_name="Alice Smith",
            bio="Software engineer and tech enthusiast",
            password="password123"
        ),
        UserCreate(
            username="bob",
            email="bob@example.com",
            full_name="Bob Johnson",
            bio="Digital artist and photographer",
            password="password123"
        ),
        UserCreate(
            username="charlie",
            email="charlie@example.com",
            full_name="Charlie Brown",
            bio="Data scientist and machine learning researcher",
            password="password123"
        )
    ]
    
    users = []
    for user_data in users_data:
        try:
            user = await user_service.create_user(user_data)
            users.append(user)
            logger.info(f"Created user: {user.username}")
        except Exception as e:
            logger.error(f"Error creating user {user_data.username}: {e}")
    
    return users


async def seed_posts(post_service: PostService, users: list) -> list:
    """Seed the database with initial posts"""
    posts_data = [
        {
            "content": "Just finished working on an exciting new project! Can't wait to share it with everyone.",
            "author_id": users[0].id
        },
        {
            "content": "Beautiful sunset from my evening walk today. Nature never fails to inspire me.",
            "author_id": users[1].id,
            "media_url": "https://example.com/sunset.jpg"
        },
        {
            "content": "Reading an interesting paper on neural networks and their applications in computer vision.",
            "author_id": users[2].id
        },
        {
            "content": "Working from home has its perks - fresh coffee and no commute!",
            "author_id": users[0].id
        },
        {
            "content": "Just published a new artwork. Check out my latest digital painting!",
            "author_id": users[1].id,
            "media_url": "https://example.com/artwork.jpg"
        }
    ]
    
    posts = []
    for post_data in posts_data:
        try:
            post_create = PostCreate(
                content=post_data["content"],
                media_url=post_data.get("media_url")
            )
            post = await post_service.create_post(post_create, post_data["author_id"])
            posts.append(post)
            logger.info(f"Created post: {post.id}")
        except Exception as e:
            logger.error(f"Error creating post: {e}")
    
    return posts


async def main():
    """Main function to seed the database"""
    logger.info("Starting database seeding...")
    
    try:
        # Initialize database
        init_db()
        
        # Initialize services
        user_service = UserService()
        post_service = PostService()
        
        # Seed users
        users = await seed_users(user_service)
        
        # Seed posts
        posts = await seed_posts(post_service, users)
        
        logger.info(f"Database seeding completed! Created {len(users)} users and {len(posts)} posts")
        
    except Exception as e:
        logger.error(f"Error during database seeding: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())