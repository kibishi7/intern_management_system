from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Intern(Base):
    __tablename__ = "interns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="intern")
    attendances = relationship("Attendance", back_populates="intern")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    intern_id = Column(Integer, ForeignKey("interns.id"))
    date = Column(DateTime, default=datetime.utcnow)
    time_in = Column(DateTime, nullable=True)
    time_out = Column(DateTime, nullable=True)

    intern = relationship("Intern", back_populates="attendances")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    intern_id = Column(Integer, ForeignKey("interns.id"))
    completed = Column(Boolean, default=False)

    intern = relationship("Intern", back_populates="tasks")
