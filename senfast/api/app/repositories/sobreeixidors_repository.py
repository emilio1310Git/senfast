from senfast.api.app.db.database import get_db_cursor
from senfast.core.monitoring import logger
from senfast.api.app.db.querys.read_query_sobreeixidors import read_query_sobreeixidors
from fastapi import HTTPException, status
from senfast.api.app.db.models.models_sobreeixidors import DataSobreeixidor
class SobreeixidorsRepository:
    @staticmethod
    def get_all(page: int, per_page: int) -> list:
        offset = (page - 1) * per_page
        with get_db_cursor() as cursor:
            # logger.debug(f"Ejecutando consulta: SELECT COUNT(*) FROM SC.SOFREL_GEO_COMPONENTS")
            # cursor.execute("SELECT COUNT(*) FROM SC.SOFREL_GEO_COMPONENTS")
            # print(cursor.fetchall())               
            logger.debug(f"Ejecutando consulta: {read_query_sobreeixidors.READ_ALL_SOBREEIXIDORS}")
            cursor.execute(read_query_sobreeixidors.READ_ALL_SOBREEIXIDORS)
            columns = [col[0] for col in cursor.description]
            records = cursor.fetchall()
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron sobreeixidors")
            # return {"data": records, "count": len(records)}
            
            return [DataSobreeixidor(**dict(zip(columns, row))) for row in records]