# import pytest
# from fastapi.testclient import TestClient
# from senfast.api.app.main import app

# client = TestClient(app)

def test_kml_endpoint_requires_token(client):
    response = client.get("/sobreeixidors/kml?token=INVALID")
    assert response.status_code == 401

def test_all_sobreeixidors_pagination(client):
    response = client.get("/sobreeixidors/all_sobreeixidors?page=1&per_page=2")
    assert response.status_code == 200
    assert isinstance(response.json(), list)