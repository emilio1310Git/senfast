from typing import List
from senfast.api.app.db.database import get_db_cursor
from senfast.api.app.db.models.models_taigua import DataSensorPressio, DataGateway, DataComptador

def obtener_sensors_pressio() -> List[DataSensorPressio]:
    query = """
    SELECT serial_number, proveidor, id_ubicacio, ubicacio, latitud, longitud, node,
        temps_nivell, bateria_nivell, temps_pressio, pressio, color,
        data_ini_ubicacio, tipus
      FROM SC.AIGUA_PRESSIO_COLOR2
     WHERE latitud IS NOT NULL AND longitud IS NOT NULL
    """
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
    SELECT id_gateway, nom, latitud, longitud, data_ultim_event, connectat
      FROM SC.GATEWAYS
    """
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
    with get_db_cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        return [
            DataComptador(**dict(zip(columns, row)))
            for row in rows
        ]


# MOCK REPOSITORY FOR TAIGUA DATA
# from typing import List
# from senfast.api.app.db.models.models_taigua import DataSensorPressio, DataGateway, DataComptador

# def obtener_sensors_pressio() -> List[DataSensorPressio]:
#     # Aquí deberías integrar tu consulta real a Oracle
#     # Ejemplo mock (borra y conecta a tu base real):
#     return [
#         DataSensorPressio(
#             serial_number="1001", proveidor="SUEZ", id_ubicacio="UB1", ubicacio="Carrer A",
#             latitud=41.2, longitud=2.1, color="VERD", bateria_nivell=80, pressio=2.1, tipus="sensor"
#         ),
#         DataSensorPressio(
#             serial_number="1002", proveidor="SUEZ", id_ubicacio="UB2", ubicacio="Carrer B",
#             latitud=41.3, longitud=2.2, color="VERMELL", bateria_nivell=15, pressio=1.2, tipus="sensor"
#         ),
#     ]

# def obtener_gateways() -> List[DataGateway]:
#     return [
#         DataGateway(
#             id_gateway="G1", nom="Gateway 1", latitud=41.0, longitud=2.0,
#             data_ultim_event="2025-05-25 14:00:00", connectat="S"
#         ),
#         DataGateway(
#             id_gateway="G2", nom="Gateway 2", latitud=41.1, longitud=2.1,
#             data_ultim_event="2025-05-24 09:15:00", connectat="N"
#         ),
#     ]

# def obtener_comptadors() -> List[DataComptador]:
#     return [
#         DataComptador(
#             serial_number="C100", comptador="CompA", contracte="CT1", adreca="Av. Catalunya 1",
#             ultima_lectura=1234.5, ultim_consum=34.2, data_ultima_lectura="2025-05-22",
#             total_lectures=24, numero_lectures="24,22,20,18,16,14,12", classificacio=2, latitud=41.4, longitud=2.4
#         ),
#         DataComptador(
#             serial_number="C101", comptador="CompB", contracte="CT2", adreca="Av. Catalunya 2",
#             ultima_lectura=2345.6, ultim_consum=44.1, data_ultima_lectura="2025-05-23",
#             total_lectures=2, numero_lectures="2,1,1,0,0,0,0", classificacio=1, latitud=41.5, longitud=2.5
#         ),
#     ]