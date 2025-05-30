from typing import List, Optional
from senfast.api.app.utils_kml.kml_config import KMLConfigManager
from senfast.api.app.utils_kml.kml_utils import create_kml_from_config
from senfast.core.monitoring import logger
from fastapi import HTTPException

class KMLService:
    """Servicio centralizado para generación de KML"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_manager = KMLConfigManager(config_dir) if config_dir else KMLConfigManager()
    
    def generate_kml(self, endpoint_name: str, datos: List, filename: Optional[str] = None) -> tuple[str, str]:
        """
        Genera KML y devuelve contenido y nombre de archivo
        
        Returns:
            tuple: (kml_content, filename)
        """
        try:
            kml_content = create_kml_from_config(
                datos=datos,
                endpoint_name=endpoint_name,
                config_manager=self.config_manager
            )
            
            if not filename:
                config = self.config_manager.load_config(endpoint_name)
                filename = config.nombre_archivo_base
            
            return kml_content, filename
            
        except FileNotFoundError as e:
            logger.error(f"Configuración KML no encontrada para {endpoint_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Configuración KML no disponible para {endpoint_name}")
        except Exception as e:
            logger.error(f"Error generando KML para {endpoint_name}: {e}")
            raise HTTPException(status_code=500, detail="Error generando KML")
    
    def get_available_configs(self) -> List[str]:
        """Devuelve lista de configuraciones disponibles"""
        import os
        config_dir = self.config_manager.config_dir
        if not os.path.exists(config_dir):
            return []
        
        configs = []
        for file in os.listdir(config_dir):
            if file.endswith(('.yaml', '.yml', '.json')):
                name = os.path.splitext(file)[0]
                configs.append(name)
        
        return configs