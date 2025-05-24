# import pytest
# from unittest.mock import MagicMock
# from contextlib import contextmanager
def test_healthcheck_with_mock(client, mock_pool):
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["database"] == "ok"
    assert data["pool"]["open"] is True