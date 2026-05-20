from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, auth

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    total_students = db.query(func.count(models.Student.id)).filter(
        models.Student.is_deleted == False
    ).scalar() or 0

    total_staff = db.query(func.count(models.User.id)).scalar() or 0

    total_revenue = float(
        db.query(func.sum(models.FeePayment.amount)).scalar() or 0
    )

    recent_logs = (
        db.query(models.AuditLog, models.User)
        .outerjoin(models.User, models.AuditLog.user_id == models.User.id)
        .order_by(models.AuditLog.timestamp.desc())
        .limit(10)
        .all()
    )

    activity = [
        {
            "id": log.id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "detail": log.detail,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            "user_name": user.name if user else "System",
        }
        for log, user in recent_logs
    ]

    return {
        "total_students": total_students,
        "total_staff": total_staff,
        "total_revenue": total_revenue,
        "recent_activity": activity,
    }
