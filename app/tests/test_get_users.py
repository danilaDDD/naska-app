import pytest


@pytest.fixture
def created_user(client):
    r = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    return r.get_json()


def test_get_users_empty(client):
    r = client.get("/api/users")
    assert r.status_code == 200
    assert r.get_json() == {"users": []}


def test_get_users_returns_created(client, created_user):
    client.post("/api/users", json={"name": "Bob", "email": "bob@example.com"})
    r = client.get("/api/users")
    assert r.status_code == 200
    users = r.get_json()["users"]
    assert len(users) == 2
    assert users[0] == created_user
    assert users[1]["name"] == "Bob"


def test_get_user_by_id(client, created_user):
    r = client.get(f"/api/users/{created_user['id']}")
    assert r.status_code == 200
    assert r.get_json() == created_user


def test_get_user_not_found(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404
    assert "error" in r.get_json()