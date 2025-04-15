from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceBase(BaseModel):
    date: Optional[datetime] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None

class AttendanceCreate(AttendanceBase):
    intern_id: int

class Attendance(AttendanceBase):
    id: int
    intern_id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    intern_id: int

class Task(TaskBase):
    id: int
    intern_id: int
    completed: bool

    class Config:
        orm_mode = True

class InternBase(BaseModel):
    name: str
    email: str

class InternCreate(InternBase):
    pass

class Intern(InternBase):
    id: int
    tasks: list[Task] = []
    attendances: list[Attendance] = []

    class Config:
        orm_mode = True
