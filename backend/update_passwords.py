"""
Script to update user passwords in the database with proper hashing
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from database import SQLALCHEMY_DATABASE_URL, Base

# Same context as in auth.py
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Create connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Create session
db = SessionLocal()

# Hash the password
plain_password = "password"
hashed_password = pwd_context.hash(plain_password)
print(f"Hashed password: {hashed_password}")

# Update the principal user
user = db.query(models.User).filter(models.User.username == "principal").first()
if user:
    print(f"Found user: {user.username}")
    user.hashed_password = hashed_password
    db.commit()
    print("Password updated successfully!")
else:
    print("User 'principal' not found!")

# Also update other users
users_to_update = [
    ("secretary", "password"),
    ("accountant", "password"),
    ("teacher", "password"),
    ("admin", "password"),
]

usernames = [u[0] for u in users_to_update]
users = db.query(models.User).filter(models.User.username.in_(usernames)).all()
user_map = {user.username: user for user in users}

for username, password in users_to_update:
    user = user_map.get(username)
    if user:
        user.hashed_password = pwd_context.hash(password)
        print(f"Updated password for {username}")
    else:
        print(f"User {username} not found")
db.commit()

db.close()
print("Done!")
