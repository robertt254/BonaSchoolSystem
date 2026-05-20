import os
import models
from database import SessionLocal, engine, Base
from auth import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

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

for user in initial_users:
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not existing_user:
        db.add(user)

db.commit()
db.close()
