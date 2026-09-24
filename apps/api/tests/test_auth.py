from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "pytest-user@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user"]["email"] == "pytest-user@example.com"
    assert data["user"]["name"] == "Test User"
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]


def test_login_user():
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login Test",
            "email": "pytest-login@example.com",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "pytest-login@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]


def test_protected_endpoint_requires_authentication():
    response = client.get("/api/v1/users/me")

    assert response.status_code in (401, 403)
