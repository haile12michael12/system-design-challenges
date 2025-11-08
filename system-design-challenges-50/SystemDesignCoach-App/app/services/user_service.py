from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.errors import UserNotFoundError

class UserService:
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(user_id)
        return user

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(username)
        return user

    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password  # In practice, hash the password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
        db_user = await UserService.get_user(db, user_id)
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        db_user = await UserService.get_user(db, user_id)
        await db.delete(db_user)
        await db.commit()
        return True