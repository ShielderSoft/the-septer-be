from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    Hunter = "Hunter"
    Guardian = "Guardian"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.Hunter


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: UserRole

    class Config:
        orm_mode = True


class GeminiKeyAdd(BaseModel):
    api_key: str

class GuardianLogin(BaseModel):
    email: EmailStr
    password: str