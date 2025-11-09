from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

class UserSignup(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example":{
                "email": "user@example.com",
                "full_name": "Иван Иванов",
                "password": "password"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example":{
                "email": "user@example.com",
                "password": "password"
            }
        }

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_atributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

