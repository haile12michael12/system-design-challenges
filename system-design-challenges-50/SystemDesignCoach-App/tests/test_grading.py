import pytest
from app.schemas.grading import GradingCreate, GradingUpdate
from app.services.grading_service import GradingService
from app.db.models import Grading

def test_grading_create():
    """
    Test creating a grading
    """
    grading_data = GradingCreate(
        submission_id=1,
        score=85.5,
        feedback="Good architecture design with clear components and relationships."
    )
    
    # In a real test, you would mock the database session
    # and verify the grading is created correctly
    assert grading_data.submission_id == 1
    assert grading_data.score == 85.5
    assert len(grading_data.feedback) > 0

def test_grading_update():
    """
    Test updating a grading
    """
    grading_update = GradingUpdate(
        score=92.0,
        feedback="Excellent design with well-defined components and clear relationships. Consider adding error handling."
    )
    
    update_data = grading_update.dict(exclude_unset=True)
    assert "score" in update_data
    assert update_data["score"] == 92.0
    assert "feedback" in update_data
    assert "error handling" in update_data["feedback"].lower()

if __name__ == "__main__":
    pytest.main()