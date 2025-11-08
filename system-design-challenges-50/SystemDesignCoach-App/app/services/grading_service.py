from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Grading
from app.schemas.grading import GradingCreate, GradingUpdate
from app.errors import GradingNotFoundError

class GradingService:
    @staticmethod
    async def get_grading(db: AsyncSession, grading_id: int) -> Grading:
        result = await db.execute(select(Grading).where(Grading.id == grading_id))
        grading = result.scalar_one_or_none()
        if not grading:
            raise GradingNotFoundError(grading_id)
        return grading

    @staticmethod
    async def get_gradings(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Grading]:
        result = await db.execute(select(Grading).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_grading(db: AsyncSession, grading: GradingCreate) -> Grading:
        db_grading = Grading(**grading.dict())
        db.add(db_grading)
        await db.commit()
        await db.refresh(db_grading)
        return db_grading

    @staticmethod
    async def update_grading(db: AsyncSession, grading_id: int, grading_update: GradingUpdate) -> Grading:
        db_grading = await GradingService.get_grading(db, grading_id)
        update_data = grading_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_grading, key, value)
        await db.commit()
        await db.refresh(db_grading)
        return db_grading

    @staticmethod
    async def delete_grading(db: AsyncSession, grading_id: int) -> bool:
        db_grading = await GradingService.get_grading(db, grading_id)
        await db.delete(db_grading)
        await db.commit()
        return True