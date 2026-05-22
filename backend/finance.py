from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas, auth
from audit import log_action
from typing import Optional

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
    payroll_id = new_payroll.id   # capture before commit clears the identity map
    log_action(db, current_user.id, "CREATE", "payroll", payroll_id,
               {"staff_id": payroll.staff_id, "month": payroll.payment_month,
                "net_pay": str(payroll.net_pay)})
    db.commit()

    try:
        db.refresh(new_payroll)
        return new_payroll
    except Exception:
        # Fallback for older Render deploys where created_at may not exist yet.
        # The startup ALTER TABLE migration adds it on next redeploy.
        return schemas.PayrollResponse(
            id=payroll_id,
            staff_id=payroll.staff_id,
            payment_month=payroll.payment_month,
            basic_salary=float(payroll.basic_salary),
            allowances=float(payroll.allowances),
            deductions=float(payroll.deductions),
            net_pay=float(payroll.net_pay),
            recorded_by=current_user.name,
            created_at=None,
        )


@router.get("/payroll", response_model=list[schemas.PayrollResponse])
def get_payroll_ledger(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    return (
        db.query(models.Payroll)
        .order_by(models.Payroll.id.desc())
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


# ── Payslip ────────────────────────────────────────────────────────────────────

@router.get("/payslip/{payroll_id}")
def get_payslip(
    payroll_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    p = db.query(models.Payroll).filter(models.Payroll.id == payroll_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Payroll record not found")

    staff = db.query(models.User).filter(models.User.id == p.staff_id).first()
    return {
        "id": p.id,
        "payment_month": p.payment_month,
        "basic_salary": float(p.basic_salary),
        "allowances": float(p.allowances),
        "deductions": float(p.deductions),
        "net_pay": float(p.net_pay),
        "recorded_by": p.recorded_by,
        "created_at": p.created_at,
        "staff_name": staff.name if staff else "Unknown",
        "job_title": staff.job_title if staff else None,
        "kra_pin": staff.kra_pin if staff else None,
        "nssf_number": staff.nssf_number if staff else None,
        "nhif_number": staff.nhif_number if staff else None,
    }


# ── Budget ─────────────────────────────────────────────────────────────────────

@router.get("/budget")
def get_budgets(
    academic_year: Optional[int] = Query(None),
    term: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    q = db.query(models.Budget)
    if academic_year:
        q = q.filter(models.Budget.academic_year == academic_year)
    if term:
        q = q.filter(models.Budget.term == term)
    budgets = q.order_by(models.Budget.term, models.Budget.category).all()

    result = []
    for b in budgets:
        actual = float(
            db.query(func.sum(models.Expense.amount)).filter(
                models.Expense.category == b.category,
                func.extract("year", models.Expense.expense_date) == b.academic_year,
            ).scalar() or 0
        )
        variance = float(b.budgeted_amount) - actual
        result.append({
            "id": b.id,
            "category": b.category,
            "academic_year": b.academic_year,
            "term": b.term,
            "budgeted_amount": float(b.budgeted_amount),
            "actual_spent": round(actual, 2),
            "variance": round(variance, 2),
            "created_by": b.created_by,
        })
    return result


@router.post("/budget", status_code=201)
def create_budget(
    payload: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    b = models.Budget(
        category=payload.category,
        academic_year=payload.academic_year,
        term=payload.term,
        budgeted_amount=payload.budgeted_amount,
        created_by=current_user.name,
    )
    db.add(b)
    db.flush()
    log_action(db, current_user.id, "CREATE", "budget", b.id,
               {"category": payload.category, "amount": str(payload.budgeted_amount)})
    db.commit()
    db.refresh(b)
    return {"id": b.id, "category": b.category, "academic_year": b.academic_year,
            "term": b.term, "budgeted_amount": float(b.budgeted_amount), "created_by": b.created_by}


@router.put("/budget/{budget_id}", status_code=200)
def update_budget(
    budget_id: int,
    payload: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    b = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    b.category = payload.category
    b.academic_year = payload.academic_year
    b.term = payload.term
    b.budgeted_amount = payload.budgeted_amount
    log_action(db, current_user.id, "UPDATE", "budget", budget_id)
    db.commit()
    return {"message": "Updated"}


@router.delete("/budget/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    b = db.query(models.Budget).filter(models.Budget.id == budget_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    log_action(db, current_user.id, "DELETE", "budget", budget_id)
    db.delete(b)
    db.commit()


# ── Petty Cash ─────────────────────────────────────────────────────────────────

@router.get("/petty-cash")
def get_petty_cash(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    transactions = (
        db.query(models.PettyCashTransaction)
        .order_by(models.PettyCashTransaction.transaction_date.asc())
        .all()
    )
    running = 0.0
    result = []
    for t in transactions:
        amt = float(t.amount)
        running += amt if t.transaction_type == "IN" else -amt
        result.append({
            "id": t.id,
            "transaction_type": t.transaction_type,
            "amount": amt,
            "description": t.description,
            "category": t.category,
            "recorded_by": t.recorded_by,
            "transaction_date": t.transaction_date,
            "running_balance": round(running, 2),
        })
    result.reverse()
    return result


@router.post("/petty-cash", status_code=201)
def create_petty_cash(
    payload: schemas.PettyCashCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    t = models.PettyCashTransaction(
        transaction_type=payload.transaction_type,
        amount=payload.amount,
        description=payload.description,
        category=payload.category,
        recorded_by=current_user.name,
        transaction_date=datetime.now(timezone.utc),
    )
    db.add(t)
    db.flush()
    log_action(db, current_user.id, "CREATE", "petty_cash", t.id,
               {"type": payload.transaction_type, "amount": str(payload.amount)})
    db.commit()
    return {"id": t.id, "message": "Recorded"}


@router.delete("/petty-cash/{tx_id}", status_code=204)
def delete_petty_cash(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_finance),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Not authorized")
    t = db.query(models.PettyCashTransaction).filter(models.PettyCashTransaction.id == tx_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    log_action(db, current_user.id, "DELETE", "petty_cash", tx_id)
    db.delete(t)
    db.commit()
