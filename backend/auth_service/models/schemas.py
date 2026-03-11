from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

Role = Literal["patient", "doctor", "lab", "pharmacy", "admin"]


class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role
    created_at: datetime


class HealthResponse(BaseModel):
    service: str
    status: str
