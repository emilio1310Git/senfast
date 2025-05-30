from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import Optional, List

from senfast.core.config import get_settings
from senfast.core.monitoring import logger
from senfast.api.app.utils.token_validator import TokenValidator
from senfast.api.app.utils_kml.kml_service import KMLService
from senfast.api.app.repositories.taigua_repository import (
    obtener_sensors_pressio,
    obtener_gateways,
    obtener_comptadors,
)

router = APIRouter(prefix="/taigua", tags=["Dades TAIGUA"])
settings = get_settings()

class XMLResponse(Response):
    media_type = "application/xml"

kml_service = KMLService()

@router.get("/kml_sensors_pressio", response_class=XMLResponse)
async def kml_sensors_pressio(token: str, file: Optional[str] = None):
    """Endpoint KML para sensores de presión usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TokenValidator.validate(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    
    try:
        sensores = obtener_sensors_pressio()
        kml_content, filename = kml_service.generate_kml("sensors_pressio", sensores)
        # no envio el nombre de fichero, usare por defecto el de la configuracion
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f'attachment; filename="{filename}.kml"'
        }

        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_sensors_pressio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/kml_gateways", response_class=XMLResponse)
async def kml_gateways(token: str, file: Optional[str] = None):
    """Endpoint KML para gateways usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TokenValidator.validate(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    
    try:
        gateways = obtener_gateways()
        kml_content, filename = kml_service.generate_kml("gateways", gateways)
         # no envio el nombre de fichero, usare por defecto el de la configuracion
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f'attachment; filename="{filename}.kml"'
        }

        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_gateways: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/kml_comptadors", response_class=XMLResponse)
async def kml_comptadors(token: str, file: Optional[str] = None):
    """Endpoint KML para comptadors usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TokenValidator.validate(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    try:
        comptadors = obtener_comptadors()
        kml_content, filename = kml_service.generate_kml("comptadors", comptadors)
         # no envio el nombre de fichero, usare por defecto el de la configuracion
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f'attachment; filename="{filename}.kml"'
        }

        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_comptadors: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")