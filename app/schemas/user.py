from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from datetime import datetime

# class UserBase(BaseModel):
#     username: str
#     name: str
#     email: EmailStr
#     status: str
#     # pelanggan_id: Optional[int] = None
#     role_id: int
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)  # Validasi panjang username
    name: constr(min_length=3, max_length=100)     # Validasi panjang nama
    email: EmailStr
    pelanggan_id: Optional[int] = None
    status: constr(pattern="^(active|inactive)$") = Field(default="inactive")  # Hanya terima active/inactive
    role_id: int = Field(default=4)  # Default role_id untuk user biasa

class UserCreate(UserBase):
    password: constr(min_length=8)  # Minimal 8 karakter untuk password

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     status: Optional[str] = None
#     password: Optional[str] = None
#     # pelanggan_id: Optional[int] = None
#     role_id: Optional[int] = None
class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    name: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    status: Optional[constr(pattern="^(active|inactive)$")] = None
    password: Optional[constr(min_length=8)] = None
    role_id: Optional[int] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str  # This will be the hashed password

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int  # user id
    exp: datetime

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: str
    role: dict
    status: str
    created_at: datetime
    updated_at: datetime 