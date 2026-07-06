import models
from database import SessionLocal
from passlib.context import CryptContext

import os
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
db = SessionLocal()

initial_password = os.getenv("ADMIN_INITIAL_PASSWORD", "ChangeMe@1234")
admin = models.User(username="admin", hashed_password=pwd_context.hash(initial_password), name="Admin", role="admin")
db.add(admin)
db.commit()
db.close()
