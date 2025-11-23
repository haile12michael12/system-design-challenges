from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Post(BaseModel):
    __tablename__ = "posts"
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    media_url = Column(String(255), nullable=True)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    
    # Indexes
    __table_args__ = (
        Index('idx_posts_author_id', 'author_id'),
        Index('idx_posts_created_at', 'created_at'),
    )

# Add back_populates to User model
from app.models.user import User
User.posts = relationship("Post", back_populates="author")