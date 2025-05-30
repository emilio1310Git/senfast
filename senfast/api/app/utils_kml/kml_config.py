import json
import yaml
from typing import Dict, List, Any, Callable, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from senfast.core.config import get_settings
from senfast.core.monitoring import logger
class StyleConfig(BaseModel):
    """Configuración de un estilo individual"""
    id: str
    icon_path: str
    label_scale: str = "0.0"
    icon_scale: str = "1.0"

class KMLEndpointConfig(BaseModel):
    """Configuración completa para un endpoint KML"""
    # Metadatos del documento
    nombre_schema: str
    nombre_doc: str
    desc_doc: str
    
    # Campos de la tabla/modelo
    campos: Dict[str, str]  # campo -> tipo SQL
    
    # Configuración de estilos
    estilos: List[StyleConfig]
    
    # Mapeo de valores a estilos
    campo_clasificacion: str  # Campo que determina el estilo
    mapeo_estilos: Dict[str, str]  # valor -> style_id
    estilo_por_defecto: str = "Sense dades"
    
    # Configuración de nombres de archivo
    nombre_archivo_base: str
    
    # Función de descripción personalizada (opcional)
    campos_descripcion: Optional[List[str]] = None

class KMLConfigManager:
    """Gestor de configuraciones KML"""
    
    def __init__(self, config_dir: str = "configurations/kml"):
        self.settings = get_settings()
        if not self.settings.KML_CONFIG_DIR:
            self.config_dir = Path(config_dir)
            logger.debug(f"KML_CONFIG_DIR no está configurado, usando el por defecto {config_dir}")
        self.config_dir = Path(self.settings.KML_CONFIG_DIR)
        self.config_cache: Dict[str, KMLEndpointConfig] = {}
    
    def load_config(self, endpoint_name: str) -> KMLEndpointConfig:
        """Carga la configuración para un endpoint específico"""
        if endpoint_name in self.config_cache:
            return self.config_cache[endpoint_name]
        
        config_file = self.config_dir / f"{endpoint_name}.yaml"
        if not config_file.exists():
            config_file = self.config_dir / f"{endpoint_name}.json"
        
        if not config_file.exists():
            raise FileNotFoundError(f"No se encontró configuración para {endpoint_name}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_file.suffix == '.yaml':
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        
        # Resolver paths relativos de iconos
        for estilo in config_data.get('estilos', []):
            if not estilo['icon_path'].startswith('/'):
                # Path relativo, resolverlo desde la configuración
                base_path = getattr(self.settings, 'ICONS_BASE_PATH', '/static/icons/')
                estilo['icon_path'] = f"{base_path.rstrip('/')}/{estilo['icon_path']}"
        
        config = KMLEndpointConfig(**config_data)
        self.config_cache[endpoint_name] = config
        return config
    
    def create_style_assignment_function(self, config: KMLEndpointConfig) -> Callable:
        """Crea una función de asignación de estilos basada en la configuración"""
        def assign_style(obj, style_config_list):
            # Obtener el valor del campo de clasificación
            campo_valor = getattr(obj, config.campo_clasificacion, None)
            if campo_valor is None:
                return config.estilo_por_defecto
            
            # Convertir a string para la comparación
            campo_valor_str = str(campo_valor).upper()
            
            # Buscar en el mapeo
            return config.mapeo_estilos.get(campo_valor_str, config.estilo_por_defecto)
        
        return assign_style
    
    def create_description_function(self, config: KMLEndpointConfig) -> Callable:
        """Crea una función para generar descripciones basada en la configuración"""
        def create_description(obj) -> str:
            if config.campos_descripcion:
                parts = []
                for campo in config.campos_descripcion:
                    valor = getattr(obj, campo, "")
                    if valor:
                        parts.append(str(valor))
                return " - ".join(parts)
            else:
                # Descripción por defecto: todos los campos menos coordenadas
                parts = []
                for campo in config.campos.keys():
                    if campo not in ['latitud', 'longitud']:
                        valor = getattr(obj, campo, "")
                        if valor:
                            parts.append(str(valor))
                return " - ".join(parts)
        
        return create_description