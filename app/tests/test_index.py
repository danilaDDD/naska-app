def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json() == {"message": "Hello, World!"}