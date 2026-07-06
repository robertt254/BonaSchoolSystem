from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


def test_health_check_success():
    """Test the health check endpoint when the database is successfully connected."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["system"] == "Bona School Backend API"
    assert data["db"] == "connected"
    assert "db_error" not in data


def test_health_check_db_error():
    """Test the health check endpoint when the database connection fails."""
    # We patch main.SessionLocal so that it raises an Exception
    with patch("main.SessionLocal") as mock_session_local:
        mock_session_local.side_effect = Exception("Simulated DB connection error")
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["system"] == "Bona School Backend API"
        assert data["db"] == "error"
        assert data["db_error"] == "Simulated DB connection error"
