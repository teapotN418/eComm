from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class Role(str, Enum):
    user = "user"
    admin = "admin"

class Password(BaseModel):
    password: str = Field(min_length=5, default="12345")

class UserBase(BaseModel):
    email: EmailStr = "test@mail.ru"

class UserAuth(Password, UserBase):
    pass

class UserCreate(UserAuth):
    role: Role = Role.user

class UserShow(UserBase):
    role: Role
    id: int