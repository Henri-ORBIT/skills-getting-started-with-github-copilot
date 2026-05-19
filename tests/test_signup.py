def test_signup_for_activity_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_same_student_to_different_activities_succeeds(client):
    # Arrange
    email = "multiclub@mergington.edu"

    # Act
    chess_response = client.post("/activities/Chess Club/signup", params={"email": email})
    drama_response = client.post("/activities/Drama Club/signup", params={"email": email})
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert chess_response.status_code == 200
    assert drama_response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Drama Club"]["participants"]
