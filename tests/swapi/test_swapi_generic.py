from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_resource():
    response = client.get("/swapi/invalid")
    assert response.status_code == 400
    assert "não é suportado" in response.json()["detail"]
