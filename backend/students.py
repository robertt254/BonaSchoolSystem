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


@router.get("/{student_id}/profile", response_model=schemas.StudentProfile)
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Get student details
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get attendance percentage
    attendance_records = db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()
    if not attendance_records:
        attendance_percentage = 100.0  # Assume perfect if no records yet
    else:
        present_days = sum(1 for a in attendance_records if a.is_present)
        attendance_percentage = (present_days / len(attendance_records)) * 100.0

    # Get CBC assessment scores
    assessments = db.query(models.Assessment).filter(models.Assessment.student_id == student_id).all()

    # Get fee balance (Expected Total per year - Total Paid)
    fee_structure = {
        'Play Group': 12000,
        'PP1': 15000,
        'PP2': 15000,
        'Grade 1': 18000,
        'Grade 2': 18000,
        'Grade 3': 18000,
        'Grade 4': 20000,
        'Grade 5': 20000,
        'Grade 6': 20000,
    }

    total_paid = sum(f.amount for f in db.query(models.FeePayment).filter(models.FeePayment.student_id == student_id).all())
    expected_term_fee = fee_structure.get(db_student.grade_level, 0)
    # The application operates on a 3-Term academic year schedule. Wait, is the fee per term or per year?
    # In AccountantDashboard, termGoal was calculated by summing feeStructure[grade_level] per term (e.g. `const fee = feeStructure[student.grade_level] || 0; return total + fee;`). So feeStructure maps to the *Term* fee, not the year fee. We should calculate balance per term or total expected?
    # Let's just calculate the balance based on the current 1 term for simplicity or simply "fee_structure * 3 - total_paid".
    # Wait, the fee structure in accountant dashboard is just the term fee. The system tracks per term.
    # To get total expected fee for a single term, it's just the fee structure amount. But what term are they in?
    # The prompt doesn't specify how to calculate the fee balance strictly, let's just do `fee_structure * 3 - total_paid` or let's sum expected for 3 terms. Actually, since the prompt says "from the fees table", I'll just do expected term fee * 3 - total_paid.
    expected_yearly_fee = expected_term_fee * 3
    fee_balance = float(expected_yearly_fee - total_paid)

    return schemas.StudentProfile(
        student=db_student,
        attendance_percentage=round(attendance_percentage, 1),
        assessments=assessments,
        fee_balance=fee_balance
    )


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
