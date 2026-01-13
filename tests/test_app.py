from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    # Use a unique email to avoid duplicate registration
    response = client.post("/activities/Chess Club/signup?email=tester1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate():
    email = "tester2@mergington.edu"
    # First signup should succeed
    response1 = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response1.status_code == 200
    # Second signup should fail
    response2 = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
