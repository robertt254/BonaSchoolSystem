from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/staff", tags=["Staff Management"])

# Helper function to ensure only admins get in
def verify_admin(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only System Administrators can manage staff")
    return current_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_staff(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    return db.query(models.User).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.UserResponse)
def create_staff(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db), 
    admin: models.User = Depends(verify_admin)
):
    # Check if username is already taken
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password before saving!
    hashed_pw = auth.pwd_context.hash(user.password)
    
    new_user = models.User(
        username=user.username,
        name=user.name,
        role=user.role,
        hashed_password=hashed_pw
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
    admin: models.User = Depends(verify_admin)
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
    admin: models.User = Depends(verify_admin)
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
