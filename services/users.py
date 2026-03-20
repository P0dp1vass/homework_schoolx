from fastapi import Depends
from sqlalchemy.orm import Session

from repositories.users import UserRepository
from schemas.users import UserRegistrationSchema, UserLoginSchema
from core.security import hash_password, verify_password, create_access_token
from core.exceptions import UserAlreadyExistsException, AppException, ErrorCode

class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repo = repository

    def register(self, user_in: UserRegistrationSchema):
        if self.repo.get_by_email(user_in.email):
            raise UserAlreadyExistsException(field="email", value=user_in.email)
        
        hashed_pwd = hash_password(user_in.password)
        new_user = self.repo.create(user_in, hashed_pwd)
        return new_user

    def authenticate(self, user_in: UserLoginSchema):
        user = self.repo.get_by_email(user_in.email)
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise AppException(
                status_code=401,
                error_code=ErrorCode.INVALID_CREDENTIALS,
                message="Не верные данные для входа"
            )
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def get_user_by_email(self, email: str):
        return self.repo.get_by_email(email)
