import pytest


@pytest.fixture
def created_user(client):
    r = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    return r.get_json()

def test_update_user_not_found(client):
    r = client.put("/api/users/999", json={"name": "Ghost"})
    assert r.status_code == 404


@pytest.mark.parametrize("payload", [
    {"name": 123},
    {"email": 456},
    {"name": [], "email": {}},
    {"name": None, "email": True},
])
def test_update_user_invalid_data(client, created_user, payload):
    r = client.put(f"/api/users/{created_user['id']}", json=payload)
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_update_user_duplicate_email(client, created_user):
    client.post("/api/users", json={"name": "Bob", "email": "bob@example.com"})
    r = client.put(f"/api/users/{created_user['id']}", json={"email": "bob@example.com"})
    assert r.status_code == 400
    errors = r.get_json()["error"]
    assert any("Email already exists" in str(e) for e in errors)