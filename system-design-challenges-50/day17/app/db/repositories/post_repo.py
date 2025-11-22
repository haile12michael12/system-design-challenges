from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models import Post, FeedEntry


class PostRepository:
    """Repository for Post operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_post(self, user_id: int, content: str) -> Post:
        """Create a new post."""
        post = Post(user_id=user_id, content=content)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """Get a post by ID."""
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_posts_by_user(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Post]:
        """Get posts by user."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id, Post.is_deleted == False)
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post (soft delete)."""
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.is_deleted = True
            self.db.commit()
            return True
        return False
    
    def get_feed_posts(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Post]:
        """Get posts for a user's feed."""
        return (
            self.db.query(Post)
            .join(FeedEntry, FeedEntry.post_id == Post.id)
            .filter(FeedEntry.user_id == user_id, Post.is_deleted == False)
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )