from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class SuperAdminCreate(BaseModel):
    email: EmailStr
    password: str
    profileImageURL: Optional[str] = None
    fullName: str
    role: str = "super_admin"

class SuperAdminResponse(BaseModel):
    id: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    createdAt: datetime
    fullName: str
    lastLogin: Optional[datetime] = None
    role: str

    class Config:
        orm_mode = True
