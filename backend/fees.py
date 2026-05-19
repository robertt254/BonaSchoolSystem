from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/fees", tags=["Finance & Fees"])

# --- THE CBC TERMLY FEE STRUCTURE ---
CBC_TERMLY_FEES = {
    "Play Group": 12000.00,
    "PP1": 15000.00,
    "PP2": 15000.00,
    "Grade 1": 18000.00,
    "Grade 2": 18000.00,
    "Grade 3": 18000.00,
    "Grade 4": 20000.00,
    "Grade 5": 20000.00,
    "Grade 6": 20000.00
}

@router.post("/", response_model=schemas.FeeResponse)
def record_payment(
    fee: schemas.FeeCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Security Check: Ensure only Finance or Admins can log money
    if current_user.role not in ["finance", "admin", "principal", "secretary"]:
        raise HTTPException(status_code=403, detail="Not authorized to record payments")

    # Verify the student actually exists
    student = db.query(models.Student).filter(models.Student.id == fee.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Log the payment and stamp it with the user who recorded it
    new_fee = models.FeePayment(
        **fee.model_dump(),
        recorded_by=current_user.name
    )
    
    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    return new_fee

@router.get("/", response_model=list[schemas.FeeResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Only Finance and Admin/Principal should see the full ledger
    if current_user.role not in ["finance", "admin", "principal", "secretary"]:
         raise HTTPException(status_code=403, detail="Not authorized to view financials")
         
    return db.query(models.FeePayment).all()

# --- THE CBC BALANCE CALCULATOR ROUTE ---
# Notice we added {term} to the URL so we can check balances per term
@router.get("/balance/{student_id}/{term}")
def get_student_balance(
    student_id: int,
    term: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["finance", "admin", "principal", "secretary"]:
         raise HTTPException(status_code=403, detail="Not authorized to view financials")

    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 1. Get the CBC Expected Fee for ONE term
    expected_term_fee = CBC_TERMLY_FEES.get(student.grade_level, 0.0)

    # 2. Sum up payments for THIS specific student AND THIS specific term
    total_paid = db.query(func.sum(models.FeePayment.amount)).filter(
        models.FeePayment.student_id == student_id,
        models.FeePayment.term == term
    ).scalar()
    
    if total_paid is None:
        total_paid = 0.0

    # 3. Calculate the balance
    balance = expected_term_fee - total_paid

    return {
        "student_id": student.id,
        "student_name": f"{student.first_name} {student.last_name}",
        "grade_level": student.grade_level,
        "term_checked": term,
        "expected_term_fee": expected_term_fee,
        "total_paid_this_term": total_paid,
        "outstanding_balance": balance
    }
