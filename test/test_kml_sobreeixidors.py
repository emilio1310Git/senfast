from types import SimpleNamespace
def test_kml_sobreeixidors_endpoint(client, monkeypatch):
    """Test del endpoint KML refactorizado"""
    # Mock de los datos
    mock_data = [
        SimpleNamespace(
            component="SE-1", descripcio="Test", latitud=41.1, longitud=2.1,
            clase="VERD", dayly_threshold=100, data_darrera_lectura="2025-05-25", lectura=0.2
        )
    ]
    
    # Mock del repository
    monkeypatch.setattr(
        "senfast.api.app.repositories.sobreeixidors_repository.SobreeixidorsRepository.get_all",
        lambda page, per_page: mock_data
    )
    
    # Mock del config manager para evitar dependencia de archivos
    mock_config = {
        "nombre_schema": "test_schema",
        "nombre_doc": "Test Doc",
        "desc_doc": "Test Description",
        "nombre_archivo_base": "test_file",
        "campos": {"component": "string", "latitud": "double", "longitud": "double", "clase": "string"},
        "campo_clasificacion": "clase",
        "estilo_por_defecto": "default",
        "mapeo_estilos": {"VERD": "green"},
        "estilos": [{"id": "green", "icon_path": "green.svg"}]
    }
    
    def mock_load_config(endpoint_name):
        from senfast.api.app.utils_kml.kml_config import KMLEndpointConfig
        return KMLEndpointConfig(**mock_config)
    
    monkeypatch.setattr(
        "senfast.api.app.utils_kml.kml_config.KMLConfigManager.load_config",
        mock_load_config
    )
    
    # Test endpoint
    response = client.get("/sobreeixidors/kml?token=valor_valido")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert "SE-1" in response.text