def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 9
    assert expected_activity in data


def test_get_activities_returns_participant_lists(client):
    # Arrange
    expected_participant = "michael@mergington.edu"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_participant in data["Chess Club"]["participants"]
    assert isinstance(data["Chess Club"]["participants"], list)
