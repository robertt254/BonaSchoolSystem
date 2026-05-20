from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from audit import log_action

router = APIRouter(prefix="/api/finance", tags=["Finance"])

FINANCE_ROLES = {"accountant", "admin", "principal"}


def require_finance(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to manage payroll")
    return current_user


@router.post("/payroll", response_model=schemas.PayrollResponse)
def execute_payroll(
    payroll: schemas.PayrollCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    staff = db.query(models.User).filter(models.User.id == payroll.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    new_payroll = models.Payroll(
        **payroll.model_dump(),
        recorded_by=current_user.name,
    )
    db.add(new_payroll)
    db.flush()
    log_action(db, current_user.id, "CREATE", "payroll", new_payroll.id,
               {"staff_id": payroll.staff_id, "month": payroll.payment_month,
                "net_pay": str(payroll.net_pay)})
    db.commit()
    db.refresh(new_payroll)
    return new_payroll


@router.get("/payroll", response_model=list[schemas.PayrollResponse])
def get_payroll_ledger(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    return (
        db.query(models.Payroll)
        .order_by(models.Payroll.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"principal", "admin"}:
        raise HTTPException(status_code=403, detail="Only the principal or admin can record expenses")

    new_expense = models.Expense(
        **expense.model_dump(),
        recorded_by=current_user.name,
    )
    db.add(new_expense)
    db.flush()
    log_action(db, current_user.id, "CREATE", "expense", new_expense.id,
               {"amount": str(expense.amount), "category": expense.category})
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view expenses")
    return (
        db.query(models.Expense)
        .order_by(models.Expense.expense_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
