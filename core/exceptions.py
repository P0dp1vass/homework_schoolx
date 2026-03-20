from fastapi import HTTPException
from enum import Enum
from typing import Optional, Dict, Any

class ErrorCode(Enum):
    """Коды всех возможных ошибок в приложении"""
    # Задачи
    TASK_NOT_FOUND = "TASK_NOT_FOUND"

    # Пользователи
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    # Общие
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class AppException(HTTPException):
    """Базовый класс для всех кастомных исключений"""
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
            message=f"Задача с идентификатором {task_id} не найдена",
            details={"task_id": task_id}
        )

class UserNotFoundException(AppException):
    def __init__(self, email: str):
        super().__init__(
            status_code=404,
            error_code=ErrorCode.USER_NOT_FOUND,
            message=f"Пользователь {email} не найден",
            details={"email": email}
        )

class UserAlreadyExistsException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=400,
            error_code=ErrorCode.USER_ALREADY_EXISTS,
            message=f"Пользователь с {field} '{value}' уже существует",
            field=field,
            details={field: value}
        )
