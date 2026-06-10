import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app, _users  # noqa: E402


@pytest.fixture(autouse=True)
def clear_users():
    _users.clear()
    import main
    main._next_id = 1
    yield
    _users.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json() == {"message": "Hello, World!"}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_list_users_empty(client):
    r = client.get("/api/users")
    assert r.status_code == 200
    assert r.get_json() == {"users": []}


def test_create_user_success(client):
    r = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_create_user_missing_name(client):
    r = client.post("/api/users", json={"email": "no-name@example.com"})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_get_user(client):
    client.post("/api/users", json={"name": "Bob"})
    r = client.get("/api/users/1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Bob"


def test_get_user_not_found(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404


def test_delete_user(client):
    client.post("/api/users", json={"name": "Carol"})
    r = client.delete("/api/users/1")
    assert r.status_code == 200
    assert client.get("/api/users/1").status_code == 404


def test_delete_user_not_found(client):
    r = client.delete("/api/users/999")
    assert r.status_code == 404


def test_list_users_after_create(client):
    client.post("/api/users", json={"name": "Dave"})
    client.post("/api/users", json={"name": "Eve"})
    r = client.get("/api/users")
    assert r.status_code == 200
    assert len(r.get_json()["users"]) == 2