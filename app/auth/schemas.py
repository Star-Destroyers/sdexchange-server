from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserDetail(BaseUser):
    id: int
    active: bool
    admin: bool
    superuser: bool
    last_login: Optional[datetime]


class UserUpdate(BaseUser):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class PasswordUpdate(BaseModel):
    password: constr(min_length=8)
    current_password: str
