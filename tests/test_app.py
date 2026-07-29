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


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
