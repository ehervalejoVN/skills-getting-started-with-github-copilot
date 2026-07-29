from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import activities, app, reset_activities_db


@pytest.fixture(autouse=True)
def reset_activities():
    reset_activities_db()
    yield
    reset_activities_db()


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)

    activity = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"
    response = client.delete(path, params={"email": email})

    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity}"
