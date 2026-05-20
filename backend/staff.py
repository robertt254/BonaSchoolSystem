from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from audit import log_action

router = APIRouter(prefix="/api/staff", tags=["Staff Management"])


def verify_admin(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only System Administrators can manage staff")
    return current_user


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_staff(db: Session = Depends(get_db), admin: models.User = Depends(verify_admin)):
    return db.query(models.User).all()


@router.post("/", response_model=schemas.UserResponse)
def create_staff(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin),
):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        name=user.name,
        role=user.role,
        hashed_password=auth.get_password_hash(user.password),
    )
    db.add(new_user)
    db.flush()
    log_action(db, admin.id, "CREATE", "staff", new_user.id,
               {"username": user.username, "role": user.role})
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_staff(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin),
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
    return db_user


@router.delete("/{user_id}")
def terminate_staff(
    user_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin),
):
    if admin.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete your own admin account")

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    log_action(db, admin.id, "DELETE", "staff", user_id,
               {"username": db_user.username, "role": db_user.role})
    db.delete(db_user)
    db.commit()
    return {"message": "Staff account terminated"}


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
