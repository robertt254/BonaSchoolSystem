from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from typing import List
from datetime import date

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

@router.post("/bulk")
def log_bulk_attendance(
    records: List[schemas.AttendanceCreate], 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["teacher", "principal", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to mark attendance")

    student_ids = [record.student_id for record in records]
    today = date.today()

    existing_records = db.query(models.Attendance).filter(
        models.Attendance.student_id.in_(student_ids),
        models.Attendance.date == today
    ).all()

    existing_map = {r.student_id: r for r in existing_records}

    for record in records:
        existing = existing_map.get(record.student_id)

        if existing:
            existing.is_present = record.is_present
            existing.remarks = record.remarks
        else:
            new_entry = models.Attendance(**record.model_dump())
            db.add(new_entry)
            
    db.commit()
    return {"message": "Attendance updated successfully"}

@router.get("/today/{grade}")
def get_today_attendance(
    grade: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Find students strictly by Grade Level (No streams)
    students = db.query(models.Student).filter(
        models.Student.grade_level == grade
    ).all()
    
    student_ids = [s.id for s in students]

    attendances = db.query(models.Attendance).filter(
        models.Attendance.student_id.in_(student_ids),
        models.Attendance.date == date.today()
    ).all()

    att_map = {att.student_id: att for att in attendances}

    results = []
    for s in students:
        att = att_map.get(s.id)
        
        results.append({
            "student_id": s.id,
            "name": f"{s.first_name} {s.last_name}",
            "is_present": att.is_present if att else True,
            "remarks": att.remarks if att else ""
        })
    return results
