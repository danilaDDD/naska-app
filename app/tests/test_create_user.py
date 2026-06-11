def test_create_user_valid(client):
    r = client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_create_user_missing_name(client):
    r = client.post("/api/users", json={"email": "no-name@example.com"})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_create_user_duplicate_email(client):
    client.post("/api/users", json={"name": "Alice", "email": "alice@example.com"})
    r = client.post("/api/users", json={"name": "Bob", "email": "alice@example.com"})
    assert r.status_code == 400
    errors = r.get_json()["error"]
    assert any("Email already exists" in str(e) for e in errors)