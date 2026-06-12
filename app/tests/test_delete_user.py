import pytest


@pytest.fixture
def created_user(client):
    r = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    return r.get_json()


def test_delete_user(client, created_user):
    r = client.delete(f"/api/users/{created_user['id']}")
    assert r.status_code == 200
    assert r.get_json() == {"message": "User deleted"}


def test_deleted_user_is_gone(client, created_user):
    client.delete(f"/api/users/{created_user['id']}")
    r = client.get(f"/api/users/{created_user['id']}")
    assert r.status_code == 404
    r = client.get("/api/users")
    assert r.get_json() == {"users": []}


def test_delete_user_not_found(client):
    r = client.delete("/api/users/999")
    assert r.status_code == 404
    assert "error" in r.get_json()


def test_delete_user_twice(client, created_user):
    assert client.delete(f"/api/users/{created_user['id']}").status_code == 200
    r = client.delete(f"/api/users/{created_user['id']}")
    assert r.status_code == 404