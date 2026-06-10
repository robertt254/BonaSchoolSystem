import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

from main import app
import models
import auth
from database import get_db

# Mocked user fixture
@pytest.fixture
def test_user(db):
    user = models.User(
        username="teststaff",
        hashed_password="hashed_testpassword",
        role="staff",
        name="Test Staff"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def authorized_client(client, test_user):
    def override_get_current_user():
        return test_user

    app.dependency_overrides[auth.get_current_user] = override_get_current_user
    yield client
    # Clean up after test
    app.dependency_overrides.pop(auth.get_current_user, None)

def test_apply_for_leave_success(authorized_client, test_user, db):
    """Test successful creation of a leave request"""
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=3)

    leave_data = {
        "leave_type": "sick",
        "start_date": str(start_date),
        "end_date": str(end_date),
        "reason": "Feeling unwell"
    }

    response = authorized_client.post("/api/leave/", json=leave_data)

    assert response.status_code == 200
    data = response.json()
    assert data["leave_type"] == "sick"
    assert data["status"] == "pending"
    assert data["staff_id"] == test_user.id

    # Verify in db
    db_leave = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == data["id"]).first()
    assert db_leave is not None
    assert db_leave.reason == "Feeling unwell"
    assert db_leave.status == "pending"

def test_apply_for_leave_end_date_before_start_date(authorized_client):
    """Test that applying for leave with end date before start date fails"""
    start_date = date.today() + timedelta(days=3)
    end_date = date.today() + timedelta(days=1)  # Before start_date

    leave_data = {
        "leave_type": "annual",
        "start_date": str(start_date),
        "end_date": str(end_date),
        "reason": "Vacation"
    }

    response = authorized_client.post("/api/leave/", json=leave_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "End date must be on or after start date"
