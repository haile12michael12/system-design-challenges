"""
Sample Data Seeding
"""
from app.db.models import User, Post, Follow
from app.db.session import AsyncSessionLocal
import uuid

async def seed_data():
    """Seed database with sample data"""
    async with AsyncSessionLocal() as db:
        # Create sample users
        user1 = User(
            id="user1",
            username="alice",
            email="alice@example.com",
            password_hash="hashed_password_1"
        )
        
        user2 = User(
            id="user2",
            username="bob",
            email="bob@example.com",
            password_hash="hashed_password_2"
        )
        
        user3 = User(
            id="user3",
            username="charlie",
            email="charlie@example.com",
            password_hash="hashed_password_3"
        )
        
        # Add users to session
        db.add_all([user1, user2, user3])
        
        # Create sample posts
        post1 = Post(
            user_id="user1",
            caption="Beautiful sunset at the beach!",
            image_url="https://example.com/sunset.jpg"
        )
        
        post2 = Post(
            user_id="user2",
            caption="My new coffee setup",
            image_url="https://example.com/coffee.jpg"
        )
        
        post3 = Post(
            user_id="user1",
            caption="Hiking adventure",
            image_url="https://example.com/hiking.jpg"
        )
        
        # Add posts to session
        db.add_all([post1, post2, post3])
        
        # Create follow relationships
        follow1 = Follow(
            follower_id="user2",
            followed_id="user1"
        )
        
        follow2 = Follow(
            follower_id="user3",
            followed_id="user1"
        )
        
        follow3 = Follow(
            follower_id="user1",
            followed_id="user2"
        )
        
        # Add follows to session
        db.add_all([follow1, follow2, follow3])
        
        # Commit changes
        await db.commit()
        
        print("Sample data seeded successfully")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_data())