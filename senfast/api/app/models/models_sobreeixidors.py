# Modelos
from pydantic import BaseModel
from typing import Literal, Optional


class DataCoordinates(BaseModel):
    latitude: float
    longitude: float

class DataSobreeixidor(BaseModel):
    component: str
    descripcio: Optional[str]
    latitud: float
    longitud: float
    clase: str
    dayly_threshold: int
    data_darrera_lectura: Optional[str]
    lectura: float
