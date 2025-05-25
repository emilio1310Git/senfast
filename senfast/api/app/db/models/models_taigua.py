from pydantic import BaseModel
from typing import Optional

class DataSensorPressio(BaseModel):
    serial_number: str
    proveidor: str
    id_ubicacio: str
    ubicacio: str
    latitud: float
    longitud: float
    node: Optional[str] = None
    temps_nivell: Optional[str] = None
    bateria_nivell: Optional[float] = None
    temps_pressio: Optional[str] = None
    pressio: Optional[float] = None
    color: Optional[str] = None
    data_ini_ubicacio: Optional[str] = None
    tipus: Optional[str] = None

class DataGateway(BaseModel):
    id_gateway: str
    nom: str
    latitud: float
    longitud: float
    data_ultim_event: str
    connectat: str

class DataComptador(BaseModel):
    serial_number: str
    comptador: str
    contracte: str
    adreca: str
    ultima_lectura: float
    ultim_consum: float
    data_ultima_lectura: str
    total_lectures: int
    numero_lectures: str
    classificacio: int
    latitud: float
    longitud: float