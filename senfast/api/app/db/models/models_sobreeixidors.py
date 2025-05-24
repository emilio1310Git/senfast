# Modelos
from pydantic import BaseModel
from typing import Literal


class DataCoordinates(BaseModel):
    latitude: float
    longitude: float

class DataSobreeixidor(BaseModel):
    component: str
    descripcio: str
    latitud: float
    longitud: float
    clase: str
    dayly_threshold: int
    data_darrera_lectura: str
    lectura: float
