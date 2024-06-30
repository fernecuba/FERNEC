from fastapi.testclient import TestClient
from main import get_app

app, _ = get_app()
client = TestClient(app)


def test_read_main():
    response = client.get("/v1/health")
    assert response.status_code == 200
