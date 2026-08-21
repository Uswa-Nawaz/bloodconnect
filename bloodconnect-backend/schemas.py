from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserSignupRequest(BaseModel):
    role: str
    name: str
    email: EmailStr
    phone: str
    password: str
    blood_type: Optional[str] = None
    date_of_birth: Optional[datetime] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    role: str
    name: str
    email: EmailStr
    phone: str
    status: str
    blood_type: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True