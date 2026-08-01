from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==================================================
# User Schemas
# ==================================================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# ==================================================
# Admin Schemas
# ==================================================    
    
class AdminCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)


# ==================================================
# JWT Schemas
# ==================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ==================================================
# Note Schemas
# ==================================================

class NoteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    priority: int = Field(ge=1, le=3)


class NoteUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1)
    priority: Optional[int] = Field(default=None, ge=1, le=3)


class NoteResponse(BaseModel):
    id: int
    name: str
    description: str
    priority: int

    user_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class PaginatedNotes(BaseModel):
    total: int
    page: int
    limit: int
    items: list[NoteResponse]