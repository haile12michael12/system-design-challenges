from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from ..models import User, Follow
from ...domain.entities.user_entity import UserEntity


class UserRepository:
    """Repository for User operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: Dict[str, Any]) -> UserEntity:
        """
        Create a new user.
        
        Args:
            user_data: User data
            
        Returns:
            UserEntity: Created user
        """
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserEntity.from_orm(db_user)
    
    def get_user_by_id(self, user_id: str) -> Optional[UserEntity]:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserEntity: User or None if not found
        """
        db_user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        return UserEntity.from_orm(db_user) if db_user else None
    
    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        """
        Get a user by username.
        
        Args:
            username: Username
            
        Returns:
            UserEntity: User or None if not found
        """
        db_user = self.db.query(User).filter(User.username == username).first()
        return UserEntity.from_orm(db_user) if db_user else None
    
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Get a user by email.
        
        Args:
            email: Email
            
        Returns:
            UserEntity: User or None if not found
        """
        db_user = self.db.query(User).filter(User.email == email).first()
        return UserEntity.from_orm(db_user) if db_user else None
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[UserEntity]:
        """
        Update a user.
        
        Args:
            user_id: User ID
            user_data: User data to update
            
        Returns:
            UserEntity: Updated user or None if not found
        """
        db_user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
            return UserEntity.from_orm(db_user)
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
    
    def follow_user(self, follower_id: str, followed_id: str) -> bool:
        """
        Follow a user.
        
        Args:
            follower_id: ID of the user who wants to follow
            followed_id: ID of the user to be followed
            
        Returns:
            bool: True if followed, False if already following or error
        """
        # Check if already following
        existing_follow = self.db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(follower_id),
            Follow.followed_id == uuid.UUID(followed_id)
        ).first()
        
        if existing_follow:
            return False  # Already following
        
        # Create follow relationship
        follow = Follow(follower_id=uuid.UUID(follower_id), followed_id=uuid.UUID(followed_id))
        self.db.add(follow)
        self.db.commit()
        return True
    
    def unfollow_user(self, follower_id: str, followed_id: str) -> bool:
        """
        Unfollow a user.
        
        Args:
            follower_id: ID of the user who wants to unfollow
            followed_id: ID of the user to be unfollowed
            
        Returns:
            bool: True if unfollowed, False if not following or error
        """
        follow = self.db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(follower_id),
            Follow.followed_id == uuid.UUID(followed_id)
        ).first()
        
        if follow:
            self.db.delete(follow)
            self.db.commit()
            return True
        return False
    
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