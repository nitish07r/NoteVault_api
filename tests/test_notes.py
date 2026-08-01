# ==================================================
# Create Note
# ==================================================

def test_create_note(
    client,
    auth_headers,
    note_data,
):

    # Arrange & Act
    response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    # Assert
    assert response.status_code == 201

    data = response.json()

    assert data["name"] == note_data["name"]
    assert data["description"] == note_data["description"]
    assert data["priority"] == note_data["priority"]

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


# ==================================================
# Get My Notes
# ==================================================

def test_get_my_notes(
    client,
    auth_headers,
    note_data,
):

    # Arrange
    client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    # Act
    response = client.get(
        "/notes",
        headers=auth_headers,
    )

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

    note = data["items"][0]

    assert note["name"] == note_data["name"]
    assert note["description"] == note_data["description"]
    assert note["priority"] == note_data["priority"]


# ==================================================
# Get Note By ID
# ==================================================

def test_get_note_by_id(
    client,
    auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    # Act
    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    # Assert
    assert response.status_code == 200

    note = response.json()

    assert note["id"] == note_id
    assert note["name"] == note_data["name"]
    assert note["description"] == note_data["description"]
    assert note["priority"] == note_data["priority"]


# ==================================================
# Update Note
# ==================================================

def test_update_note(
    client,
    auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    updated_note = {
        "name": "Updated Backend Notes",
        "priority": 1,
    }

    # Act
    response = client.patch(
        f"/notes/{note_id}",
        headers=auth_headers,
        json=updated_note,
    )

    # Assert
    assert response.status_code == 200

    note = response.json()

    assert note["name"] == "Updated Backend Notes"
    assert note["priority"] == 1

    # Description should remain unchanged.
    assert note["description"] == note_data["description"]


# ==================================================
# Delete Note
# ==================================================

def test_delete_note(
    client,
    auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    # Act
    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    # Assert
    assert response.status_code == 200

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


# ==================================================
# Authorization Tests
# ==================================================

def test_user_cannot_access_another_users_note(
    client,
    auth_headers,
    second_auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    # Act
    response = client.get(
        f"/notes/{note_id}",
        headers=second_auth_headers,
    )

    # Assert
    assert response.status_code == 404


def test_user_cannot_update_another_users_note(
    client,
    auth_headers,
    second_auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/notes/{note_id}",
        headers=second_auth_headers,
        json={
            "name": "Hacked",
        },
    )

    # Assert
    assert response.status_code == 404


def test_user_cannot_delete_another_users_note(
    client,
    auth_headers,
    second_auth_headers,
    note_data,
):

    # Arrange
    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    # Act
    response = client.delete(
        f"/notes/{note_id}",
        headers=second_auth_headers,
    )

    # Assert
    assert response.status_code == 404