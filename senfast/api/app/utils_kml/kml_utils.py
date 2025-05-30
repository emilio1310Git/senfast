from xml.etree import ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Callable
from senfast.api.app.utils_kml.kml_config import KMLConfigManager, KMLEndpointConfig

def create_kml_from_config(
    datos: List,
    endpoint_name: str,
    config_manager: KMLConfigManager = None
) -> str:
    """
    Crea un KML basado completamente en configuración externa
    
    Args:
        datos: Lista de objetos con los datos
        endpoint_name: Nombre del endpoint para cargar su configuración
        config_manager: Gestor de configuración (opcional)
    
    Returns:
        String con el contenido XML del KML
    """
    if config_manager is None:
        config_manager = KMLConfigManager()
    
    config = config_manager.load_config(endpoint_name)
    
    # Crear funciones basadas en configuración
    assign_style_func = config_manager.create_style_assignment_function(config)
    create_desc_func = config_manager.create_description_function(config)
    
    # Convertir StyleConfig a formato esperado por create_kml_general
    config_simbologia = [
        {
            "id": estilo.id,
            "icon_path": estilo.icon_path,
            "label_scale": estilo.label_scale,
            "icon_scale": estilo.icon_scale
        }
        for estilo in config.estilos
    ]
    
    return create_kml_general(
        datos=datos,
        campos=config.campos,
        config_simbologia=config_simbologia,
        nombre_schema=config.nombre_schema,
        nombre_doc=config.nombre_doc,
        desc_doc=config.desc_doc,
        funcion_asignacion_estilo=assign_style_func,
        funcion_descripcion=create_desc_func
    )

def create_kml_general(
    datos: List,
    campos: Dict[str, str],
    config_simbologia: List[Dict],
    nombre_schema: str,
    nombre_doc: str,
    desc_doc: str,
    funcion_asignacion_estilo: Callable,
    funcion_descripcion: Callable = None,
) -> str:
    """Versión mejorada de create_kml_general con función de descripción personalizable"""
    kml = ET.Element("kml")
    kml.set("xmlns", "http://earth.google.com/kml/2.2")
    kml.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    document = ET.SubElement(kml, "Document")
    name = ET.SubElement(document, "name")
    name.text = nombre_doc

    description = ET.SubElement(document, "description")
    description.text = desc_doc

    schema = ET.SubElement(document, "Schema")
    schema.set("name", nombre_schema)
    schema.set("id", nombre_schema)

    for campo, tipo in campos.items():
        simple_field = ET.SubElement(schema, "SimpleField")
        simple_field.set("name", campo.lower())
        simple_field.set("type", tipo)

    # Estilos
    for estilo in config_simbologia:
        style = ET.SubElement(document, "Style")
        style.set("id", estilo["id"])
        
        # Label Style
        label_style = ET.SubElement(style, "LabelStyle")
        scale = ET.SubElement(label_style, "scale")
        scale.text = estilo.get("label_scale", "0.0")
        
        # Icon Style
        icon_style = ET.SubElement(style, "IconStyle")
        scale = ET.SubElement(icon_style, "scale")
        scale.text = estilo.get("icon_scale", "1.0")
        icon = ET.SubElement(icon_style, "Icon")
        href = ET.SubElement(icon, "href")
        href.text = estilo["icon_path"]

    for objeto in datos:
        if getattr(objeto, "latitud", 0.0) != 0.0 and getattr(objeto, "longitud", 0.0) != 0.0:
            placemark = ET.SubElement(document, "Placemark")
            name = ET.SubElement(placemark, "name")
            
            # Usar el primer campo como nombre por defecto
            primer_campo = list(campos.keys())[0]
            name.text = str(getattr(objeto, primer_campo, ""))

            description = ET.SubElement(placemark, "description")
            if funcion_descripcion:
                description.text = funcion_descripcion(objeto)
            else:
                # Descripción por defecto
                text_description = " - ".join(
                    str(getattr(objeto, c, "")) 
                    for c in campos 
                    if c not in ["latitud", "longitud"] and getattr(objeto, c, "")
                )
                description.text = text_description

            extended_data = ET.SubElement(placemark, "ExtendedData")
            schema_data = ET.SubElement(extended_data, "SchemaData")
            schema_data.set("schemaUrl", f"#{nombre_schema}")

            for campo in campos.keys():
                simple_data = ET.SubElement(schema_data, "SimpleData")
                simple_data.set("name", campo.lower())
                simple_data.text = str(getattr(objeto, campo, ""))

            style_url = ET.SubElement(placemark, "styleUrl")
            style_url.text = "#" + funcion_asignacion_estilo(objeto, config_simbologia)

            point = ET.SubElement(placemark, "Point")
            coordinates = ET.SubElement(point, "coordinates")
            coordinates.text = f"{getattr(objeto, 'longitud')},{getattr(objeto, 'latitud')}"

    rough_string = ET.tostring(kml, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')