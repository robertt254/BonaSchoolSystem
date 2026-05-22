from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import date
from pydantic import BaseModel, Field
from database import get_db
import models, schemas, auth
from audit import log_action


class PasswordResetRequest(BaseModel):
    new_password: str = Field(..., min_length=8)

router = APIRouter(prefix="/api/staff", tags=["Staff Management"])


def verify_hr_manager(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Only admins and the principal can manage staff")
    return current_user


def verify_staff_reader(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role not in {"admin", "principal", "accountant"}:
        raise HTTPException(status_code=403, detail="Not authorized to view staff list")
    return current_user


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_staff(db: Session = Depends(get_db), current_user: models.User = Depends(verify_staff_reader)):
    users = db.query(models.User).order_by(models.User.name).all()
    current_year = date.today().year
    result = []
    for user in users:
        approved_leaves = (
            db.query(models.LeaveRequest)
            .filter(
                models.LeaveRequest.staff_id == user.id,
                models.LeaveRequest.status == "approved",
                extract("year", models.LeaveRequest.start_date) == current_year,
            )
            .all()
        )
        days_used = sum((l.end_date - l.start_date).days + 1 for l in approved_leaves)
        entitlement = user.accrued_leave_days if user.accrued_leave_days is not None else 21
        include_salary = current_user.role in {"admin", "accountant"}
        result.append(schemas.UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            role=user.role,
            job_title=user.job_title,
            contract_type=user.contract_type,
            date_of_hire=user.date_of_hire,
            kra_pin=user.kra_pin,
            nssf_number=user.nssf_number,
            nhif_number=user.nhif_number,
            accrued_leave_days=entitlement,
            leave_days_used=days_used,
            leave_days_left=max(0, entitlement - days_used),
            basic_salary=float(user.basic_salary or 0) if include_salary else 0.0,
            allowances=float(user.allowances or 0) if include_salary else 0.0,
            deductions=float(user.deductions or 0) if include_salary else 0.0,
        ))
    return result


@router.post("/", response_model=schemas.UserResponse)
def create_staff(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_hr_manager),
):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        name=user.name,
        role=user.role,
        hashed_password=auth.get_password_hash(user.password),
        job_title=user.job_title,
        contract_type=user.contract_type,
        date_of_hire=user.date_of_hire,
        kra_pin=user.kra_pin,
        nssf_number=user.nssf_number,
        nhif_number=user.nhif_number,
        accrued_leave_days=user.accrued_leave_days if user.accrued_leave_days is not None else 21,
        basic_salary=user.basic_salary or 0,
        allowances=user.allowances or 0,
        deductions=user.deductions or 0,
    )
    db.add(new_user)
    db.flush()
    log_action(db, admin.id, "CREATE", "staff", new_user.id,
               {"username": user.username, "role": user.role})
    db.commit()
    db.refresh(new_user)
    entitlement = new_user.accrued_leave_days if new_user.accrued_leave_days is not None else 21
    include_salary = admin.role in {"admin", "accountant"}
    return schemas.UserResponse(
        id=new_user.id,
        username=new_user.username,
        name=new_user.name,
        role=new_user.role,
        job_title=new_user.job_title,
        contract_type=new_user.contract_type,
        date_of_hire=new_user.date_of_hire,
        kra_pin=new_user.kra_pin,
        nssf_number=new_user.nssf_number,
        nhif_number=new_user.nhif_number,
        accrued_leave_days=entitlement,
        leave_days_used=0,
        leave_days_left=entitlement,
        basic_salary=float(new_user.basic_salary or 0) if include_salary else 0.0,
        allowances=float(new_user.allowances or 0) if include_salary else 0.0,
        deductions=float(new_user.deductions or 0) if include_salary else 0.0,
    )


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_staff(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_hr_manager),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = auth.get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    log_action(db, admin.id, "UPDATE", "staff", user_id,
               {k: v for k, v in update_data.items() if k != "hashed_password"})
    db.commit()
    db.refresh(db_user)
    current_year = date.today().year
    approved_leaves = (
        db.query(models.LeaveRequest)
        .filter(
            models.LeaveRequest.staff_id == db_user.id,
            models.LeaveRequest.status == "approved",
            extract("year", models.LeaveRequest.start_date) == current_year,
        )
        .all()
    )
    days_used = sum((l.end_date - l.start_date).days + 1 for l in approved_leaves)
    entitlement = db_user.accrued_leave_days if db_user.accrued_leave_days is not None else 21
    include_salary = admin.role in {"admin", "accountant"}
    return schemas.UserResponse(
        id=db_user.id,
        username=db_user.username,
        name=db_user.name,
        role=db_user.role,
        job_title=db_user.job_title,
        contract_type=db_user.contract_type,
        date_of_hire=db_user.date_of_hire,
        kra_pin=db_user.kra_pin,
        nssf_number=db_user.nssf_number,
        nhif_number=db_user.nhif_number,
        accrued_leave_days=entitlement,
        leave_days_used=days_used,
        leave_days_left=max(0, entitlement - days_used),
        basic_salary=float(db_user.basic_salary or 0) if include_salary else 0.0,
        allowances=float(db_user.allowances or 0) if include_salary else 0.0,
        deductions=float(db_user.deductions or 0) if include_salary else 0.0,
    )


@router.delete("/{user_id}")
def terminate_staff(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_hr_manager),
):
    if admin.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot terminate your own account")

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    log_action(db, admin.id, "DELETE", "staff", user_id,
               {"username": db_user.username, "role": db_user.role})
    db.delete(db_user)
    db.commit()
    return {"message": "Staff account terminated"}


@router.post("/{user_id}/reset-password")
def reset_staff_password(
    user_id: int,
    payload: PasswordResetRequest,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_hr_manager),
):
    if admin.id == user_id:
        raise HTTPException(status_code=400, detail="Use Change Password to update your own password")

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    db_user.hashed_password = auth.get_password_hash(payload.new_password)
    log_action(db, admin.id, "UPDATE", "staff", user_id,
               {"username": db_user.username, "password_reset": True})
    db.commit()
    return {"message": f"Password for {db_user.name} has been reset successfully"}


@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Not authorized to view audit logs")
    logs = (
        db.query(models.AuditLog)
        .order_by(models.AuditLog.timestamp.desc())
        .limit(500)
        .all()
    )
    return [
        {
            "id": l.id,
            "user_id": l.user_id,
            "action": l.action,
            "resource": l.resource,
            "resource_id": l.resource_id,
            "detail": l.detail,
            "timestamp": l.timestamp,
        }
        for l in logs
    ]
