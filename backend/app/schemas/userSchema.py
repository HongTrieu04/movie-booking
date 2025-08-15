from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

class UserResponse(UserBase):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    phone: str
    password: str

class UserGet(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str

    class Config:
        from_attributes = True