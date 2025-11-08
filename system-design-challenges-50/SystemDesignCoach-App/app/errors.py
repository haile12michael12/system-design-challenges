from fastapi import HTTPException, status

class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFoundError(CustomException):
    def __init__(self, user_id: int):
        super().__init__(detail=f"User with id {user_id} not found", status_code=status.HTTP_404_NOT_FOUND)

class PromptNotFoundError(CustomException):
    def __init__(self, prompt_id: int):
        super().__init__(detail=f"Prompt with id {prompt_id} not found", status_code=status.HTTP_404_NOT_FOUND)

class SubmissionNotFoundError(CustomException):
    def __init__(self, submission_id: int):
        super().__init__(detail=f"Submission with id {submission_id} not found", status_code=status.HTTP_404_NOT_FOUND)

class GradingNotFoundError(CustomException):
    def __init__(self, grading_id: int):
        super().__init__(detail=f"Grading with id {grading_id} not found", status_code=status.HTTP_404_NOT_FOUND)

class DatabaseConnectionError(CustomException):
    def __init__(self, detail: str = "Database connection error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)