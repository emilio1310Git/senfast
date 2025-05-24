import pytest
from fastapi.testclient import TestClient
from senfast.api.app.main import app 
from unittest.mock import MagicMock
from contextlib import contextmanager

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_pool(monkeypatch):
    # Mock del cursor
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    # Mock de la conexión
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock del pool
    mock_pool_instance = MagicMock()
    mock_pool_instance.acquire.return_value = mock_conn

    # Parchar los métodos en el módulo database
    monkeypatch.setattr("senfast.api.app.db.database.get_connection_pool", lambda: mock_pool_instance)

    @contextmanager
    def fake_get_db_connection():
        yield mock_conn

    monkeypatch.setattr("senfast.api.app.db.database.get_db_connection", fake_get_db_connection)
    return mock_pool_instance

@pytest.fixture
def mock_barris(monkeypatch):
    from senfast.api.app.db import database

    # Mock del cursor
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    # Simula una lista de tuplas como devolvería fetchall()
    mock_cursor.fetchall.return_value = [
        (90, "BARRI MOCK 1"),
        (91, "BARRI MOCK 2"),
    ]
    # Simula los nombres de las columnas
    mock_cursor.description = [("CODI_BARRI",), ("NOM_BARRI",)]

    # Mock de la conexión
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock del pool
    mock_pool_instance = MagicMock()
    mock_pool_instance.acquire.return_value = mock_conn

    # Parchar los métodos en el módulo database
    monkeypatch.setattr(database, "get_connection_pool", lambda: mock_pool_instance)

    @contextmanager
    def fake_get_db_connection():
        yield mock_conn

    monkeypatch.setattr(database, "get_db_connection", fake_get_db_connection)
    return mock_pool_instance