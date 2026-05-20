from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db
import models, schemas, auth
from audit import log_action

# Fallback fee amounts (mirrored from fees.py) used for profile balance calc.
_CBC_FEES = {
    "Play Group": 12000.00, "PP1": 15000.00, "PP2": 15000.00,
    "Grade 1": 18000.00, "Grade 2": 15000.00, "Grade 3": 18000.00,
    "Grade 4": 20000.00, "Grade 5": 20000.00, "Grade 6": 20000.00,
}

router = APIRouter(prefix="/api/students", tags=["Students"])

WRITE_ROLES = {"admin", "principal", "secretary"}


@router.post("/", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in WRITE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to admit students")

    if db.query(models.Student).filter(
        models.Student.admission_number == student.admission_number
    ).first():
        raise HTTPException(status_code=400, detail="Admission number already registered")

    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.flush()  # populate new_student.id before logging
    log_action(db, current_user.id, "CREATE", "student", new_student.id,
               {"admission_number": student.admission_number})
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/", response_model=list[schemas.StudentResponse])
def get_all_students(
    skip: int = 0,
    limit: int = 200,
    search: Optional[str] = Query(None, description="Search by name or admission number"),
    grade: Optional[str] = Query(None, description="Filter by grade level"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.Student).filter(models.Student.is_deleted == False)
    if search:
        like = f"%{search}%"
        q = q.filter(
            or_(
                models.Student.first_name.ilike(like),
                models.Student.last_name.ilike(like),
                models.Student.admission_number.ilike(like),
            )
        )
    if grade:
        q = q.filter(models.Student.grade_level == grade)
    return q.order_by(models.Student.last_name).offset(skip).limit(limit).all()


@router.get("/archived", response_model=list[schemas.StudentResponse])
def get_archived_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can view archived records")
    return db.query(models.Student).filter(models.Student.is_deleted == True).all()


@router.get("/{student_id}/profile")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Attendance rate
    total_days = db.query(func.count(models.Attendance.id)).filter(
        models.Attendance.student_id == student_id
    ).scalar() or 0
    days_present = db.query(func.count(models.Attendance.id)).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.is_present == True,
    ).scalar() or 0
    att_pct = round(days_present / total_days * 100) if total_days > 0 else 100

    # Annual fee balance (all three terms this academic year)
    year = datetime.now().year
    total_expected = 0.0
    for term in ["Term 1", "Term 2", "Term 3"]:
        fs = db.query(models.FeeStructure).filter(
            models.FeeStructure.grade_level == student.grade_level,
            models.FeeStructure.term == term,
            models.FeeStructure.academic_year == year,
        ).first()
        total_expected += float(fs.amount) if fs else _CBC_FEES.get(student.grade_level, 0.0)

    total_paid = float(
        db.query(func.sum(models.FeePayment.amount)).filter(
            models.FeePayment.student_id == student_id
        ).scalar() or 0
    )

    # All assessments ordered by term
    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id
    ).order_by(models.Assessment.term, models.Assessment.learning_area).all()

    # Last 15 fee payments
    payments = db.query(models.FeePayment).filter(
        models.FeePayment.student_id == student_id
    ).order_by(models.FeePayment.payment_date.desc()).limit(15).all()

    return {
        "student": schemas.StudentResponse.model_validate(student),
        "attendance_percentage": att_pct,
        "total_days": total_days,
        "days_present": days_present,
        "fee_balance": round(total_expected - total_paid, 2),
        "total_paid": round(total_paid, 2),
        "assessments": [
            {"id": a.id, "term": a.term, "learning_area": a.learning_area,
             "score": a.score, "remarks": a.remarks}
            for a in assessments
        ],
        "recent_payments": [
            {"id": p.id, "receipt_number": p.receipt_number,
             "amount": float(p.amount), "payment_type": p.payment_type,
             "term": p.term, "payment_date": p.payment_date.isoformat(),
             "recorded_by": p.recorded_by}
            for p in payments
        ],
    }


@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in WRITE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to update student records")

    db_student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    log_action(db, current_user.id, "UPDATE", "student", student_id, update_data)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can archive student records")

    db_student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.is_deleted = True
    db_student.status = "inactive"
    log_action(db, current_user.id, "DELETE", "student", student_id,
               {"admission_number": db_student.admission_number})
    db.commit()
    return {"message": f"Student {student_id} archived. Record preserved for audit purposes."}


@router.post("/{student_id}/restore", response_model=schemas.StudentResponse)
def restore_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can restore student records")

    db_student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == True,
    ).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Archived student not found")

    db_student.is_deleted = False
    db_student.status = "Active"
    log_action(db, current_user.id, "UPDATE", "student", student_id, {"restored": True})
    db.commit()
    db.refresh(db_student)
    return db_student
