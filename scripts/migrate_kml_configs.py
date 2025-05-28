"""
Script para migrar las configuraciones hardcodeadas a archivos YAML
"""
import os
import yaml
from pathlib import Path

def create_config_directory():
    """Crea el directorio de configuraciones si no existe"""
    config_dir = Path("configurations/kml")
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def create_sobreeixidors_config():
    """Crea la configuración para sobreeixidors"""
    return {
        "nombre_schema": "kmlTERRASSA_Sobreeixidors",
        "nombre_doc": "Dades SENTILO Terrassa - Sobreeixidors -",
        "desc_doc": "KML amb la informació relativa als sobreeixidors instal·lats a la ciutat",
        "nombre_archivo_base": "Sobreeixidors",
        "campos": {
            "component": "string",
            "descripcio": "string",
            "latitud": "double",
            "longitud": "double",
            "clase": "string",
            "dayly_threshold": "integer",
            "data_darrera_lectura": "string",
            "lectura": "double"
        },
        "campo_clasificacion": "clase",
        "estilo_por_defecto": "Sense dades",
        "mapeo_estilos": {
            "VERD": "Sense activacions",
            "VERMELL": "Amb activacions"
        },
        "estilos": [
            {
                "id": "Sense activacions",
                "icon_path": "sobreeixidors/icon_sobreeixidor_poi_verd.svg",
                "label_scale": "0.0",
                "icon_scale": "1.0"
            },
            {
                "id": "Amb activacions", 
                "icon_path": "sobreeixidors/icon_sobreeixidor_poi_vermell.svg",
                "label_scale": "0.0",
                "icon_scale": "1.0"
            },
            {
                "id": "Sense dades",
                "icon_path": "sobreeixidors/icon_sobreeixidor_poi_gris.svg", 
                "label_scale": "0.0",
                "icon_scale": "1.0"
            }
        ],
        "campos_descripcion": ["component", "descripcio", "data_darrera_lectura"]
    }

def create_taigua_configs():
    """Crea las configuraciones para TAIGUA"""
    configs = {}
    
    # Sensores de presión
    configs["sensors_pressio"] = {
        "nombre_schema": "kmlTAIGUA_SensorsPressio",
        "nombre_doc": "Dades SENTILO Terrassa - Sensors de pressió -",
        "desc_doc": "KML amb la informació relativa als sensors de pressió de TAIGUA",
        "nombre_archivo_base": "TAIGUA_SensorsPressio",
        "campos": {
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
        },
        "campo_clasificacion": "color",
        "estilo_por_defecto": "Sense Dades",
        "mapeo_estilos": {
            "VERD": "En funcionament",
            "GROC": "Dades més antigues de 2 dies",
            "TARONJA": "Amb dades negatives", 
            "VERMELL": "Menys 20% bateria",
            "GRIS": "Ubicació"
        },
        "estilos": [
            {"id": "En funcionament", "icon_path": "taigua/icona_sensor_pressio_verd.svg"},
            {"id": "Dades més antigues de 2 dies", "icon_path": "taigua/icona_sensor_pressio_groc.svg"},
            {"id": "Amb dades negatives", "icon_path": "taigua/icona_sensor_pressio_taronja.svg"},
            {"id": "Menys 20% bateria", "icon_path": "taigua/icona_sensor_pressio_vermell.svg"},
            {"id": "Ubicació", "icon_path": "taigua/icona_sensor_pressio_ubicacio.svg"},
            {"id": "Sense Dades", "icon_path": "taigua/icona_sensor_pressio_gris.svg"}
        ],
        "campos_descripcion": ["serial_number", "proveidor", "bateria_nivell", "pressio"]
    }
    
    # Gateways
    configs["gateways"] = {
        "nombre_schema": "kmlTAIGUA_Gateways",
        "nombre_doc": "Dades SENTILO Terrassa - Gateways -", 
        "desc_doc": "KML amb la informació relativa als gateways de TAIGUA",
        "nombre_archivo_base": "TAIGUA_Gateways",
        "campos": {
            "id_gateway": "string",
            "nom": "string",
            "latitud": "double", 
            "longitud": "double",
            "data_ultim_event": "string",
            "connectat": "string"
        },
        "campo_clasificacion": "connectat",
        "estilo_por_defecto": "Fora de servei",
        "mapeo_estilos": {
            "S": "En servei",
            "N": "Fora de servei"
        },
        "estilos": [
            {"id": "En servei", "icon_path": "taigua/icona_gateway_en_servei.svg"},
            {"id": "Fora de servei", "icon_path": "taigua/icona_gateway_fora_servei.svg"}
        ],
        "campos_descripcion": ["id_gateway", "nom", "data_ultim_event"]
    }
    
    # Comptadors
    configs["comptadors"] = {
        "nombre_schema": "kmlSentiloComptadors",
        "nombre_doc": "Dades SENTILO Terrassa - Comptadors d'Aigua -",
        "desc_doc": "KML amb la informació dels sensors públics de la ciutat de Terrassa amb dades referents a comptadors d'aigua",
        "nombre_archivo_base": "TAIGUA_Comptadors",
        "campos": {
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
        },
        "campo_clasificacion": "classificacio",
        "estilo_por_defecto": "sentiloComptadorsAiguaTerrassa_0",
        "mapeo_estilos": {
            "0": "sentiloComptadorsAiguaTerrassa_0",
            "1": "sentiloComptadorsAiguaTerrassa_1", 
            "2": "sentiloComptadorsAiguaTerrassa_2",
            "3": "sentiloComptadorsAiguaTerrassa_3"
        },
        "estilos": [
            {"id": "sentiloComptadorsAiguaTerrassa_0", "icon_path": "taigua/icona_comptador_0.svg"},
            {"id": "sentiloComptadorsAiguaTerrassa_1", "icon_path": "taigua/icona_comptador_1.svg"},
            {"id": "sentiloComptadorsAiguaTerrassa_2", "icon_path": "taigua/icona_comptador_2.svg"},
            {"id": "sentiloComptadorsAiguaTerrassa_3", "icon_path": "taigua/icona_comptador_3.svg"}
        ],
        "campos_descripcion": ["serial_number", "adreca"]
    }
    
    return configs

def main():
    """Función principal de migración"""
    print("Iniciando migración de configuraciones KML...")
    
    # Crear directorio
    config_dir = create_config_directory()
    print(f"Directorio de configuración: {config_dir}")
    
    # Crear configuraciones
    configs = {
        "sobreeixidors": create_sobreeixidors_config(),
        **create_taigua_configs()
    }
    
    # Escribir archivos
    for name, config in configs.items():
        config_file = config_dir / f"{name}.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
        print(f"✓ Creado: {config_file}")
    
    print(f"\nMigración completada. {len(configs)} configuraciones creadas.")
    print("\nPasos siguientes:")
    print("1. Revisar y ajustar las rutas de iconos en los archivos YAML")
    print("2. Actualizar las importaciones en main.py para usar los nuevos routers")
    print("3. Probar los endpoints refactorizados")

if __name__ == "__main__":
    main()