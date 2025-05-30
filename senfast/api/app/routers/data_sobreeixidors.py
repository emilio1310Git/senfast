import time
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import Response
from typing import Optional, List 

from senfast.core.config import get_settings
from senfast.core.monitoring import logger
from senfast.core.metrics import REQUEST_COUNT, REQUEST_LATENCY
from senfast.api.app.utils.token_validator import TokenValidator
from senfast.api.app.utils_kml.kml_service import KMLService
from senfast.api.app.utils_kml.kml_config import KMLConfigManager
from senfast.api.app.utils_kml.kml_utils import create_kml_from_config
from senfast.api.app.models.models_sobreeixidors import DataSobreeixidor
from senfast.core.exceptions import DatabaseQueryError
from senfast.api.app.utils.error_utils import standard_http_exception
from senfast.api.app.repositories.sobreeixidors_repository import obtener_sobreeixidors

settings = get_settings()
router = APIRouter(prefix="/sobreeixidors", tags=["Dades Sobreeixidors"])

class XMLResponse(Response):
    media_type = "application/xml"

kml_service = KMLService()

@router.get("/kml", response_class=XMLResponse)
async def kml_sobreeixidors(token: Optional[str], file: Optional[str] = None):
    """
    Endpoint principal que genera KML con información de sobreeixidors
    usando configuración externa
    """
    """Endpoint KML para sensores de presión usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TokenValidator.validate(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    try:
        sobreeixidors = obtener_sobreeixidors(page=1, per_page=1000)
        kml_content, filename = kml_service.generate_kml("sobreeixidors", sobreeixidors)
        # no envio el nombre de fichero, usare por defecto el de la configuracion
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f'attachment; filename="{filename}.kml"'
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
    """
)
async def read_sobreeixidors(
    request: Request,
    page: int = Query(1, ge=1, description="Página (>=1)"),
    per_page: int = Query(100, ge=1, le=1000, description="Elementos por página (1-1000)")
):
    """Endpoint para obtener datos de sobreeixidors en formato JSON."""
    start = time.time()
    try:
        logger.info(f"Request ID: {request.state.request_id} - Solicitud recibida para obtener todos los sobreeixidors")
        sobreeixidors = obtener_sobreeixidors(page, per_page)
        REQUEST_COUNT.labels(endpoint="/all_sobreeixidors", method="GET", status_code=200).inc()
        REQUEST_LATENCY.labels(endpoint="/all_sobreeixidors", method="GET").observe(time.time() - start)
        return sobreeixidors
        
    except DatabaseQueryError as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error al obtener todos los sobreeixidors: {str(e)}")
        raise DatabaseQueryError(detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        REQUEST_COUNT.labels(endpoint="/all_sobreeixidors", method="GET", status_code=500).inc()
        raise standard_http_exception("Error interno del servidor")