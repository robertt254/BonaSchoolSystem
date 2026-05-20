from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from typing import List
from audit import log_action

router = APIRouter(prefix="/api/academics", tags=["Academics"])


@router.post("/scores")
def record_scores(
    scores: List[schemas.AssessmentCreate],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"teacher", "admin", "principal"}:
        raise HTTPException(status_code=403, detail="Not authorized to alter academic records")

    student_ids = {s.student_id for s in scores}
    existing_students = {
        s.id
        for s in db.query(models.Student.id).filter(
            models.Student.id.in_(student_ids),
            models.Student.is_deleted == False,
        ).all()
    }
    missing = student_ids - existing_students
    if missing:
        raise HTTPException(status_code=404, detail=f"Student IDs not found: {sorted(missing)}")

    for score in scores:
        existing = db.query(models.Assessment).filter(
            models.Assessment.student_id == score.student_id,
            models.Assessment.term == score.term,
            models.Assessment.learning_area == score.learning_area,
        ).first()

        if existing:
            existing.score = score.score
            existing.remarks = score.remarks
            log_action(db, current_user.id, "UPDATE", "assessment", existing.id,
                       {"student_id": score.student_id, "learning_area": score.learning_area, "score": score.score})
        else:
            new_score = models.Assessment(**score.model_dump())
            db.add(new_score)
            db.flush()
            log_action(db, current_user.id, "CREATE", "assessment", new_score.id,
                       {"student_id": score.student_id, "learning_area": score.learning_area, "score": score.score})

    db.commit()
    return {"message": "Academic scores updated successfully"}


@router.get("/report-card/{student_id}/{term}")
def generate_report_card(
    student_id: int,
    term: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.is_deleted == False,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    assessments = db.query(models.Assessment).filter(
        models.Assessment.student_id == student_id,
        models.Assessment.term == term,
    ).all()

    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "admission_number": student.admission_number,
        "grade_level": student.grade_level,
        "term": term,
        "results": [
            {"learning_area": a.learning_area, "score": a.score, "remarks": a.remarks}
            for a in assessments
        ],
    }
