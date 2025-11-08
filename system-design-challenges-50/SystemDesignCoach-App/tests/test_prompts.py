import pytest
from app.schemas.prompt import PromptCreate, PromptUpdate
from app.services.prompt_service import PromptService
from app.db.models import Prompt

def test_prompt_create():
    """
    Test creating a prompt
    """
    prompt_data = PromptCreate(
        title="Test Prompt",
        description="A test prompt for system design",
        difficulty="intermediate"
    )
    
    # In a real test, you would mock the database session
    # and verify the prompt is created correctly
    assert prompt_data.title == "Test Prompt"
    assert prompt_data.difficulty == "intermediate"

def test_prompt_update():
    """
    Test updating a prompt
    """
    prompt_update = PromptUpdate(
        title="Updated Prompt Title"
    )
    
    update_data = prompt_update.dict(exclude_unset=True)
    assert "title" in update_data
    assert update_data["title"] == "Updated Prompt Title"
    assert "description" not in update_data

if __name__ == "__main__":
    pytest.main()