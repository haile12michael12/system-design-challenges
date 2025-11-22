from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from ..models import Post, User
from ...domain.entities.post_entity import PostEntity


class PostRepository:
    """Repository for Post operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, post_data: Dict[str, Any]) -> PostEntity:
        """
        Create a new post.
        
        Args:
            post_data: Post data
            
        Returns:
            PostEntity: Created post
        """
        db_post = Post(**post_data)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return PostEntity.from_orm(db_post)
    
    def get_post_by_id(self, post_id: str) -> Optional[PostEntity]:
        """
        Get a post by ID.
        
        Args:
            post_id: Post ID
            
        Returns:
            PostEntity: Post or None if not found
        """
        db_post = self.db.query(Post).filter(Post.id == uuid.UUID(post_id)).first()
        return PostEntity.from_orm(db_post) if db_post else None
    
    def get_posts_by_user(self, user_id: str, limit: int = 10, offset: int = 0) -> List[PostEntity]:
        """
        Get posts by user.
        
        Args:
            user_id: User ID
            limit: Number of posts to return
            offset: Offset for pagination
            
        Returns:
            List[PostEntity]: List of posts
        """
        db_posts = (
            self.db.query(Post)
            .filter(Post.user_id == uuid.UUID(user_id))
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [PostEntity.from_orm(post) for post in db_posts]
    
    def get_feed_posts(self, user_id: str, limit: int = 10, offset: int = 0) -> List[PostEntity]:
        """
        Get feed posts for a user (posts from followed users).
        
        Args:
            user_id: User ID
            limit: Number of posts to return
            offset: Offset for pagination
            
        Returns:
            List[PostEntity]: List of posts
        """
        # This is a simplified version - in a real implementation, you would join with the follows table
        # to get posts from followed users
        db_posts = (
            self.db.query(Post)
            .join(User, Post.user_id == User.id)
            .filter(User.id == uuid.UUID(user_id))  # Simplified - should filter by followed users
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [PostEntity.from_orm(post) for post in db_posts]
    
    def delete_post(self, post_id: str) -> bool:
        """
        Delete a post.
        
        Args:
            post_id: Post ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_post = self.db.query(Post).filter(Post.id == uuid.UUID(post_id)).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False