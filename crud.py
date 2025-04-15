from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

def get_intern(db: Session, intern_id: int):
    return db.query(models.Intern).filter(models.Intern.id == intern_id).first()

def get_intern_by_email(db: Session, email: str):
    return db.query(models.Intern).filter(models.Intern.email == email).first()

def create_intern(db: Session, intern: schemas.InternCreate):
    db_intern = models.Intern(name=intern.name, email=intern.email)
    db.add(db_intern)
    db.commit()
    db.refresh(db_intern)
    return db_intern

def get_attendance_by_intern_and_date(db: Session, intern_id: int, date: datetime):
    return db.query(models.Attendance).filter(
        models.Attendance.intern_id == intern_id,
        models.Attendance.date == date
    ).first()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(
        intern_id=attendance.intern_id,
        date=attendance.date or datetime.utcnow(),
        time_in=attendance.time_in,
        time_out=attendance.time_out
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance_time_in(db: Session, attendance: models.Attendance, time_in: datetime):
    attendance.time_in = time_in
    db.commit()
    db.refresh(attendance)
    return attendance

def update_attendance_time_out(db: Session, attendance: models.Attendance, time_out: datetime):
    attendance.time_out = time_out
    db.commit()
    db.refresh(attendance)
    return attendance

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        intern_id=task.intern_id,
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def mark_task_completed(db: Session, task: models.Task):
    task.completed = True
    db.commit()
    db.refresh(task)
    return task

def get_intern_tasks(db: Session, intern_id: int):
    return db.query(models.Task).filter(models.Task.intern_id == intern_id).all()

def get_intern_attendance(db: Session, intern_id: int):
    return db.query(models.Attendance).filter(models.Attendance.intern_id == intern_id).all()
