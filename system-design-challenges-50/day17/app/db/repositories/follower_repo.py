from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models import Follower, User


class FollowerRepository:
    """Repository for Follower operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def follow_user(self, follower_id: int, followee_id: int) -> Follower:
        """Create a follow relationship."""
        follower = Follower(
            follower_id=follower_id,
            followee_id=followee_id
        )
        self.db.add(follower)
        self.db.commit()
        self.db.refresh(follower)
        return follower
    
    def unfollow_user(self, follower_id: int, followee_id: int) -> bool:
        """Remove a follow relationship."""
        follower = (
            self.db.query(Follower)
            .filter(
                Follower.follower_id == follower_id,
                Follower.followee_id == followee_id
            )
            .first()
        )
        
        if follower:
            self.db.delete(follower)
            self.db.commit()
            return True
        return False
    
    def get_followers(self, user_id: int) -> List[User]:
        """Get followers of a user."""
        return (
            self.db.query(User)
            .join(Follower, Follower.follower_id == User.id)
            .filter(Follower.followee_id == user_id)
            .all()
        )
    
    def get_following(self, user_id: int) -> List[User]:
        """Get users that a user is following."""
        return (
            self.db.query(User)
            .join(Follower, Follower.followee_id == User.id)
            .filter(Follower.follower_id == user_id)
            .all()
        )