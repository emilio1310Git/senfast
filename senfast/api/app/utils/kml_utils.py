from xml.etree import ElementTree as ET
from xml.dom import minidom
from typing import List

def create_kml_document(sobreeixidors: List) -> str:
    kml = ET.Element("kml")
    kml.set("xmlns", "http://earth.google.com/kml/2.2")
    kml.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    document = ET.SubElement(kml, "Document")
    name = ET.SubElement(document, "name")
    name.text = "Dades SENTILO Terrassa - Sobreeixidors -"

    description = ET.SubElement(document, "description")
    description.text = "KML amb la informació relativa als sobreexidors instal·lats a la ciutat"

    # ... (resto de la lógica, extraída del método original)...

    rough_string = ET.tostring(kml, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')