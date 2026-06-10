import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models, schemas, academics, auth

import database
database.engine = create_engine("sqlite:///:memory:")
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()

admin_user = models.User(id=1, username="admin", hashed_password="pw", name="Admin", role="admin")
db.add(admin_user)
db.commit()

# Setup test data
for i in range(1, 1001):
    student = models.Student(id=i, first_name=f"First{i}", last_name=f"Last{i}", admission_number=f"ADM-{i}", grade_level="Grade 1", status="Active")
    db.add(student)
db.commit()

# Insert 10 assessments per student
assessments = []
for i in range(1, 1001):
    for j in range(1, 11):
        assessments.append(models.Assessment(
            student_id=i,
            academic_year="2023",
            term="Term 1",
            learning_area=f"Area {j%3}",
            strand=f"Strand {j}",
            score=f"{80+j}",
            remarks="Good"
        ))
db.bulk_save_objects(assessments)
db.commit()

start = time.time()
result = academics.get_grade_assessments(grade="Grade 1", term="Term 1", academic_year="2023", db=db, current_user=admin_user)
end = time.time()

print(f"BASELINE - Time taken to get assessments for 1000 students: {end - start:.4f} seconds")
print(f"Number of students returned: {len(result)}")
