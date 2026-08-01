# ==================================================
# Register
# ==================================================

def test_register_success(client, user_data):

    response = client.post(
        "/register",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["role"] == "user"

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_register_duplicate_email(client, registered_user, user_data):

    response = client.post(
        "/register",
        json={
            "username": "anotheruser",
            "email": user_data["email"],
            "password": "Password@123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_duplicate_username(client, registered_user, user_data):

    response = client.post(
        "/register",
        json={
            "username": user_data["username"],
            "email": "another@gmail.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


# ==================================================
# Login
# ==================================================

def test_login_success(client, registered_user, user_data):

    response = client.post(
        "/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, registered_user, user_data):

    response = client.post(
        "/login",
        data={
            "username": user_data["email"],
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"