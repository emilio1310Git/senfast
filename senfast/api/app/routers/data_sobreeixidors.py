# Endpoints
import os
from fastapi import APIRouter, HTTPException, status, Request , Query, Depends, Path
from fastapi.responses import Response
from typing import Optional, List 
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, ValidationError, field_validator, Field
import oracledb
import xml.etree.ElementTree as ET
from xml.dom import minidom

import time

from senfast.core.config import get_settings
from senfast.api.app.db.querys.read_query_sobreeixidors import read_query_sobreeixidors
from senfast.core.monitoring import logger
from senfast.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

from senfast.api.app.db.models.models_sobreeixidors import DataSobreeixidor
from senfast.api.app.db.database import get_db_cursor, validate_table_name, get_connection_pool
from senfast.core.exceptions import TableNotFoundError, GeometryColumnNotFoundError, DatabaseQueryError
from senfast.api.app.utils.kml_utils import create_kml_general
from senfast.api.app.utils.error_utils import standard_http_exception
from senfast.api.app.repositories.sobreeixidors_repository import SobreeixidorsRepository


settings = get_settings()
router = APIRouter(prefix="/sobreeixidors", tags=["Dades Sobreeixidors"])
class XMLResponse(Response):
    media_type = "application/xml"
class SobreeixidorsService:
    def __init__(self, db_pool):
        # self.db_pool = db_pool
        pass
    
    @staticmethod
    def get_all_sobreeixidors(page: int, per_page: int) -> List[DataSobreeixidor]:
        return SobreeixidorsRepository.get_all(page, per_page)

    @staticmethod
    def validate_token(token: str) -> bool:
        # Implementación real de validación del token
        # Por ejemplo, comprobar contra base de datos, JWT, etc.
        return token == "valor_valido"  # Sustituir por la lógica real
    
    
# Endpoints de la API
@router.get("/kml", response_class=XMLResponse)
async def kml_sobreeixidors(token: Optional[str], file: Optional[str] = None):
    """
    Endpoint principal que genera KML con información de sobreeixidors
    
    Parameters:
    - file: Nombre del archivo (opcional)
    """
    
    if settings.ENVIRONMENT == "production" and not SobreeixidorsService.validate_token(token):
        logger.warning("Token invàlido en acceso a /sobreeixidors/kml")
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    try:
        sobreeixidors = SobreeixidorsService.get_all_sobreeixidors(page=1, per_page=1000)
        campos = {
            "component": "string",
            "descripcio": "string",
            "latitud": "double",
            "longitud": "double",
            "clase": "string",
            "dayly_threshold": "integer",
            "data_darrera_lectura": "string",
            "lectura": "double"
        }
        ICON_PATH = settings.PATH_ICONES_SOBREEIXIDORS
        config_simbologia = [
            {"id": "Sense activacions", "icon_path": os.path.join(ICON_PATH, "icon_sobreeixidor_poi_verd.svg")},
            {"id": "Amb activacions", "icon_path": os.path.join(ICON_PATH, "icon_sobreeixidor_poi_vermell.svg")},
            {"id": "Sense dades", "icon_path": os.path.join(ICON_PATH, "icon_sobreeixidor_poi_gris.svg")},
        ]
        def asigna_estilo(obj, config):
            if obj.clase == "VERD":
                return "Sense activacions"
            elif obj.clase == "VERMELL":
                return "Amb activacions"
            else:
                return "Sense dades"
        kml_content = create_kml_general(
            datos=sobreeixidors,
            campos=campos,
            config_simbologia=config_simbologia,
            nombre_schema="kmlTERRASSA_Sobreeixidors",
            nombre_doc="Dades SENTILO Terrassa - Sobreeixidors -",
            desc_doc="KML amb la informació relativa als sobreexidors instal·lats a la ciutat",
            funcion_asignacion_estilo=asigna_estilo
        )
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f"attachment; filename=\"{file or 'Sobreeixidors'}.kml\""
        }
        return XMLResponse(content=kml_content, headers=headers)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise standard_http_exception("Error interno del servidor")
    
@router.get(
    "/all_sobreeixidors",
    response_model=list[DataSobreeixidor],
    summary="Obtener todos los sobreeixidors",
    description="""
    Devuelve una lista completa de todos los sobreeixidors en formato JSON.

    - Parámetros:
        - page: página de la consulta (>=1)
        - per_page: elementos por página (1-1000)

    Ejemplo de uso:

    * Obtener todos los sobreeixidors: `/all_sobreeixidors`
    """
)
async def read_sobreexidors(
    request: Request,
    page: int = Query(1, ge=1, description="Página (>=1)"),
    per_page: int = Query(100, ge=1, le=1000, description="Elementos por página (1-1000)")
    ):
    """Endpoint para obtener datos de sobreeixidors en formato JSON."""
    logger.critical("RUTA /all_sobreeixidors INICIADA")  # Log CRITICAL
    start = time.time()
    try:
        logger.info(f"Request ID: {request.state.request_id} - Solicitud recibida para obtener todos los sobreeixidors")
        sobreeixidors = SobreeixidorsService.get_all_sobreeixidors(page, per_page)
        REQUEST_COUNT.labels(endpoint="/all_sobreeixidors", method="GET", status_code=200).inc()
        REQUEST_LATENCY.labels(endpoint="/all_sobreeixidors", method="GET").observe(time.time() - start)
        return sobreeixidors
        
    except DatabaseQueryError as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error al obtener todos los sobreeixidors: {str(e)}")
        raise DatabaseQueryError(detail=str(e))
    except oracledb.OperationalError as e:
        logger.error(f"Request ID: {request.state.request_id} - Error de base de datos: {str(e)}", exc_info=True)
        raise DatabaseQueryError(detail=str(e))      
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        REQUEST_COUNT.labels(endpoint="/all_sobreeixidors", method="GET", status_code=500).inc()
        raise standard_http_exception("Error interno del servidor")





