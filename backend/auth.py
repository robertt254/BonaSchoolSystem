import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
import models
from limiter import limiter

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set. Refusing to start.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Accept both bcrypt (new) and pbkdf2_sha256 (legacy). New passwords are always
# stored as bcrypt; legacy hashes are re-saved as bcrypt on next successful login.
pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    deprecated=["pbkdf2_sha256"],
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def verify_and_maybe_rehash(plain: str, hashed: str, user: models.User, db: Session) -> bool:
    """Verify password and transparently upgrade deprecated hashes to bcrypt."""
    if not pwd_context.verify(plain, hashed):
        return False
    if pwd_context.needs_update(hashed):
        user.hashed_password = pwd_context.hash(plain)
        db.add(user)
        db.commit()
    return True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_and_maybe_rehash(form_data.password, user.hashed_password, user, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user.username,
        "role": user.role,
        "name": user.name,
        "exp": expire,
    }
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {"name": user.name, "role": user.role},
    }


@router.post("/setup-users")
def setup_initial_users(db: Session = Depends(get_db)):
    """
    One-time bootstrap. Only works on an empty database.
    Remove or disable this route before deploying to production.
    """
    if db.query(models.User).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Users already exist. Setup is disabled.",
        )

    initial_users = [
        models.User(
            username="admin",
            hashed_password=get_password_hash(os.getenv("ADMIN_INITIAL_PASSWORD", "ChangeMe@1234")),
            role="admin",
            name="System Admin",
        ),
        models.User(
            username="principal",
            hashed_password=get_password_hash(os.getenv("PRINCIPAL_INITIAL_PASSWORD", "ChangeMe@1234")),
            role="principal",
            name="Jane Principal",
        ),
        models.User(
            username="accountant",
            hashed_password=get_password_hash(os.getenv("ACCOUNTANT_INITIAL_PASSWORD", "ChangeMe@1234")),
            role="accountant",
            name="Mary Finance",
        ),
    ]

    db.add_all(initial_users)
    db.commit()

    return {"message": "Database seeded. Change all default passwords immediately."}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials — please log in again",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


@router.post("/change-password")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not pwd_context.verify(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.hashed_password = get_password_hash(data.new_password)
    db.add(current_user)
    db.commit()
    return {"message": "Password changed successfully"}
