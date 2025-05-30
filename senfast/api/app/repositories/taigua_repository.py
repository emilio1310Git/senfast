from typing import List
from senfast.api.app.db.database import get_db_cursor
from senfast.api.app.models.models_taigua import DataSensorPressio, DataGateway, DataComptador

def obtener_sensors_pressio() -> List[DataSensorPressio]:
    query = """
    SELECT serial_number, provider, id_ubicacio, latitud, longitud,
        temps_nivell, bateria_nivell, temps_pressio, pressio, color,
        concat(to_char(data_ini_a_ubicacio,'DD/MM/YYYY, HH24:MI'),'h') AS data_ini_ubicacio,
        adreça
      FROM SC.AIGUA_PRESSIO_COLOR2
     WHERE latitud IS NOT NULL AND longitud IS NOT NULL
    """
#     SELECT SERIAL_NUMBER, PROVIDER, LATITUD, LONGITUD, TEMPS_NIVELL, BATERIA_NIVELL, TEMPS_PRESSIO, PRESSIO, COLOR, DATA_INI_A_UBICACIO, ID_UBICACIO, ADREÇA
# FROM SC.AIGUA_PRESSIO_COLOR2;
    with get_db_cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        return [
            DataSensorPressio(**dict(zip(columns, row)))
            for row in rows
        ]

def obtener_gateways() -> List[DataGateway]:
    query = """
    SELECT id_gateway, nom, latitud, longitud,
      concat(to_char(temps_event,'DD/MM/YYYY, HH24:MI'),'h') AS data_ultim_event, connectat
      FROM SC.GATEWAYS
    """
# SELECT ID_GATEWAY, NOM, LATITUD, LONGITUD, TEMPS_EVENT, CONNECTAT
# FROM SC.GATEWAYS;    
    with get_db_cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        return [
            DataGateway(**dict(zip(columns, row)))
            for row in rows
        ]

def obtener_comptadors() -> List[DataComptador]:
    query = """
    SELECT serial_number, comptador, contracte, adreca, ultima_lectura, ultim_consum,
           data_ultima_lectura, total_lectures, numero_lectures, classificacio, latitud, longitud
      FROM SC.DADES_COMPTADORS_ITRON
     WHERE latitud IS NOT NULL AND longitud IS NOT NULL
    """
# SELECT SERIAL_NUMBER, "Latitud", "Longitud", "Adreça", "Contracte", "Comptador", "Gran Consum", "Darrera Lectura", "Lectura", "Darrer Consum", "Consum", "Ahir", "Fa 2 dies", "Fa 3 dies", "Fa 4 dies", "Fa 5 dies", "Fa 6 dies", "Fa 7 dies"
# FROM SC.DADES_COMPTADORS_ITRON;    
    with get_db_cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        return [
            DataComptador(**dict(zip(columns, row)))
            for row in rows
        ]

