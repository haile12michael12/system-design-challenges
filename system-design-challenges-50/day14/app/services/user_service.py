from typing import List, Optional
from datetime import datetime

class User:
    def __init__(self, id: int, username: str, email: str, full_name: str):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class UserService:
    def __init__(self):
        # In a real implementation, this would be a database
        self.users = {}
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List all users"""
        users = list(self.users.values())
        return users[skip : skip + limit]
    
    def create_user(self, username: str, email: str, full_name: str, password: str) -> User:
        """Create a new user"""
        user_id = len(self.users) + 1
        user = User(user_id, username, email, full_name)
        self.users[user_id] = user
        return user
    
    def update_user(self, user_id: int, username: str = None, email: str = None, 
                   full_name: str = None) -> Optional[User]:
        """Update a user"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if full_name is not None:
            user.full_name = full_name
        
        user.updated_at = datetime.now()
        return user
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        user.is_active = False
        user.updated_at = datetime.now()
        return user