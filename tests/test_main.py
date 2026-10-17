
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_returns_application_details():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert data["application"] == "ResilientDeploy"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_version_endpoint():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"
