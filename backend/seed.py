import os
import sys

import models
from database import SessionLocal
from passlib.context import CryptContext

# Never ship a hardcoded default. The initial admin password must be supplied
# explicitly so a production run can't silently seed a guessable account.
admin_password = os.getenv("ADMIN_INITIAL_PASSWORD")
if not admin_password:
    sys.exit(
        "ADMIN_INITIAL_PASSWORD is not set. "
        "Set it before seeding, e.g. ADMIN_INITIAL_PASSWORD='...' python seed.py"
    )

pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated=["pbkdf2_sha256"])
db = SessionLocal()

admin = models.User(
    username="admin",
    hashed_password=pwd_context.hash(admin_password),
    name="Admin",
    role="admin",
)
db.add(admin)
db.commit()
db.close()
