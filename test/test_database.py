from senfast.api.app.db import database

def test_connection_pool_init_and_close():
    pool = database.create_connection_pool()
    assert pool is not None
    pool.close()

def test_get_db_connection(mock_pool):
    with database.get_db_connection() as conn:
        assert conn is not None
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            row = cursor.fetchone()
            assert row[0] == 1

def test_health_endpoint(client):
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data and data["database"] == "ok"
    assert "pool" in data