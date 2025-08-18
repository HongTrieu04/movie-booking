from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Schema cho request login truyền thống (DB)."""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Schema cho response login thành công."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str

class RegisterResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: str