import pytest
import models
from auth import get_current_user
from sqlalchemy.orm import Session
from main import app

class MockUser:
    id = 1
    username = "teacher1"
    role = "teacher"

def override_get_current_user():
    return MockUser()

@pytest.fixture
def test_students(db: Session):
    u1 = models.User(
        username="teacher1",
        hashed_password="pw",
        name="Teacher 1",
        role="teacher"
    )
    db.add(u1)

    s1 = models.Student(
        admission_number="BONA-0001",
        first_name="John",
        last_name="Doe",
        grade_level="Grade 1",
        is_deleted=False,
    )
    s2 = models.Student(
        admission_number="BONA-0002",
        first_name="Jane",
        last_name="Smith",
        grade_level="Grade 1",
        is_deleted=False,
    )
    db.add_all([s1, s2])
    db.commit()
    db.refresh(s1)
    db.refresh(s2)
    return [s1.id, s2.id]

def test_log_bulk_attendance_success(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = [
        {"student_id": test_students[0], "is_present": True, "remarks": "On time"},
        {"student_id": test_students[1], "is_present": False, "remarks": "Sick"},
    ]

    response = client.post("/api/attendance/bulk", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message": "Attendance updated successfully"}

    att1 = db.query(models.Attendance).filter_by(student_id=test_students[0]).first()
    assert att1 is not None
    assert att1.is_present is True
    assert att1.remarks == "On time"

    att2 = db.query(models.Attendance).filter_by(student_id=test_students[1]).first()
    assert att2 is not None
    assert att2.is_present is False
    assert att2.remarks == "Sick"

def test_log_bulk_attendance_unauthorized(client):
    class UnauthorizedUser:
        id = 2
        username = "parent1"
        role = "parent"

    app.dependency_overrides[get_current_user] = lambda: UnauthorizedUser()

    response = client.post("/api/attendance/bulk", json=[{"student_id": 1, "is_present": True}])
    assert response.status_code == 403

def test_log_bulk_attendance_missing_students(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = [
        {"student_id": test_students[0], "is_present": True},
        {"student_id": 9999, "is_present": False},
    ]

    response = client.post("/api/attendance/bulk", json=payload)
    assert response.status_code == 404
    assert "9999" in response.json()["detail"]

def test_log_bulk_attendance_update_existing(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload1 = [
        {"student_id": test_students[0], "is_present": False, "remarks": "Late"},
    ]
    client.post("/api/attendance/bulk", json=payload1)

    payload2 = [
        {"student_id": test_students[0], "is_present": True, "remarks": "Arrived later"},
    ]
    response = client.post("/api/attendance/bulk", json=payload2)
    assert response.status_code == 200

    att = db.query(models.Attendance).filter_by(student_id=test_students[0]).all()
    assert len(att) == 1
    assert att[0].is_present is True
    assert att[0].remarks == "Arrived later"

def test_log_bulk_attendance_partial_missing(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = [
        {"student_id": test_students[0], "is_present": True},
        {"student_id": 9999, "is_present": False},
        {"student_id": test_students[1], "is_present": True},
    ]

    response = client.post("/api/attendance/bulk", json=payload)
    assert response.status_code == 404
    assert "9999" in response.json()["detail"]

    # Assert nothing was logged for the valid ones either, because it should abort early
    att = db.query(models.Attendance).all()
    assert len(att) == 0

def test_get_student_attendance(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Add some records
    payload = [
        {"student_id": test_students[0], "is_present": True, "remarks": "On time"},
    ]
    client.post("/api/attendance/bulk", json=payload)

    response = client.get(f"/api/attendance/student/{test_students[0]}")
    assert response.status_code == 200

    data = response.json()
    assert data["student_id"] == test_students[0]
    assert data["total_days"] == 1
    assert data["days_present"] == 1
    assert data["attendance_percentage"] == 100
    assert len(data["records"]) == 1

def test_get_student_attendance_not_found(client, db):
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/api/attendance/student/9999")
    assert response.status_code == 404

def test_get_attendance_summary(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = [
        {"student_id": test_students[0], "is_present": True},
        {"student_id": test_students[1], "is_present": False},
    ]
    client.post("/api/attendance/bulk", json=payload)

    response = client.get("/api/attendance/summary")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    grade1 = next((g for g in data if g["grade"] == "Grade 1"), None)
    assert grade1 is not None
    assert grade1["total_records"] == 2
    assert grade1["present"] == 1
    assert grade1["percentage"] == 50

def test_get_today_attendance(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = [
        {"student_id": test_students[0], "is_present": False, "remarks": "Sick"},
    ]
    client.post("/api/attendance/bulk", json=payload)

    response = client.get("/api/attendance/today/Grade%201")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    student1 = next((s for s in data if s["student_id"] == test_students[0]), None)
    assert student1 is not None
    assert student1["is_present"] is False
    assert student1["remarks"] == "Sick"

    student2 = next((s for s in data if s["student_id"] == test_students[1]), None)
    assert student2 is not None
    assert student2["is_present"] is True # default is True if not marked
    assert student2["remarks"] == ""


def test_log_bulk_attendance_absence_notification(client, db, test_students):
    app.dependency_overrides[get_current_user] = override_get_current_user

    # Update one of the students with a phone number so we hit lines 75-78
    student = db.query(models.Student).filter_by(id=test_students[0]).first()
    student.guardian_phone = "+1234567890"
    student.guardian2_phone = "+0987654321"
    db.commit()

    payload = [
        {"student_id": test_students[0], "is_present": False},
    ]

    response = client.post("/api/attendance/bulk", json=payload)
    assert response.status_code == 200

    # Check that it was actually logged correctly
    att = db.query(models.Attendance).filter_by(student_id=test_students[0]).first()
    assert att is not None
    assert att.is_present is False
