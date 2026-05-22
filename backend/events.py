from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from audit import log_action
from typing import Optional

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("/")
def list_events(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    q = db.query(models.SchoolEvent)
    if year:
        from sqlalchemy import extract
        q = q.filter(extract("year", models.SchoolEvent.start_date) == year)
    if month:
        from sqlalchemy import extract
        q = q.filter(extract("month", models.SchoolEvent.start_date) == month)
    events = q.order_by(models.SchoolEvent.start_date).all()
    return [_serialize(e) for e in events]


@router.post("/", status_code=201)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal", "secretary", "teacher"}:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_event = models.SchoolEvent(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        start_date=event.start_date,
        end_date=event.end_date,
        all_day=event.all_day,
        created_by=current_user.name,
    )
    db.add(new_event)
    db.flush()
    log_action(db, current_user.id, "CREATE", "event", new_event.id, {"title": event.title})
    db.commit()
    db.refresh(new_event)
    return _serialize(new_event)


@router.put("/{event_id}")
def update_event(
    event_id: int,
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal", "secretary", "teacher"}:
        raise HTTPException(status_code=403, detail="Not authorized")

    row = db.query(models.SchoolEvent).filter(models.SchoolEvent.id == event_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in event.model_dump().items():
        setattr(row, field, value)

    log_action(db, current_user.id, "UPDATE", "event", event_id, {"title": event.title})
    db.commit()
    db.refresh(row)
    return _serialize(row)


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role not in {"admin", "principal"}:
        raise HTTPException(status_code=403, detail="Not authorized")

    row = db.query(models.SchoolEvent).filter(models.SchoolEvent.id == event_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")

    log_action(db, current_user.id, "DELETE", "event", event_id)
    db.delete(row)
    db.commit()


def _serialize(e: models.SchoolEvent) -> dict:
    return {
        "id": e.id,
        "title": e.title,
        "description": e.description,
        "event_type": e.event_type,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "all_day": e.all_day,
        "created_by": e.created_by,
        "created_at": e.created_at,
    }
