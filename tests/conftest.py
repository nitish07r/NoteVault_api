import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
import database_models

from main import app


# ==================================================
# Test Database Configuration
# ==================================================

from config import TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ==================================================
# Override Database Dependency
# ==================================================

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[
    database.get_db
] = override_get_db


# ==================================================
# Database Setup
# ==================================================

@pytest.fixture(scope="session", autouse=True)
def setup_database():

    database_models.Base.metadata.create_all(bind=engine)

    yield

    database_models.Base.metadata.drop_all(bind=engine)


# ==================================================
# Clean Database Before Every Test
# ==================================================

@pytest.fixture(autouse=True)
def clean_database():

    db = TestingSessionLocal()

    db.query(database_models.Note).delete(
        synchronize_session=False
    )

    db.query(database_models.User).delete(
        synchronize_session=False
    )

    db.commit()
    db.close()


# ==================================================
# Test Client
# ==================================================

@pytest.fixture
def client():

    with TestClient(app) as client:
        yield client


# ==================================================
# User Fixtures
# ==================================================

@pytest.fixture
def user_data():

    return {
        "username": "nitish",
        "email": "nitish@gmail.com",
        "password": "Nitish@123",
    }


@pytest.fixture
def registered_user(client, user_data):

    client.post(
        "/register",
        json=user_data,
    )


@pytest.fixture
def auth_headers(
    client,
    registered_user,
    user_data,
):

    response = client.post(
        "/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ==================================================
# Second User Fixtures
# ==================================================

@pytest.fixture
def second_user_data():

    return {
        "username": "rahul",
        "email": "rahul@gmail.com",
        "password": "Rahul@123",
    }


@pytest.fixture
def second_registered_user(
    client,
    second_user_data,
):

    client.post(
        "/register",
        json=second_user_data,
    )


@pytest.fixture
def second_auth_headers(
    client,
    second_registered_user,
    second_user_data,
):

    response = client.post(
        "/login",
        data={
            "username": second_user_data["email"],
            "password": second_user_data["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ==================================================
# Admin Fixtures
# ==================================================

@pytest.fixture
def admin_data():

    return {
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "Admin@123",
    }


@pytest.fixture
def registered_admin(
    client,
    admin_data,
):

    client.post(
        "/register",
        json=admin_data,
    )


@pytest.fixture
def admin_headers(
    client,
    registered_admin,
    admin_data,
):

    db = TestingSessionLocal()

    admin = (
        db.query(database_models.User)
        .filter(
            database_models.User.email == admin_data["email"]
        )
        .first()
    )

    admin.role = "admin"

    db.commit()
    db.close()

    response = client.post(
        "/login",
        data={
            "username": admin_data["email"],
            "password": admin_data["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ==================================================
# Note Fixture
# ==================================================

@pytest.fixture
def note_data():

    return {
        "name": "Backend Notes",
        "description": "Learn FastAPI",
        "priority": 3,
    }