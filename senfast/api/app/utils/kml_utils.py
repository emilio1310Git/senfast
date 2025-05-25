# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Callable
import os

def create_kml_general(
    datos: List,
    campos: Dict[str, str],
    config_simbologia: List[Dict],
    nombre_schema: str,
    nombre_doc: str,
    desc_doc: str,
    funcion_asignacion_estilo: Callable,
) -> str:
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
        href.text = estilo["icon_path"]  # Debe ser un path absoluto o relativo accesible

    for objeto in datos:
        if getattr(objeto, "latitud", 0.0) != 0.0 and getattr(objeto, "longitud", 0.0) != 0.0:
            placemark = ET.SubElement(document, "Placemark")
            name = ET.SubElement(placemark, "name")
            name.text = getattr(objeto, campos.get("component", list(campos.keys())[0]), "")

            description = ET.SubElement(placemark, "description")
            text_description = " - ".join(str(getattr(objeto, c, "")) for c in campos if c != "latitud" and c != "longitud")
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