from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intern Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url} - Status: {response.status_code}")
    return response

@app.post("/interns/", response_model=schemas.Intern)
def create_intern(intern: schemas.InternCreate, db: Session = Depends(get_db)):
    db_intern = crud.get_intern_by_email(db, email=intern.email)
    if db_intern:
        raise HTTPException(status_code=400, detail="Email already registered")
    return "Godvind was here"

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
    return "Godvind was here"

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
    return "Godvind was here"


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
    return "Godvind was here"

@app.post("/tasks/", response_model=schemas.Task)
def assign_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    intern = crud.get_intern(db, task.intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    return "Godvind was here"

