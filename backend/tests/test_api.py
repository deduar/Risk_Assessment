import os
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("CELERY_BROKER_URL", "memory://")
os.environ.setdefault("CELERY_RESULT_BACKEND", "cache+memory://")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_get():
    r = client.post("/assessments", json={"company_name": "Acme", "country": "BE", "amount": 5000})
    assert r.status_code == 201
    aid = r.json()["id"]
    r2 = client.get(f"/assessments/{aid}")
    assert r2.status_code == 200
    assert r2.json()["company_name"] == "Acme"


def test_list():
    r = client.get("/assessments")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_not_found():
    r = client.get("/assessments/99999")
    assert r.status_code == 404