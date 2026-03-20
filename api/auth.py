from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from schemas.users import UserRegistrationSchema, UserLoginSchema, UserInfoSchema, AccessTokenSchema
from services.users import UserService
from dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInfoSchema, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegistrationSchema, service: UserService = Depends()):
    new_user = service.register(user_in)
    return new_user

@router.post("/login", response_model=AccessTokenSchema, status_code=status.HTTP_200_OK)
def login(response: Response, user_in: UserLoginSchema, service: UserService = Depends()):
    token_data = service.authenticate(user_in)
    response.set_cookie(key="access_token", value=token_data["access_token"], httponly=True)
    return token_data

@router.get("/test")
def protect_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}, auth works!"}
