from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200, response.text

    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    assert delete_response.status_code == 200, delete_response.text

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
