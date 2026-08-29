from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original_activities = deepcopy(activities)
    test_client = TestClient(app)
    yield test_client
    activities.clear()
    activities.update(deepcopy(original_activities))


def test_unregister_participant_removes_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200, signup_response.text
    assert delete_response.status_code == 200, delete_response.text

    activities_payload = client.get("/activities").json()
    assert email not in activities_payload[activity_name]["participants"]
