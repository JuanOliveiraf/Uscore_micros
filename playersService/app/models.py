from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class PlayerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)
    position: Optional[str] = None
    team: Optional[str] = None
    active: bool = True


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    position: Optional[str] = None
    team: Optional[str] = None
    active: Optional[bool] = None


class PlayerInDB(PlayerBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class PlayerResponse(PlayerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
