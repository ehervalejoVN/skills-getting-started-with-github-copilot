from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    activities.clear()
    activities.update(original)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities_returns_all():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity_success():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    new_email = "new_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    assert new_email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {new_email} for {activity}"


def test_signup_already_signed_up_returns_400():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found_returns_404():
    # Arrange
    client = TestClient(app)
    activity = "Nonexistent Activity"
    email = "x@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_success():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity}"


def test_unregister_participant_not_found_returns_404():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = "not_in_activity@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_activity_not_found_returns_404():
    # Arrange
    client = TestClient(app)
    activity = "No Activity"
    email = "x@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
