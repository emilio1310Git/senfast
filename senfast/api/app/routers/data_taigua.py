from fastapi import APIRouter
from fastapi.responses import Response
from typing import Optional
import os

from senfast.api.app.utils.kml_utils import create_kml_general
from senfast.api.app.repositories.taigua_repository import (
    obtener_sensors_pressio,
    obtener_gateways,
    obtener_comptadors,
)

router = APIRouter(prefix="/taigua", tags=["Dades TAIGUA"])

ICON_PATH = "/ruta/static/icons_taigua/"  # Ajusta la ruta según tu estructura real

class XMLResponse(Response):
    media_type = "application/xml"

# --- Sensores de presión ---
@router.get("/kml_sensors_pressio", response_class=XMLResponse)
async def kml_sensors_pressio(token: str, file: Optional[str] = None):
    if token != "valor_valido":
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    sensores = obtener_sensors_pressio()
    campos = {
        "serial_number": "string",
        "proveidor": "string",
        "id_ubicacio": "string",
        "ubicacio": "string",
        "latitud": "double",
        "longitud": "double",
        "node": "string",
        "temps_nivell": "string",
        "bateria_nivell": "double",
        "temps_pressio": "string",
        "pressio": "double",
        "color": "string",
        "data_ini_ubicacio": "string",
        "tipus": "string"
    }
    config_simbologia = [
        {"id": "En funcionament", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_verd.svg")},
        {"id": "Dades més antigues de 2 dies", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_groc.svg")},
        {"id": "Amb dades negatives", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_taronja.svg")},
        {"id": "Menys 20% bateria", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_vermell.svg")},
        {"id": "Ubicació", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_ubicacio.svg")},
        {"id": "Sense Dades", "icon_path": os.path.join(ICON_PATH, "icona_sensor_pressio_gris.svg")}
    ]
    def asigna_estilo(sensor, config):
        color = getattr(sensor, "color", "").upper()
        if color == "VERD":
            return "En funcionament"
        elif color == "GROC":
            return "Dades més antigues de 2 dies"
        elif color == "TARONJA":
            return "Amb dades negatives"
        elif color == "VERMELL":
            return "Menys 20% bateria"
        elif color == "GRIS":
            return "Ubicació"
        else:
            return "Sense Dades"
    kml_content = create_kml_general(
        datos=sensores,
        campos=campos,
        config_simbologia=config_simbologia,
        nombre_schema="kmlTAIGUA_SensorsPressio",
        nombre_doc="Dades SENTILO Terrassa - Sensors de pressió -",
        desc_doc="KML amb la informació relativa als sensors de pressió de TAIGUA",
        funcion_asignacion_estilo=asigna_estilo
    )
    headers = {
        "Content-Type": "application/vnd.google-earth.kml+xml",
        "Content-Disposition": f"attachment; filename=\"{file or 'TAIGUA_SensorsPressio'}.kml\""
    }
    return XMLResponse(content=kml_content, headers=headers)

# --- Gateways ---
@router.get("/kml_gateways", response_class=XMLResponse)
async def kml_gateways(token: str, file: Optional[str] = None):
    if token != "valor_valido":
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    gateways = obtener_gateways()
    campos = {
        "id_gateway": "string",
        "nom": "string",
        "latitud": "double",
        "longitud": "double",
        "data_ultim_event": "string",
        "connectat": "string"
    }
    config_simbologia = [
        {"id": "En servei", "icon_path": os.path.join(ICON_PATH, "icona_gateway_en_servei.svg")},
        {"id": "Fora de servei", "icon_path": os.path.join(ICON_PATH, "icona_gateway_fora_servei.svg")},
    ]
    def asigna_estilo(gateway, config):
        return "En servei" if gateway.connectat == "S" else "Fora de servei"
    kml_content = create_kml_general(
        datos=gateways,
        campos=campos,
        config_simbologia=config_simbologia,
        nombre_schema="kmlTAIGUA_Gateways",
        nombre_doc="Dades SENTILO Terrassa - Gateways -",
        desc_doc="KML amb la informació relativa als gateways de TAIGUA",
        funcion_asignacion_estilo=asigna_estilo
    )
    headers = {
        "Content-Type": "application/vnd.google-earth.kml+xml",
        "Content-Disposition": f"attachment; filename=\"{file or 'TAIGUA_Gateways'}.kml\""
    }
    return XMLResponse(content=kml_content, headers=headers)

# --- Comptadors ---
@router.get("/kml_comptadors", response_class=XMLResponse)
async def kml_comptadors(token: str, file: Optional[str] = None):
    if token != "valor_valido":
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    comptadors = obtener_comptadors()
    campos = {
        "serial_number": "string",
        "comptador": "string",
        "contracte": "string",
        "adreca": "string",
        "ultima_lectura": "double",
        "ultim_consum": "double",
        "data_ultima_lectura": "string",
        "total_lectures": "int",
        "numero_lectures": "string",
        "classificacio": "int",
        "latitud": "double",
        "longitud": "double"
    }
    # Los iconos deben corresponder a los valores posibles de classificacio
    config_simbologia = [
        {"id": "sentiloComptadorsAiguaTerrassa_0", "icon_path": os.path.join(ICON_PATH, "icona_comptador_0.svg")},
        {"id": "sentiloComptadorsAiguaTerrassa_1", "icon_path": os.path.join(ICON_PATH, "icona_comptador_1.svg")},
        {"id": "sentiloComptadorsAiguaTerrassa_2", "icon_path": os.path.join(ICON_PATH, "icona_comptador_2.svg")},
        {"id": "sentiloComptadorsAiguaTerrassa_3", "icon_path": os.path.join(ICON_PATH, "icona_comptador_3.svg")},
    ]
    def asigna_estilo(comptador, config):
        idx = getattr(comptador, "classificacio", 0)
        return f"sentiloComptadorsAiguaTerrassa_{idx}"
    kml_content = create_kml_general(
        datos=comptadors,
        campos=campos,
        config_simbologia=config_simbologia,
        nombre_schema="kmlSentiloComptadors",
        nombre_doc="Dades SENTILO Terrassa - Comptadors d'Aigua -",
        desc_doc="KML amb la informació dels sensors públics de la ciutat de Terrassa amb dades referents a comptadors d'aigua",
        funcion_asignacion_estilo=asigna_estilo
    )
    headers = {
        "Content-Type": "application/vnd.google-earth.kml+xml",
        "Content-Disposition": f"attachment; filename=\"{file or 'TAIGUA_Comptadors'}.kml\""
    }
    return XMLResponse(content=kml_content, headers=headers)