from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class Role(str, Enum):
    user = "user"
    admin = "admin"

class Permission(str, Enum):
    success = True
    fail = False

class Password(BaseModel):
    password: str = "12345"

class UserBase(BaseModel):
    email: EmailStr = "test@mail.ru"

class UserAuth(Password, UserBase):
    pass

class ID(BaseModel):
    id: str

class UserVerify(ID):
    role: Role