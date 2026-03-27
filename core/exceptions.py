from fastapi import HTTPException
from enum import Enum
from typing import Optional, Dict, Any

class ErrorCode(Enum):
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    COMMENT_NOT_FOUND = "COMMENT_NOT_FOUND"

    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class AppException(HTTPException):
    def __init__(
            self,
            status_code: int,
            error_code: ErrorCode,
            message: str,
            field: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "code": error_code.value,
                "message": message,
                "field": field,
                "details": details or {}
            }
        )

class TaskNotFoundException(AppException):
    def __init__(self, task_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.TASK_NOT_FOUND,
            message=f"Task with ID {task_id} not found",
            details={"task_id": task_id}
        )

class CommentNotFoundException(AppException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.COMMENT_NOT_FOUND,
            message=f"Comment with ID {comment_id} not found",
            details={"comment_id": comment_id}
        )

class UserNotFoundException(AppException):
    def __init__(self, email: str):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.USER_NOT_FOUND,
            message=f"User with email {email} not found",
            details={"email": email}
        )

class UserAlreadyExistsException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=400,
            error_code=ErrorCode.USER_ALREADY_EXISTS,
            message=f"User with {field} '{value}' already exists",
            field=field,
            details={field: value}
        )
