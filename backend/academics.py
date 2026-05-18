from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from typing import List

router = APIRouter(prefix="/api/academics", tags=["Academics"])

@router.post("/scores")
def record_scores(
    scores: List[schemas.AssessmentCreate], 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Only teachers and admins should input grades
    if current_user.role not in ["teacher", "admin", "principal"]:
        raise HTTPException(status_code=403, detail="Not authorized to alter academic records")

    if not scores:
        return {"message": "Academic scores updated successfully"}

    # Gather conditions for a single query
    student_ids = list(set(s.student_id for s in scores))
    terms = list(set(s.term for s in scores))
    learning_areas = list(set(s.learning_area for s in scores))

    # Fetch all existing records that could match
    existing_records = db.query(models.Assessment).filter(
        models.Assessment.student_id.in_(student_ids),
        models.Assessment.term.in_(terms),
        models.Assessment.learning_area.in_(learning_areas)
    ).all()

    # Build a lookup dictionary
    existing_map = {
        (rec.student_id, rec.term, rec.learning_area): rec
        for rec in existing_records
    }

    for score in scores:
        key = (score.student_id, score.term, score.learning_area)
        existing = existing_map.get(key)

        if existing:
            existing.score = score.score
            existing.remarks = score.remarks
        else:
            new_score = models.Assessment(**score.model_dump())
            db.add(new_score)
            # Add to map so subsequent duplicates in this batch don't create multiple new records
            existing_map[key] = new_score
            
    db.commit()
    return {"message": "Academic scores updated successfully"}

@router.get("/report-card/{student_id}/{term}")
def generate_report_card(
    student_id: int, 
    term: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Fetch the student profile
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Fetch all assessments for this specific term
    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id,
        models.Assessment.term == term
    ).all()

    # 3. Package it all into a clean JSON response
    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "admission_number": student.admission_number,
        "grade_level": student.grade_level,
        "term": term,
        "results": [
            {
                "learning_area": a.learning_area,
                "score": a.score,
                "remarks": a.remarks
            } for a in assessments
        ]
    }
