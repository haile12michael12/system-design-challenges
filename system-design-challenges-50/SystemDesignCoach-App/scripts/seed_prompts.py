#!/usr/bin/env python3
"""
Seed the database with initial prompts
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.db.session import get_db_session
from app.db.models import Prompt
from app.schemas.prompt import PromptCreate
from app.services.prompt_service import PromptService

async def seed_prompts():
    """
    Seed the database with initial prompts
    """
    prompts_data = [
        {
            "title": "Design a URL Shortening Service",
            "description": "Create a service that takes long URLs and shortens them.",
            "difficulty": "intermediate"
        },
        {
            "title": "Design a Chat Application",
            "description": "Build a real-time chat application supporting multiple users.",
            "difficulty": "advanced"
        },
        {
            "title": "Design a File Storage Service",
            "description": "Create a service for storing and retrieving files with metadata.",
            "difficulty": "intermediate"
        },
        {
            "title": "Design a News Feed System",
            "description": "Build a system that shows personalized news feeds to users.",
            "difficulty": "advanced"
        }
    ]
    
    async for db in get_db_session():
        for prompt_data in prompts_data:
            prompt_create = PromptCreate(**prompt_data)
            prompt = await PromptService.create_prompt(db, prompt_create)
            print(f"Created prompt: {prompt.title}")
        break  # Exit the async generator
    
    print("Prompts seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_prompts())