from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Import our database tools and models
from database import get_db
import models
import os

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

router = APIRouter()

# Tell FastAPI where clients can go to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- SECURITY SETUP ---
# This tells Python to use pbkdf2_sha256 to securely scramble passwords (bcrypt alternative)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- DATA MODELS ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

# --- ROUTES ---

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Look for the user in the real PostgreSQL database
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Check if user exists AND if the hashed password matches
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # 3. Create the secure token
    expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode = {"sub": user.username, "role": user.role, "exp": expire}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_info": {"name": user.name, "role": user.role}
    }

# --- TEMPORARY BOOTSTRAP ROUTE ---
# Run this ONCE to fill your empty database with the initial staff
@router.post("/setup-users")
def setup_initial_users(db: Session = Depends(get_db)):
    # Check if we already have users so we don't duplicate them
    existing_user = db.query(models.User).first()
    if existing_user:
        return {"message": "Users already exist! Setup skipped."}

    # Create our initial school staff with securely hashed passwords
    initial_users = [
        models.User(username="admin", hashed_password=get_password_hash("password"), role="admin", name="System Admin"),
        models.User(username="principal", hashed_password=get_password_hash("password"), role="principal", name="Jane Principal"),
        models.User(username="accountant", hashed_password=get_password_hash("password"), role="accountant", name="Mary Finance"),
    ]
    
    # Add them to the database and save (commit)
    db.add_all(initial_users)
    db.commit()
    
    return {"message": "Database successfully seeded with Admin, Principal, and Accountant!"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """This is our bouncer. It checks the token and returns the logged-in user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials - Please log in again",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Try to read the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        # If the token is expired or fake, reject them
        raise credentials_exception
        
    # Check if the user actually exists in the database
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user
