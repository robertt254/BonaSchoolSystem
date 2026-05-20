from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from audit import log_action

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
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        db.query(models.Student)
        .filter(models.Student.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/archived", response_model=list[schemas.StudentResponse])
def get_archived_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can view archived records")
    return db.query(models.Student).filter(models.Student.is_deleted == True).all()


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
