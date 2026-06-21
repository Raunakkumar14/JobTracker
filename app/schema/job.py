from datetime import date
from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    company: str
    status: str = "open"
    description: Optional[str] = None
    location: Optional[str] = None
    deadline: Optional[date] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    deadline: Optional[date] = None


class JobOut(JobBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True