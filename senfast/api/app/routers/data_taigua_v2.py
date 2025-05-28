from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import Optional, List

from senfast.core.config import get_settings
from senfast.core.monitoring import logger
from senfast.api.app.utils_kml.kml_config import KMLConfigManager
from senfast.api.app.utils_kml.kml_utils_v2 import create_kml_from_config
from senfast.api.app.repositories.taigua_repository import (
    obtener_sensors_pressio,
    obtener_gateways,
    obtener_comptadors,
)

router = APIRouter(prefix="/taigua", tags=["Dades TAIGUA"])
settings = get_settings()

class XMLResponse(Response):
    media_type = "application/xml"

class TaiguaService:
    def __init__(self):
        self.kml_config_manager = KMLConfigManager()
    
    @staticmethod
    def validate_token(token: str) -> bool:
        return token == "valor_valido"  # Sustituir por lógica real
    
    def generate_kml(self, endpoint_name: str, datos: List) -> str:
        """Genera KML usando configuración externa"""
        try:
            return create_kml_from_config(
                datos=datos,
                endpoint_name=endpoint_name,
                config_manager=self.kml_config_manager
            )
        except FileNotFoundError as e:
            logger.error(f"Configuración KML no encontrada para {endpoint_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Configuración KML no disponible para {endpoint_name}")
        except Exception as e:
            logger.error(f"Error generando KML para {endpoint_name}: {e}")
            raise HTTPException(status_code=500, detail="Error generando KML")

# Instancia del servicio
taigua_service = TaiguaService()

@router.get("/kml_sensors_pressio", response_class=XMLResponse)
async def kml_sensors_pressio(token: str, file: Optional[str] = None):
    """Endpoint KML para sensores de presión usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TaiguaService.validate_token(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    
    try:
        sensores = obtener_sensors_pressio()
        kml_content = taigua_service.generate_kml("sensors_pressio", sensores)
        
        config = taigua_service.kml_config_manager.load_config("sensors_pressio")
        filename = file or config.nombre_archivo_base
        
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f"attachment; filename=\"{filename}.kml\""
        }
        
        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_sensors_pressio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/kml_gateways", response_class=XMLResponse)
async def kml_gateways(token: str, file: Optional[str] = None):
    """Endpoint KML para gateways usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TaiguaService.validate_token(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    
    try:
        gateways = obtener_gateways()
        kml_content = taigua_service.generate_kml("gateways", gateways)
        
        config = taigua_service.kml_config_manager.load_config("gateways")
        filename = file or config.nombre_archivo_base
        
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f"attachment; filename=\"{filename}.kml\""
        }
        
        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_gateways: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/kml_comptadors", response_class=XMLResponse)
async def kml_comptadors(token: str, file: Optional[str] = None):
    """Endpoint KML para comptadors usando configuración externa"""
    if settings.ENVIRONMENT == "production" and not TaiguaService.validate_token(token):
        return XMLResponse(content="<?xml version='1.0' encoding='utf-8'?><kml></kml>", status_code=401)
    
    try:
        comptadors = obtener_comptadors()
        kml_content = taigua_service.generate_kml("comptadors", comptadors)
        
        config = taigua_service.kml_config_manager.load_config("comptadors")
        filename = file or config.nombre_archivo_base
        
        headers = {
            "Content-Type": "application/vnd.google-earth.kml+xml",
            "Content-Disposition": f"attachment; filename=\"{filename}.kml\""
        }
        
        return XMLResponse(content=kml_content, headers=headers)
        
    except Exception as e:
        logger.error(f"Error en kml_comptadors: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")