from src.app import activities


def test_root_redirects_to_index(client):
    # Arrange: client fixture provided

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers.get("location") == "/static/index.html"


def test_get_activities_returns_initial(client):
    # Arrange: fresh activities via reset_activities fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_and_unregister_updates_activity(client):
    # Arrange
    activity_name = next(iter(activities))
    email = "tester@example.com"

    # Act: sign up
    resp_signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert signup succeeded and participant was added
    assert resp_signup.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Act: unregister
    resp_unreg = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert unregister succeeded and participant was removed
    assert resp_unreg.status_code == 200
    assert email not in activities[activity_name]["participants"]
