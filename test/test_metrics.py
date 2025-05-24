def test_metrics(client):
    response = client.get("/metrics/")
    assert response.status_code == 200
    assert "senfast_db_up" in response.text 