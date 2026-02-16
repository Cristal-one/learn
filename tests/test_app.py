from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    # Verify added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess Club/signup?email=dup@mergington.edu")
    # Second should fail
    response = client.post("/activities/Chess Club/signup?email=dup@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_remove_participant_success():
    # Add first
    client.post("/activities/Chess Club/signup?email=removeme@mergington.edu")
    # Remove
    response = client.delete("/activities/Chess Club/participants/removeme@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Removed" in result["message"]
    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "removeme@mergington.edu" not in data["Chess Club"]["participants"]

def test_remove_participant_not_found():
    response = client.delete("/activities/Chess Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Participant not found" in result["detail"]

def test_remove_invalid_activity():
    response = client.delete("/activities/Invalid Activity/participants/test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]