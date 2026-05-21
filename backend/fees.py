from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas, auth
from audit import log_action
from notifications import notify_payment

router = APIRouter(prefix="/api/fees", tags=["Finance & Fees"])

CBC_TERMLY_FEES_FALLBACK = {
    "Play Group": 12000.00,
    "PP1": 15000.00,
    "PP2": 15000.00,
    "Grade 1": 18000.00,
    "Grade 2": 18000.00,
    "Grade 3": 18000.00,
    "Grade 4": 20000.00,
    "Grade 5": 20000.00,
    "Grade 6": 20000.00,
}

TERM_ORDER = {"Term 1": 1, "Term 2": 2, "Term 3": 3}
TERM_BY_NUM = {1: "Term 1", 2: "Term 2", 3: "Term 3"}

FINANCE_ROLES = {"accountant", "admin", "principal"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _generate_receipt_number(db: Session) -> str:
    year = datetime.now().year
    prefix = f"BNS-{year}-"
    last = (
        db.query(models.FeePayment)
        .filter(models.FeePayment.receipt_number.isnot(None))
        .filter(models.FeePayment.receipt_number.like(f"{prefix}%"))
        .with_for_update()
        .order_by(models.FeePayment.id.desc())
        .first()
    )
    if last and last.receipt_number:
        last_seq = int(last.receipt_number.split("-")[2])
    else:
        last_seq = 0
    return f"{prefix}{last_seq + 1:05d}"


def _get_expected_fee(db: Session, grade_level: str, term: str) -> float:
    year = datetime.now().year
    structure = (
        db.query(models.FeeStructure)
        .filter(
            models.FeeStructure.grade_level == grade_level,
            models.FeeStructure.term == term,
            models.FeeStructure.academic_year == year,
        )
        .first()
    )
    if structure:
        return float(structure.amount)
    return CBC_TERMLY_FEES_FALLBACK.get(grade_level, 0.0)


def _get_rollover_credit(db: Session, student_id: int, grade_level: str, up_to_term_num: int) -> float:
    """Return the cumulative overpayment from all terms before up_to_term_num."""
    cumulative_expected = 0.0
    cumulative_paid = 0.0
    for num in range(1, up_to_term_num):
        t = TERM_BY_NUM[num]
        cumulative_expected += _get_expected_fee(db, grade_level, t)
        paid = db.query(func.sum(models.FeePayment.amount)).filter(
            models.FeePayment.student_id == student_id,
            models.FeePayment.term == t,
        ).scalar() or 0.0
        cumulative_paid += float(paid)
    return max(0.0, round(cumulative_paid - cumulative_expected, 2))


def compute_effective_term_collection(db: Session, students: list, term: str) -> float:
    """
    Compute the portion of payments that count toward `term`.

    Each student's contribution is capped at their expected fee for the term.
    Overpayments from prior terms are brought in as rollover credit before capping.
    This prevents overpayments in Term 1 from inflating Term 1's completion %.
    """
    term_num = TERM_ORDER.get(term, 1)
    total = 0.0
    for s in students:
        expected = _get_expected_fee(db, s.grade_level, term)
        if expected <= 0:
            continue
        direct_paid = float(
            db.query(func.sum(models.FeePayment.amount))
            .filter(models.FeePayment.student_id == s.id, models.FeePayment.term == term)
            .scalar() or 0.0
        )
        rollover = _get_rollover_credit(db, s.id, s.grade_level, term_num)
        total += min(direct_paid + rollover, expected)
    return round(total, 2)


# ── Payment endpoints ─────────────────────────────────────────────────────────

@router.post("/", response_model=schemas.FeeResponse)
def record_payment(
    fee: schemas.FeeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"accountant", "admin"}:
        raise HTTPException(status_code=403, detail="Not authorized to record payments")

    student = db.query(models.Student).filter(
        models.Student.id == fee.student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    receipt = _generate_receipt_number(db)
    new_fee = models.FeePayment(
        **fee.model_dump(),
        recorded_by=current_user.name,
        receipt_number=receipt,
    )
    db.add(new_fee)
    db.flush()
    log_action(db, current_user.id, "CREATE", "fee", new_fee.id,
               {"receipt": receipt, "amount": str(fee.amount), "student_id": fee.student_id})
    db.commit()
    db.refresh(new_fee)

    if student.guardian_phone:
        background_tasks.add_task(
            notify_payment,
            f"{student.first_name} {student.last_name}",
            student.guardian_phone,
            float(fee.amount),
            fee.term,
            receipt,
        )

    return new_fee


@router.get("/student/{student_id}", response_model=list[schemas.FeeResponse])
def get_student_payments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view fee records")
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return (
        db.query(models.FeePayment)
        .filter(models.FeePayment.student_id == student_id)
        .order_by(models.FeePayment.payment_date.desc())
        .all()
    )


@router.get("/", response_model=list[schemas.FeeResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")
    return db.query(models.FeePayment).order_by(models.FeePayment.payment_date.desc()).all()


@router.get("/balance/{student_id}/{term}")
def get_student_balance(
    student_id: int,
    term: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")

    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    current_term_num = TERM_ORDER.get(term, 1)
    expected = _get_expected_fee(db, student.grade_level, term)

    total_paid = float(
        db.query(func.sum(models.FeePayment.amount)).filter(
            models.FeePayment.student_id == student_id,
            models.FeePayment.term == term,
        ).scalar() or 0.0
    )

    # Credit carried forward from any overpayments in earlier terms
    rollover_credit = _get_rollover_credit(db, student_id, student.grade_level, current_term_num)

    # Outstanding cannot be negative (overpayment of current term is not rolled here,
    # it will become credit when the next term is queried)
    outstanding = round(max(0.0, expected - total_paid - rollover_credit), 2)

    return {
        "student_id": student.id,
        "student_name": f"{student.first_name} {student.last_name}",
        "grade_level": student.grade_level,
        "term_checked": term,
        "expected_term_fee": expected,
        "total_paid_this_term": total_paid,
        "rollover_credit": rollover_credit,
        "outstanding_balance": outstanding,
    }


@router.get("/term-summary")
def get_term_summary(
    term: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Expected vs collected for a given term across all active students."""
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")

    students = db.query(models.Student).filter(
        models.Student.is_deleted == False,
        models.Student.status == "Active",
    ).all()

    total_expected = round(sum(_get_expected_fee(db, s.grade_level, term) for s in students), 2)

    # Effective collection: capped per-student so overpayments don't inflate %
    total_collected = compute_effective_term_collection(db, students, term)

    pct = round(total_collected / total_expected * 100, 1) if total_expected > 0 else 0.0

    return {
        "term": term,
        "total_expected": total_expected,
        "total_collected": total_collected,
        "percentage": pct,
    }


@router.get("/monthly-collection")
def get_monthly_collection(
    year: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Fee payments totalled by calendar month for a given year (defaults to current year)."""
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")

    if year is None:
        year = datetime.now().year

    rows = (
        db.query(
            func.extract("month", models.FeePayment.payment_date).label("month"),
            func.sum(models.FeePayment.amount).label("total"),
        )
        .filter(func.extract("year", models.FeePayment.payment_date) == year)
        .group_by(func.extract("month", models.FeePayment.payment_date))
        .order_by(func.extract("month", models.FeePayment.payment_date))
        .all()
    )

    monthly = {int(r.month): float(r.total) for r in rows}
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return [{"month": labels[m - 1], "total": monthly.get(m, 0.0)} for m in range(1, 13)]


@router.get("/defaulters")
def get_defaulters(
    term: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Return all active students who have an outstanding balance for the given term."""
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized to view financials")

    students = db.query(models.Student).filter(models.Student.is_deleted == False).all()
    defaulters = []
    current_term_num = TERM_ORDER.get(term, 1)
    for s in students:
        expected = _get_expected_fee(db, s.grade_level, term)
        if expected == 0:
            continue
        paid = float(
            db.query(func.sum(models.FeePayment.amount)).filter(
                models.FeePayment.student_id == s.id,
                models.FeePayment.term == term,
            ).scalar() or 0.0
        )
        credit = _get_rollover_credit(db, s.id, s.grade_level, current_term_num)
        balance = round(max(0.0, expected - paid - credit), 2)
        if balance > 0:
            defaulters.append({
                "student_id": s.id,
                "student_name": f"{s.first_name} {s.last_name}",
                "admission_number": s.admission_number,
                "grade_level": s.grade_level,
                "expected_fee": expected,
                "total_paid": paid,
                "rollover_credit": credit,
                "outstanding_balance": balance,
            })
    return defaulters


# ── Fee Structure CRUD ────────────────────────────────────────────────────────

@router.get("/structure", response_model=list[schemas.FeeStructureResponse])
def get_fee_structure(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in FINANCE_ROLES:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(models.FeeStructure).order_by(
        models.FeeStructure.academic_year.desc(),
        models.FeeStructure.grade_level,
    ).all()


@router.post("/structure", response_model=schemas.FeeStructureResponse)
def create_fee_structure(
    entry: schemas.FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can configure fee structures")

    existing = db.query(models.FeeStructure).filter(
        models.FeeStructure.grade_level == entry.grade_level,
        models.FeeStructure.term == entry.term,
        models.FeeStructure.fee_type == entry.fee_type,
        models.FeeStructure.academic_year == entry.academic_year,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Fee structure entry already exists for this grade/term/type/year")

    new_entry = models.FeeStructure(**entry.model_dump())
    db.add(new_entry)
    db.flush()
    log_action(db, current_user.id, "CREATE", "fee_structure", new_entry.id, entry.model_dump())
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.put("/structure/{entry_id}", response_model=schemas.FeeStructureResponse)
def update_fee_structure(
    entry_id: int,
    entry: schemas.FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can configure fee structures")

    row = db.query(models.FeeStructure).filter(models.FeeStructure.id == entry_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Fee structure entry not found")

    for key, value in entry.model_dump().items():
        setattr(row, key, value)

    log_action(db, current_user.id, "UPDATE", "fee_structure", entry_id, entry.model_dump())
    db.commit()
    db.refresh(row)
    return row


@router.delete("/structure/{entry_id}")
def delete_fee_structure(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin"}:
        raise HTTPException(status_code=403, detail="Only admins can delete fee structure entries")

    row = db.query(models.FeeStructure).filter(models.FeeStructure.id == entry_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Fee structure entry not found")

    log_action(db, current_user.id, "DELETE", "fee_structure", entry_id)
    db.delete(row)
    db.commit()
    return {"message": "Fee structure entry deleted"}
