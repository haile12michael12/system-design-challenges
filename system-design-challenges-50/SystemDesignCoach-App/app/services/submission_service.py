from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Submission
from app.schemas.submission import SubmissionCreate, SubmissionUpdate
from app.errors import SubmissionNotFoundError

class SubmissionService:
    @staticmethod
    async def get_submission(db: AsyncSession, submission_id: int) -> Submission:
        result = await db.execute(select(Submission).where(Submission.id == submission_id))
        submission = result.scalar_one_or_none()
        if not submission:
            raise SubmissionNotFoundError(submission_id)
        return submission

    @staticmethod
    async def get_submissions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Submission]:
        result = await db.execute(select(Submission).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_submission(db: AsyncSession, submission: SubmissionCreate) -> Submission:
        db_submission = Submission(**submission.dict())
        db.add(db_submission)
        await db.commit()
        await db.refresh(db_submission)
        return db_submission

    @staticmethod
    async def update_submission(db: AsyncSession, submission_id: int, submission_update: SubmissionUpdate) -> Submission:
        db_submission = await SubmissionService.get_submission(db, submission_id)
        update_data = submission_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_submission, key, value)
        await db.commit()
        await db.refresh(db_submission)
        return db_submission

    @staticmethod
    async def delete_submission(db: AsyncSession, submission_id: int) -> bool:
        db_submission = await SubmissionService.get_submission(db, submission_id)
        await db.delete(db_submission)
        await db.commit()
        return True