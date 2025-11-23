from app.models.post import Post
from sqlalchemy.orm import Session
from typing import Optional

def create_post(db: Session, post_data: dict, author_id: int) -> Post:
    """Create a new post"""
    post = Post(
        author_id=author_id,
        content=post_data.get("content", ""),
        media_url=post_data.get("media_url")
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Get a post by ID"""
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post_data: dict, author_id: int) -> Optional[Post]:
    """Update a post"""
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == author_id).first()
    if not post:
        return None
    
    if "content" in post_data:
        post.content = post_data["content"]
    if "media_url" in post_data:
        post.media_url = post_data["media_url"]
    
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, author_id: int) -> bool:
    """Delete a post"""
    post = db.query(Post).filter(Post.id == post_id, Post.author_id == author_id).first()
    if not post:
        return False
    
    db.delete(post)
    db.commit()
    return True