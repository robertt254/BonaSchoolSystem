from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from datetime import datetime

router = APIRouter(prefix="/api/finance", tags=["Finance"])

def verify_finance_access(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role not in ["finance", "admin"]: # "finance" not accountant based on schema change earlier or instruction
        raise HTTPException(status_code=403, detail="Only Finance Officers or Admins can execute payroll")
    return current_user

@router.post("/payroll", response_model=schemas.PayrollResponse)
def execute_payroll(
    payroll: schemas.PayrollCreate,
    db: Session = Depends(get_db),
    finance_officer: models.User = Depends(verify_finance_access)
):
    # Verify the staff exists
    staff = db.query(models.User).filter(models.User.id == payroll.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    new_payroll = models.Payroll(**payroll.model_dump())
    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)
    return new_payroll

@router.get("/payroll", response_model=list[schemas.PayrollResponse])
def get_payroll_ledger(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    finance_officer: models.User = Depends(verify_finance_access)
):
    return db.query(models.Payroll).offset(skip).limit(limit).all()

@router.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "principal":
        raise HTTPException(status_code=403, detail="Only the principal can create expenses")

    new_expense = models.Expense(
        **expense.model_dump(),
        recorded_by=current_user.name
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role not in ["finance", "admin", "principal", "secretary"]:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")
    return db.query(models.Expense).offset(skip).limit(limit).all()
