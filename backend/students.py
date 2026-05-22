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
    "Grade 1": 18000.00, "Grade 2": 18000.00, "Grade 3": 18000.00,
    "Grade 4": 20000.00, "Grade 5": 20000.00, "Grade 6": 20000.00,
}

router = APIRouter(prefix="/api/students", tags=["Students"])

WRITE_ROLES = {"admin", "principal", "secretary"}

CBC_GRADES = ["Play Group", "PP1", "PP2", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]


@router.get("/classes/summary")
def get_classes_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Return per-grade headcount, present-today count, and gender split."""
    today = datetime.now().date()
    result = []
    for grade in CBC_GRADES:
        students = db.query(models.Student).filter(
            models.Student.grade_level == grade,
            models.Student.is_deleted == False,
            models.Student.status == "Active",
        ).all()
        total = len(students)
        if total == 0:
            continue
        ids = [s.id for s in students]
        present_today = db.query(func.count(models.Attendance.id)).filter(
            models.Attendance.student_id.in_(ids),
            models.Attendance.date == today,
            models.Attendance.is_present == True,
        ).scalar() or 0
        male = sum(1 for s in students if (s.gender or "").lower() == "male")
        female = sum(1 for s in students if (s.gender or "").lower() == "female")
        result.append({
            "grade_level": grade,
            "total": total,
            "present_today": present_today,
            "male": male,
            "female": female,
            "other": total - male - female,
        })
    return result


@router.get("/classes/{grade}")
def get_class_roster(
    grade: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Return all students in a grade with attendance % and current fee balance."""
    students = db.query(models.Student).filter(
        models.Student.grade_level == grade,
        models.Student.is_deleted == False,
    ).order_by(models.Student.last_name).all()

    year = datetime.now().year
    roster = []
    for s in students:
        total_days = db.query(func.count(models.Attendance.id)).filter(
            models.Attendance.student_id == s.id
        ).scalar() or 0
        days_present = db.query(func.count(models.Attendance.id)).filter(
            models.Attendance.student_id == s.id,
            models.Attendance.is_present == True,
        ).scalar() or 0
        att_pct = round(days_present / total_days * 100) if total_days > 0 else None

        total_expected = 0.0
        for term in ["Term 1", "Term 2", "Term 3"]:
            fs = db.query(models.FeeStructure).filter(
                models.FeeStructure.grade_level == s.grade_level,
                models.FeeStructure.term == term,
                models.FeeStructure.academic_year == year,
            ).first()
            total_expected += float(fs.amount) if fs else _CBC_FEES.get(s.grade_level, 0.0)

        total_paid = float(
            db.query(func.sum(models.FeePayment.amount)).filter(
                models.FeePayment.student_id == s.id
            ).scalar() or 0
        )

        roster.append({
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "admission_number": s.admission_number,
            "gender": s.gender,
            "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
            "status": s.status,
            "attendance_pct": att_pct,
            "fee_balance": round(total_expected - total_paid, 2),
        })
    return roster


def _generate_admission_number(db: Session) -> str:
    year = datetime.now().year
    prefix = f"BNS/{year}/"
    last = (
        db.query(models.Student)
        .filter(models.Student.admission_number.like(f"{prefix}%"))
        .with_for_update()
        .order_by(models.Student.id.desc())
        .first()
    )
    if last and last.admission_number:
        try:
            seq = int(last.admission_number.split("/")[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    else:
        seq = 1
    return f"{prefix}{seq:04d}"


@router.post("/", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in WRITE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to admit students")

    admission_number = student.admission_number or _generate_admission_number(db)

    if db.query(models.Student).filter(
        models.Student.admission_number == admission_number
    ).first():
        raise HTTPException(status_code=400, detail="Admission number already registered")

    data = student.model_dump()
    data["admission_number"] = admission_number
    new_student = models.Student(**data)
    db.add(new_student)
    db.flush()
    log_action(db, current_user.id, "CREATE", "student", new_student.id,
               {"admission_number": admission_number})
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


GRADE_PROGRESSION = {
    "Play Group": "PP1", "PP1": "PP2", "PP2": "Grade 1",
    "Grade 1": "Grade 2", "Grade 2": "Grade 3", "Grade 3": "Grade 4",
    "Grade 4": "Grade 5", "Grade 5": "Grade 6", "Grade 6": None,
}


@router.post("/promote")
def promote_students(
    payload: schemas.PromotionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admin or principal can promote students")

    promoted, graduated = 0, 0
    for sid in payload.student_ids:
        student = db.query(models.Student).filter(
            models.Student.id == sid,
            models.Student.is_deleted == False,
        ).first()
        if not student:
            continue

        if payload.to_grade is None:
            next_grade = GRADE_PROGRESSION.get(student.grade_level)
        else:
            next_grade = payload.to_grade

        if next_grade is None:
            student.status = "Graduated"
            graduated += 1
            log_action(db, current_user.id, "UPDATE", "student", sid,
                       {"from": student.grade_level, "status": "Graduated"})
        else:
            log_action(db, current_user.id, "UPDATE", "student", sid,
                       {"from": student.grade_level, "to": next_grade})
            student.grade_level = next_grade
            promoted += 1

    db.commit()
    return {"promoted": promoted, "graduated": graduated}


@router.post("/year-transition")
def year_transition(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Promote ALL active students to next grade; Grade 6 → Graduated."""
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admin or principal can run year transition")

    students = db.query(models.Student).filter(
        models.Student.is_deleted == False,
        models.Student.status == "Active",
    ).all()

    promoted, graduated = 0, 0
    for student in students:
        next_grade = GRADE_PROGRESSION.get(student.grade_level)
        if next_grade is None:
            student.status = "Graduated"
            graduated += 1
        else:
            student.grade_level = next_grade
            promoted += 1
        log_action(db, current_user.id, "UPDATE", "student", student.id,
                   {"year_transition": True,
                    "from": student.grade_level if next_grade else student.grade_level,
                    "to": next_grade or "Graduated"})

    db.commit()
    return {"promoted": promoted, "graduated": graduated, "total": promoted + graduated}


@router.get("/enrollment-summary")
def enrollment_summary(
    academic_year: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.Student.grade_level, func.count(models.Student.id).label("count")).filter(
        models.Student.is_deleted == False,
        models.Student.status == "Active",
    )
    rows = q.group_by(models.Student.grade_level).all()
    grade_order = ["Play Group","PP1","PP2","Grade 1","Grade 2","Grade 3","Grade 4","Grade 5","Grade 6"]
    order_map = {g: i for i, g in enumerate(grade_order)}
    result = [{"grade_level": r.grade_level, "count": r.count} for r in rows]
    result.sort(key=lambda x: order_map.get(x["grade_level"], 99))
    return result


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
