def test_data_barris(client, mock_barris):
    response = client.get("/api/all_barris?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2  
    assert data[0]["CODI_BARRI"] == 90