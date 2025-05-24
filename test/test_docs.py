# from fastapi.testclient import TestClient
# from senfast.api.app.main import get_application

# client = TestClient(get_application())

def test_docs_extra(client):
    response = client.get("/about")
    assert response.status_code == 200

def test_health(client):
    response = client.get("/health/")
    assert response.status_code == 200