from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Prompt
from app.schemas.prompt import PromptCreate, PromptUpdate
from app.errors import PromptNotFoundError

class PromptService:
    @staticmethod
    async def get_prompt(db: AsyncSession, prompt_id: int) -> Prompt:
        result = await db.execute(select(Prompt).where(Prompt.id == prompt_id))
        prompt = result.scalar_one_or_none()
        if not prompt:
            raise PromptNotFoundError(prompt_id)
        return prompt

    @staticmethod
    async def get_prompts(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Prompt]:
        result = await db.execute(select(Prompt).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_prompt(db: AsyncSession, prompt: PromptCreate) -> Prompt:
        db_prompt = Prompt(**prompt.dict())
        db.add(db_prompt)
        await db.commit()
        await db.refresh(db_prompt)
        return db_prompt

    @staticmethod
    async def update_prompt(db: AsyncSession, prompt_id: int, prompt_update: PromptUpdate) -> Prompt:
        db_prompt = await PromptService.get_prompt(db, prompt_id)
        update_data = prompt_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prompt, key, value)
        await db.commit()
        await db.refresh(db_prompt)
        return db_prompt

    @staticmethod
    async def delete_prompt(db: AsyncSession, prompt_id: int) -> bool:
        db_prompt = await PromptService.get_prompt(db, prompt_id)
        await db.delete(db_prompt)
        await db.commit()
        return True