import pytest


@pytest.fixture
def two_users(client):
    client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    client.post("/api/users", json={"name": "Bob", "email": "bob@example.com"})


def test_get_users_empty(client):
    r = client.get("/api/users")
    assert r.status_code == 200
    assert r.get_json() == {"users": []}


def test_get_users(client, two_users):
    r = client.get("/api/users")
    assert r.status_code == 200
    assert len(r.get_json()["users"]) == 2


def test_get_user_by_id(client, two_users):
    r = client.get("/api/users/1")
    assert r.status_code == 200
    data = r.get_json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_get_user_by_id_not_found(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404
    assert "error" in r.get_json()