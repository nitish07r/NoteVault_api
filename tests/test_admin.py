# ==================================================
# View Users
# ==================================================

def test_admin_can_view_all_users(
    client,
    admin_headers,
):

    response = client.get(
        "/admin/users",
        headers=admin_headers,
    )

    assert response.status_code == 200


def test_user_cannot_view_all_users(
    client,
    auth_headers,
):

    response = client.get(
        "/admin/users",
        headers=auth_headers,
    )

    assert response.status_code == 403


# ==================================================
# View Notes
# ==================================================

def test_admin_can_view_all_notes(
    client,
    admin_headers,
):

    response = client.get(
        "/admin/notes",
        headers=admin_headers,
    )

    assert response.status_code == 200


# ==================================================
# Delete Any Note
# ==================================================

def test_admin_can_delete_any_note(
    client,
    auth_headers,
    admin_headers,
    note_data,
):

    create_response = client.post(
        "/notes",
        headers=auth_headers,
        json=note_data,
    )

    note_id = create_response.json()["id"]

    response = client.delete(
        f"/admin/notes/{note_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


# ==================================================
# Create Admin
# ==================================================

def test_admin_can_create_admin(
    client,
    admin_headers,
):

    response = client.post(
        "/admin/create-admin",
        headers=admin_headers,
        json={
            "username": "newadmin",
            "email": "newadmin@gmail.com",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["role"] == "admin"


def test_user_cannot_create_admin(
    client,
    auth_headers,
):

    response = client.post(
        "/admin/create-admin",
        headers=auth_headers,
        json={
            "username": "newadmin",
            "email": "newadmin@gmail.com",
            "password": "Admin@123",
        },
    )

    assert response.status_code == 403