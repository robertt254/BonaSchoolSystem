from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import auth

# Set up the router with a standard prefix
router = APIRouter(prefix="/api/students", tags=["Students"])


@router.post("/", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Check if admission number already exists
    db_student = db.query(models.Student).filter(models.Student.admission_number == student.admission_number).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Admission number already registered")

    # 2. Convert Pydantic schema to SQLAlchemy model
    new_student = models.Student(**student.model_dump())
    
    # 3. Save to PostgreSQL
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


@router.get("/", response_model=list[schemas.StudentResponse])
def get_all_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Retrieve students from the database
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students


# --- 1. THE UPDATE ROUTE (PUT) ---
@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int, 
    student_update: schemas.StudentUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Find the specific student
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Update only the fields the user actually provided
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    # Save changes
    db.commit()
    db.refresh(db_student)
    return db_student


# --- 2. THE DELETE ROUTE (DELETE) ---
@router.delete("/{student_id}")
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Find the specific student
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Erase them from the database
    db.delete(db_student)
    db.commit()
    return {"message": f"Student record {student_id} has been permanently deleted"}
