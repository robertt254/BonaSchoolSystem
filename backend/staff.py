from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/staff", tags=["Staff Management"])

# Helper function to ensure only admins or principal get in
def verify_admin_or_principal(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role not in ["admin", "principal"]:
        raise HTTPException(status_code=403, detail="Only System Administrators or Principals can manage staff")
    return current_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_staff(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: models.User = Depends(verify_admin_or_principal)
):
    return db.query(models.User).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.UserResponse)
def create_staff(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(verify_admin_or_principal)
):
    # Check if username is already taken
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password before saving!
    hashed_pw = auth.pwd_context.hash(user.password)
    
    # Pass all fields securely
    new_user = models.User(
        username=user.username,
        name=user.name,
        role=user.role,
        hashed_password=hashed_pw,
        kra_pin=user.kra_pin,
        nssf_number=user.nssf_number,
        nhif_number=user.nhif_number,
        job_title=user.job_title,
        date_of_hire=user.date_of_hire,
        contract_type=user.contract_type,
        accrued_leave_days=user.accrued_leave_days
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_staff(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(verify_admin_or_principal)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    # If the admin provided a new password, hash it. Otherwise, ignore it.
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = auth.pwd_context.hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def terminate_staff(
    user_id: int, 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(verify_admin_or_principal)
):
    # The Ultimate Safety Check
    if admin.id == user_id:
        raise HTTPException(status_code=400, detail="CRITICAL: You cannot delete your own admin account!")

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Staff member not found")

    db.delete(db_user)
    db.commit()
    return {"message": "Staff account terminated"}
