import pytest
from app.schemas.submission import SubmissionCreate, SubmissionUpdate
from app.services.submission_service import SubmissionService
from app.db.models import Submission

def test_submission_create():
    """
    Test creating a submission
    """
    submission_data = SubmissionCreate(
        prompt_id=1,
        user_id=1,
        diagram_data="graph TD\nA[Client] --> B[Server]",
        explanation="A simple client-server architecture"
    )
    
    # In a real test, you would mock the database session
    # and verify the submission is created correctly
    assert submission_data.prompt_id == 1
    assert "client-server" in submission_data.explanation.lower()

def test_submission_update():
    """
    Test updating a submission
    """
    submission_update = SubmissionUpdate(
        diagram_data="graph TD\nA[Client] --> B[Load Balancer]\nB --> C[Server 1]\nB --> D[Server 2]"
    )
    
    update_data = submission_update.dict(exclude_unset=True)
    assert "diagram_data" in update_data
    assert "Server 2" in update_data["diagram_data"]
    assert "explanation" not in update_data

if __name__ == "__main__":
    pytest.main()