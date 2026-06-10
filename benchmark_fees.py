import time
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from database import SessionLocal, engine, Base
import models
import schemas
from fees import bulk_upsert_fee_structure

# setup db
models.Base.metadata.create_all(engine)
db = SessionLocal()

admin = models.User(id=1, username="admin", name="Admin", role="admin", hashed_password="pw")
db.add(admin)
db.commit()

# Create dummy entries (let's do 500 entries)
entries = []
count = 0
for year in [2022, 2023, 2024, 2025]:
    for grade in ["Playgroup", "PP1", "PP2", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]:
        for term in ["Term 1", "Term 2", "Term 3"]:
            for fee_type in ["Tuition", "Transport", "Meals", "Uniform", "Library", "Extra-Curricular"]:
                entries.append(
                    schemas.FeeStructureCreate(
                        grade_level=grade,
                        term=term,
                        fee_type=fee_type,
                        academic_year=year,
                        amount=1000.0,
                        is_mandatory=True
                    )
                )
                count += 1
                if count >= 500:
                    break
            if count >= 500:
                break
        if count >= 500:
            break
    if count >= 500:
        break

print(f"Number of entries: {len(entries)}")

# Time the baseline (Insert)
start = time.time()
bulk_upsert_fee_structure(entries=entries, db=db, current_user=admin)
insert_time = time.time() - start

# Update baseline (Update)
for e in entries:
    e.amount = 1200.0

start = time.time()
bulk_upsert_fee_structure(entries=entries, db=db, current_user=admin)
update_time = time.time() - start

print(f"Baseline - Insert time: {insert_time:.4f}s")
print(f"Baseline - Update time: {update_time:.4f}s")
