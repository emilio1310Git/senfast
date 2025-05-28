from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from typing import List, Dict, Any
from senfast.core.kml_config import KMLConfigManager
from senfast.api.app.services.kml_service import KMLService
from senfast.core.monitoring import logger

router = APIRouter(prefix="/admin_kml", tags=["Administration"])
security = HTTPBearer()

def verify_admin_token(token: str = Depends(security)):
    """Verificación básica de token de administrador"""
    # Implementar verificación real aquí
    if token.credentials != "admin_token":
        raise HTTPException(status_code=401, detail="Token de administrador inválido")
    return token

@router.get("/kml/configs", dependencies=[Depends(verify_admin_token)])
async def list_kml_configs() -> Dict[str, Any]:
    """Lista todas las configuraciones KML disponibles"""
    try:
        kml_service = KMLService()
        configs = kml_service.get_available_configs()
        
        details = {}
        for config_name in configs:
            try:
                config = kml_service.config_manager.load_config(config_name)
                details[config_name] = {
                    "nombre_doc": config.nombre_doc,
                    "desc_doc": config.desc_doc,
                    "campos_count": len(config.campos),
                    "estilos_count": len(config.estilos),
                    "campo_clasificacion": config.campo_clasificacion
                }
            except Exception as e:
                details[config_name] = {"error": str(e)}
        
        return {
            "total_configs": len(configs),
            "configs": details
        }
    except Exception as e:
        logger.error(f"Error listando configuraciones KML: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/kml/config/{config_name}", dependencies=[Depends(verify_admin_token)])
async def get_kml_config(config_name: str) -> Dict[str, Any]:
    """Obtiene detalles de una configuración específica"""
    try:
        config_manager = KMLConfigManager()
        config = config_manager.load_config(config_name)
        
        return {
            "config_name": config_name,
            "config": config.dict()
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Configuración '{config_name}' no encontrada")
    except Exception as e:
        logger.error(f"Error obteniendo configuración {config_name}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/kml/validate/{config_name}", dependencies=[Depends(verify_admin_token)])
async def validate_kml_config(config_name: str) -> Dict[str, Any]:
    """Valida una configuración KML sin generar el archivo completo"""
    try:
        config_manager = KMLConfigManager()
        config = config_manager.load_config(config_name)
        
        # Validaciones básicas
        errors = []
        warnings = []
        
        # Verificar que existen los archivos de iconos
        for estilo in config.estilos:
            # Aquí podrías verificar si el archivo existe
            pass
        
        # Verificar coherencia en mapeo de estilos
        estilos_ids = {e.id for e in config.estilos}
        for valor, estilo_id in config.mapeo_estilos.items():
            if estilo_id not in estilos_ids:
                errors.append(f"Estilo '{estilo_id}' referenciado en mapeo pero no definido")
        
        if config.estilo_por_defecto not in estilos_ids:
            errors.append(f"Estilo por defecto '{config.estilo_por_defecto}' no definido")
        
        return {
            "config_name": config_name,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Configuración '{config_name}' no encontrada")
    except Exception as e:
        logger.error(f"Error validando configuración {config_name}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")