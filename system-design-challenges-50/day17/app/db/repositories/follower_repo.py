from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from ..models import Follow, User
from ...domain.entities.user_entity import UserEntity


class FollowerRepository:
    """Repository for Follower operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_followers(self, user_id: str) -> List[UserEntity]:
        """
        Get followers of a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[UserEntity]: List of followers
        """
        db_followers = (
            self.db.query(User)
            .join(Follow, Follow.follower_id == User.id)
            .filter(Follow.followed_id == uuid.UUID(user_id))
            .all()
        )
        return [UserEntity.from_orm(user) for user in db_followers]
    
    def get_following(self, user_id: str) -> List[UserEntity]:
        """
        Get users that a user is following.
        
        Args:
            user_id: User ID
            
        Returns:
            List[UserEntity]: List of users being followed
        """
        db_following = (
            self.db.query(User)
            .join(Follow, Follow.followed_id == User.id)
            .filter(Follow.follower_id == uuid.UUID(user_id))
            .all()
        )
        return [UserEntity.from_orm(user) for user in db_following]
    
    def is_following(self, follower_id: str, followed_id: str) -> bool:
        """
        Check if a user is following another user.
        
        Args:
            follower_id: ID of the user who might be following
            followed_id: ID of the user who might be followed
            
        Returns:
            bool: True if following, False otherwise
        """
        follow = self.db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(follower_id),
            Follow.followed_id == uuid.UUID(followed_id)
        ).first()
        return follow is not None
    
    def get_follower_count(self, user_id: str) -> int:
        """
        Get the number of followers for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of followers
        """
        return self.db.query(Follow).filter(Follow.followed_id == uuid.UUID(user_id)).count()
    
    def get_following_count(self, user_id: str) -> int:
        """
        Get the number of users a user is following.
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of users being followed
        """
        return self.db.query(Follow).filter(Follow.follower_id == uuid.UUID(user_id)).count()