from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserInfoSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str
