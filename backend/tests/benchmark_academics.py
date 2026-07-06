import sys
import os
import time

# Ensure backend module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from models import Base
from datetime import datetime, timezone

# Setup a test SQLite database
engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def seed_db(db):
    # Create 100 students in Grade 1
    students = []
    for i in range(1000):
        s = models.Student(
            first_name=f"First{i}",
            last_name=f"Last{i}",
            admission_number=f"BONA-{i:05d}",
            grade_level="Grade 1",
            date_of_birth=datetime(2015, 1, 1).date(),
            gender="Male",
            is_deleted=False,
            created_at=datetime.now(timezone.utc)
        )
        db.add(s)
        students.append(s)
    db.commit()

    # Create 10 assessments for each student for Term 1, 2024
    for s in students:
        for j in range(10):
            a = models.Assessment(
                student_id=s.id,
                academic_year="2024",
                term="Term 1",
                learning_area=f"Area {j}",
                strand=f"Strand {j}",
                score=str(j),
                remarks=f"Remark {j}"
            )
            db.add(a)
    db.commit()


def run_benchmark():
    db = TestingSessionLocal()
    seed_db(db)

    # Fetch all students in Grade 1
    students = (
        db.query(models.Student)
        .filter(models.Student.grade_level == "Grade 1", models.Student.is_deleted == False)
        .order_by(models.Student.last_name)
        .all()
    )

    grade = "Grade 1"
    term = "Term 1"
    academic_year = "2024"

    start_time = time.time()

    result = []
    for s in students:
        q = db.query(models.Assessment).filter(
            models.Assessment.student_id == s.id,
            models.Assessment.term == term,
        )
        if academic_year:
            q = q.filter(models.Assessment.academic_year == academic_year)
        assessments = q.all()

        scores: dict = {}
        for a in assessments:
            if a.learning_area not in scores:
                scores[a.learning_area] = {}
            scores[a.learning_area][a.strand] = {
                "score": a.score,
                "remarks": a.remarks,
            }

        result.append({
            "student_id": s.id,
            "student_name": f"{s.first_name} {s.last_name}",
            "admission_number": s.admission_number,
            "scores": scores,
        })

    end_time = time.time()

    print(f"Original logic took {end_time - start_time:.4f} seconds")

    # NEW OPTIMIZED LOGIC
    start_time_opt = time.time()

    result_opt = []
    student_ids = [s.id for s in students]

    q_opt = db.query(models.Assessment).filter(
        models.Assessment.student_id.in_(student_ids),
        models.Assessment.term == term,
    )
    if academic_year:
        q_opt = q_opt.filter(models.Assessment.academic_year == academic_year)
    all_assessments = q_opt.all()

    # Group assessments by student_id
    assessments_by_student = {s_id: [] for s_id in student_ids}
    for a in all_assessments:
        if a.student_id in assessments_by_student:
            assessments_by_student[a.student_id].append(a)

    for s in students:
        scores: dict = {}
        for a in assessments_by_student[s.id]:
            if a.learning_area not in scores:
                scores[a.learning_area] = {}
            scores[a.learning_area][a.strand] = {
                "score": a.score,
                "remarks": a.remarks,
            }

        result_opt.append({
            "student_id": s.id,
            "student_name": f"{s.first_name} {s.last_name}",
            "admission_number": s.admission_number,
            "scores": scores,
        })

    end_time_opt = time.time()
    print(f"Optimized logic took {end_time_opt - start_time_opt:.4f} seconds")
    print(f"Results match: {result == result_opt}")

    db.close()

if __name__ == "__main__":
    run_benchmark()
