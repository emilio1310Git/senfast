import pytest
import tempfile
import os
from pathlib import Path
from types import SimpleNamespace
from senfast.api.app.utils_kml.kml_config import KMLConfigManager, KMLEndpointConfig
from senfast.api.app.utils_kml.kml_utils import create_kml_from_config

@pytest.fixture
def temp_config_dir():
    """Crea un directorio temporal con configuraciones de prueba"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        
        # Crear configuración de prueba para sobreeixidors
        config_content = """
nombre_schema: "test_schema"
nombre_doc: "Test Document"
desc_doc: "Test Description"
nombre_archivo_base: "test_file"

campos:
  component: "string"
  latitud: "double"
  longitud: "double"
  clase: "string"

campo_clasificacion: "clase"
estilo_por_defecto: "default"

mapeo_estilos:
  "VERD": "green_style"
  "VERMELL": "red_style"

estilos:
  - id: "green_style"
    icon_path: "icons/green.svg"
  - id: "red_style"
    icon_path: "icons/red.svg"
  - id: "default"
    icon_path: "icons/default.svg"
"""
        
        config_file = config_dir / "test_endpoint.yaml"
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        yield str(config_dir)

def test_kml_config_manager_load_config(temp_config_dir):
    """Test carga de configuración desde archivo YAML"""
    manager = KMLConfigManager(config_dir=temp_config_dir)
    config = manager.load_config("test_endpoint")
    
    assert config.nombre_schema == "test_schema"
    assert config.nombre_doc == "Test Document"
    assert len(config.estilos) == 3
    assert config.campo_clasificacion == "clase"

def test_style_assignment_function(temp_config_dir):
    """Test función de asignación de estilos"""
    manager = KMLConfigManager(config_dir=temp_config_dir)
    config = manager.load_config("test_endpoint")
    assign_func = manager.create_style_assignment_function(config)
    
    # Test con objeto mock
    obj_verde = SimpleNamespace(clase="VERD")
    obj_rojo = SimpleNamespace(clase="VERMELL")
    obj_otro = SimpleNamespace(clase="ALTRO")
    
    assert assign_func(obj_verde, []) == "green_style"
    assert assign_func(obj_rojo, []) == "red_style"
    assert assign_func(obj_otro, []) == "default"

def test_kml_generation_from_config(temp_config_dir):
    """Test generación completa de KML desde configuración"""
    # Datos de prueba
    datos = [
        SimpleNamespace(component="TEST-1", latitud=41.1, longitud=2.1, clase="VERD"),
        SimpleNamespace(component="TEST-2", latitud=41.2, longitud=2.2, clase="VERMELL"),
    ]
    
    manager = KMLConfigManager(config_dir=temp_config_dir)
    kml_content = create_kml_from_config(
        datos=datos,
        endpoint_name="test_endpoint",
        config_manager=manager
    )
    
    # Verificaciones básicas
    assert "test_schema" in kml_content
    assert "Test Document" in kml_content
    assert "TEST-1" in kml_content
    assert "TEST-2" in kml_content
    assert "2.1,41.1" in kml_content
    assert "2.2,41.2" in kml_content

def test_config_file_not_found():
    """Test manejo de archivo de configuración no encontrado"""
    manager = KMLConfigManager(config_dir="/nonexistent")
    
    with pytest.raises(FileNotFoundError):
        manager.load_config("nonexistent_endpoint")