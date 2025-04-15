from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intern Management System")

# CORS middleware (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware for logging requests (optional)
@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url} - Status: {response.status_code}")
    return response

# Create intern
@app.post("/interns/", response_model=schemas.Intern)
def create_intern(intern: schemas.InternCreate, db: Session = Depends(get_db)):
    db_intern = crud.get_intern_by_email(db, email=intern.email)
    if db_intern:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_intern(db, intern=intern)

# Intern log time in
@app.post("/interns/{intern_id}/time_in", response_model=schemas.Attendance)
def log_time_in(intern_id: int, db: Session = Depends(get_db)):
    today = date.today()
    attendance = crud.get_attendance_by_intern_and_date(db, intern_id=intern_id, date=today)
    now = datetime.utcnow()
    if attendance:
        if attendance.time_in:
            raise HTTPException(status_code=400, detail="Time in already logged for today")
        attendance = crud.update_attendance_time_in(db, attendance, now)
    else:
        attendance_in = schemas.AttendanceCreate(intern_id=intern_id, date=today, time_in=now)
        attendance = crud.create_attendance(db, attendance_in)
    return attendance

# Intern log time out
@app.post("/interns/{intern_id}/time_out", response_model=schemas.Attendance)
def log_time_out(intern_id: int, db: Session = Depends(get_db)):
    today = date.today()
    attendance = crud.get_attendance_by_intern_and_date(db, intern_id=intern_id, date=today)
    now = datetime.utcnow()
    if not attendance or not attendance.time_in:
        raise HTTPException(status_code=400, detail="Time in not logged yet for today")
    if attendance.time_out:
        raise HTTPException(status_code=400, detail="Time out already logged for today")
    attendance = crud.update_attendance_time_out(db, attendance, now)
    return attendance

# Get intern attendance summary (total duration and daily attendance)
@app.get("/interns/{intern_id}/attendance")
def get_attendance_summary(intern_id: int, db: Session = Depends(get_db)):
    attendances = crud.get_intern_attendance(db, intern_id=intern_id)
    total_duration = timedelta()
    daily_attendance = []
    for att in attendances:
        if att.time_in and att.time_out:
            duration = att.time_out - att.time_in
            total_duration += duration
            daily_attendance.append({
                "date": att.date,
                "time_in": att.time_in,
                "time_out": att.time_out,
                "duration_minutes": int(duration.total_seconds() / 60)
            })
    return {
        "intern_id": intern_id,
        "total_duration_minutes": int(total_duration.total_seconds() / 60),
        "daily_attendance": daily_attendance
    }

# Admin assign task to intern
@app.post("/tasks/", response_model=schemas.Task)
def assign_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    intern = crud.get_intern(db, task.intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    return crud.create_task(db, task=task)

# Intern mark task completed
@app.post("/tasks/{task_id}/complete", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.completed:
        raise HTTPException(status_code=400, detail="Task already completed")
    return crud.mark_task_completed(db, task)
