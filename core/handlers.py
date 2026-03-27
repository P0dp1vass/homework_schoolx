from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from core.exceptions import AppException, ErrorCode
from typing import Dict
import traceback

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
            headers=get_error_headers(exc.status_code)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            loc_path = error.get("loc", [])
            field = ".".join(str(loc) for loc in loc_path[1:]) if len(loc_path) > 1 else str(loc_path[0]) if loc_path else None
            errors.append({
                "code": ErrorCode.VALIDATION_ERROR.value,
                "message": error.get("msg"),
                "field": field,
                "details": {"type": error.get("type")}
            })

        return JSONResponse(
            status_code=422,
            content={"errors": errors},
            headers=get_error_headers(422)
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        error_msg = str(exc.orig)
        field = "unknown"

        if "email" in error_msg.lower():
            field = "email"

        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": ErrorCode.USER_ALREADY_EXISTS.value,
                    "message": "Resource with such data already exists",
                    "field": field,
                    "details": {"constraint": error_msg}
                }
            },
            headers=get_error_headers(400)
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exc: Exception):
        print("=" * 50)
        print(f"UNEXPECTED ERROR: {exc}")
        print(traceback.format_exc())
        print("=" * 50)

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": ErrorCode.INTERNAL_SERVER_ERROR.value,
                    "message": "Internal server error",
                    "field": None,
                    "details": traceback.format_exc()
                }
            },
            headers=get_error_headers(500)
        )

def get_error_headers(status_code: int) -> Dict[str, str]:
    headers = {}
    if status_code == 401:
        headers["WWW-Authenticate"] = 'Bearer realm="api"'
    return headers
