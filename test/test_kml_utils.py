import os
import tempfile
import pytest
from types import SimpleNamespace
from senfast.api.app.utils.kml_utils import create_kml_general

@pytest.fixture
def datos_mock():
    return [
        SimpleNamespace(
            component="SE-1", descripcio="Primero", latitud=41.1, longitud=2.1,
            clase="VERD", dayly_threshold=100, data_darrera_lectura="2025-05-25", lectura=0.2
        ),
        SimpleNamespace(
            component="SE-2", descripcio="Segundo", latitud=41.2, longitud=2.2,
            clase="VERMELL", dayly_threshold=80, data_darrera_lectura="2025-05-24", lectura=0.8
        ),
        SimpleNamespace(
            component="SE-3", descripcio="Sin datos", latitud=41.3, longitud=2.3,
            clase="ALTRE", dayly_threshold=50, data_darrera_lectura="2025-05-23", lectura=1.2
        ),
    ]

@pytest.fixture
def campos():
    return {
        "component": "string",
        "descripcio": "string",
        "latitud": "double",
        "longitud": "double",
        "clase": "string",
        "dayly_threshold": "integer",
        "data_darrera_lectura": "string",
        "lectura": "double"
    }

@pytest.fixture
def config_simbologia(tmp_path):
    # Simula iconos en un directorio temporal
    icon_dir = tmp_path
    icons = [
        ("Sense activacions", "icon_verd.svg"),
        ("Amb activacions", "icon_vermell.svg"),
        ("Sense dades", "icon_gris.svg"),
    ]
    config = []
    for id_style, fname in icons:
        path = os.path.join(icon_dir, fname)
        with open(path, "w") as f:
            f.write("ICON")
        config.append({"id": id_style, "icon_path": path})
    return config

@pytest.fixture
def asigna_estilo():
    def _fn(obj, config):
        if obj.clase == "VERD":
            return "Sense activacions"
        elif obj.clase == "VERMELL":
            return "Amb activacions"
        else:
            return "Sense dades"
    return _fn

def test_kml_general(datos_mock, campos, config_simbologia, asigna_estilo):
    kml = create_kml_general(
        datos=datos_mock,
        campos=campos,
        config_simbologia=config_simbologia,
        nombre_schema="TestSchema",
        nombre_doc="TestDoc",
        desc_doc="Test description",
        funcion_asignacion_estilo=asigna_estilo
    )
    # Comprueba que hay 3 estilos (uno por cada tipo)
    assert '<Style id="Sense activacions">' in kml
    assert '<Style id="Amb activacions">' in kml
    assert '<Style id="Sense dades">' in kml
    # Comprueba los styleUrl en los placemarks
    assert "#Sense activacions" in kml
    assert "#Amb activacions" in kml
    assert "#Sense dades" in kml
    # Comprueba que los componentes aparecen como nombres
    assert "SE-1" in kml
    assert "SE-2" in kml
    assert "SE-3" in kml
    # Comprueba que las coordenadas están en el KML
    assert "2.1,41.1" in kml
    assert "2.2,41.2" in kml
    assert "2.3,41.3" in kml
    # Comprueba que el schema y la descripción están
    assert "TestSchema" in kml
    assert "TestDoc" in kml
    assert "Test description" in kml