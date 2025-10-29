# tests/test_auth.py
from fastapi.testclient import TestClient

def test_login_form_and_me(client: TestClient):
    r = client.post("/jwt/login_form", data={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r2 = client.get("/jwt/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["sub"]  # id admina
    assert "ROLE_ADMIN" in data["roles"]

def test_protected_requires_auth(client: TestClient):
    r = client.get("/movies")  # router chroniony globalnie
    assert r.status_code in (401, 403)

def test_secure_ping_ok(client: TestClient):
    r = client.post("/jwt/login_form", data={"username": "admin", "password": "admin"})
    token = r.json()["access_token"]
    r2 = client.get("/secure/ping", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["ok"] is True
