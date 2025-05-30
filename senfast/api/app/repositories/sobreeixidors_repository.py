from senfast.api.app.db.database import get_db_cursor
from senfast.core.monitoring import logger
from fastapi import HTTPException, status
from senfast.api.app.models.models_sobreeixidors import DataSobreeixidor

def obtener_sobreeixidors(page: int, per_page: int) -> list:
    offset = (page - 1) * per_page
    query = """
        SELECT "component", "descripcio", "latitud", "longitud", "color" AS "clase",
               concat(to_char("darrera_lectura",'DD/MM/YYYY, HH24:MI'),'h') AS "data_darrera_lectura",
               "dayly_threshold", "lectura"
        FROM SC.SOFREL_GEO_COMPONENTS
        WHERE "latitud" IS NOT NULL
        ORDER BY "component"
        OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
    """    
    with get_db_cursor() as cursor:
        cursor.execute(query, {"offset": offset, "per_page": per_page})
        columns = [col[0].lower() for col in cursor.description]
        records = cursor.fetchall()
        logger.debug(f"Ejecutando consulta: {query}")
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron sobreeixidors")
        return [DataSobreeixidor(**dict(zip(columns, row))) for row in records]
    
# class SobreeixidorsRepository:
#     @staticmethod
#     def get_all(page: int, per_page: int) -> list:
#         offset = (page - 1) * per_page
#         # query = """
#         # SELECT "component", "descripcio", "latitud", "longitud", "color" AS "clase",
#         #        concat(to_char("darrera_lectura",'DD/MM/YYYY, HH24:MI'),'h') AS "data_darrera_lectura",
#         #        "dayly_threshold", "lectura"
#         # FROM SC.SOFREL_GEO_COMPONENTS
#         # WHERE "latitud" IS NOT NULL
#         # ORDER BY "component"
#         # """  
#         query = """
#         SELECT component, descripcio, latitud, longitud, clase, dayly_threshold, data_darrera_lectura, lectura
#         FROM SC.SOFREL_GEO_COMPONENTS
#         WHERE latitud IS NOT NULL AND longitud IS NOT NULL
#         OFFSET :offset ROWS FETCH NEXT :per_page ROWS ONLY
#         """        
#         with get_db_cursor() as cursor:
#             # logger.debug(f"Ejecutando consulta: SELECT COUNT(*) FROM SC.SOFREL_GEO_COMPONENTS")
#             # cursor.execute("SELECT COUNT(*) FROM SC.SOFREL_GEO_COMPONENTS")
#             # print(cursor.fetchall())
#             logger.debug(f"Ejecutando consulta: {query}")
#             cursor.execute(query, {"offset": offset, "per_page": per_page})
#             columns = [col[0].lower() for col in cursor.description]
#             records = cursor.fetchall()
#             if not records:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron sobreeixidors")
#             # return {"data": records, "count": len(records)}
            
#             return [DataSobreeixidor(**dict(zip(columns, row))) for row in records]