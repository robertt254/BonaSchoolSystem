from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db
import models, schemas, auth
from audit import log_action
from typing import List
from datetime import date

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

MARK_ROLES = {"teacher", "principal", "admin"}


@router.post("/bulk")
def log_bulk_attendance(
    records: List[schemas.AttendanceCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in MARK_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to mark attendance")

    student_ids = [r.student_id for r in records]
    existing_students = {
        s.id
        for s in db.query(models.Student.id).filter(
            models.Student.id.in_(student_ids),
            models.Student.is_deleted == False,
        ).all()
    }
    missing = set(student_ids) - existing_students
    if missing:
        raise HTTPException(status_code=404, detail=f"Student IDs not found: {sorted(missing)}")

    today = date.today()
    existing_records = {
        att.student_id: att
        for att in db.query(models.Attendance).filter(
            and_(
                models.Attendance.student_id.in_(student_ids),
                models.Attendance.date == today,
            )
        ).all()
    }

    for record in records:
        if record.student_id in existing_records:
            existing_records[record.student_id].is_present = record.is_present
            existing_records[record.student_id].remarks = record.remarks
        else:
            db.add(models.Attendance(**record.model_dump()))

    log_action(db, current_user.id, "CREATE", "attendance", None,
               {"date": str(today), "count": len(records)})
    db.commit()
    return {"message": "Attendance updated successfully"}


@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: int,
    limit: int = 60,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    total = db.query(func.count(models.Attendance.id)).filter(
        models.Attendance.student_id == student_id
    ).scalar() or 0
    present = db.query(func.count(models.Attendance.id)).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.is_present == True,
    ).scalar() or 0

    records = (
        db.query(models.Attendance)
        .filter(models.Attendance.student_id == student_id)
        .order_by(models.Attendance.date.desc())
        .limit(limit)
        .all()
    )

    return {
        "student_id": student_id,
        "total_days": total,
        "days_present": present,
        "attendance_percentage": round(present / total * 100) if total > 0 else 100,
        "records": [
            {"date": str(r.date), "is_present": r.is_present, "remarks": r.remarks or ""}
            for r in records
        ],
    }


@router.get("/today/{grade}")
def get_today_attendance(
    grade: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    today = date.today()

    rows = (
        db.query(models.Student, models.Attendance)
        .outerjoin(
            models.Attendance,
            and_(
                models.Attendance.student_id == models.Student.id,
                models.Attendance.date == today,
            ),
        )
        .filter(
            models.Student.grade_level == grade,
            models.Student.is_deleted == False,
        )
        .all()
    )

    return [
        {
            "student_id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "is_present": att.is_present if att else True,
            "remarks": att.remarks if att else "",
        }
        for student, att in rows
    ]
