# Endpoints
from fastapi import APIRouter, HTTPException, status, Request , Query, Depends, Path
from typing import Optional, List 
from pydantic import BaseModel, ValidationError, field_validator 
import oracledb
# from oracledb import pool

from senfast.core.config import get_settings
from senfast.api.app.db.querys.read_query import read_query
from senfast.core.monitoring import logger
from senfast.api.app.db.models import BarriRead
from senfast.api.app.db.database import get_db_cursor, validate_table_name, get_connection_pool
from senfast.core.exceptions import TableNotFoundError, GeometryColumnNotFoundError, DatabaseQueryError
# from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
# from prometheus_client import Counter, Gauge
# from starlette.responses import Response

settings = get_settings()
router = APIRouter(prefix="", tags=["Dades Barris"])

class TableName(BaseModel): 
    table_name: str 
    @field_validator("table_name") 
    def validate_table(cls, v: str): 
        if not validate_table_name(v): 
            raise ValueError("Nombre de tabla inválido") 
        return v 

@router.get(
    "/all_barris",
    response_model=list[BarriRead],
    summary="Obtener todos los barrios",
    description="""
    Devuelve una lista completa de todos los barrios disponibles.

    Ejemplo de uso:

    * Obtener todos los barrios: `/all_barris`
    """
)
async def read_barris(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=1000)
    ):
    """Endpoint optimizado para obtener todos los barrios."""
    logger.critical("RUTA /all_barris INICIADA")  # Log CRITICAL
    try:
        logger.info(f"Request ID: {request.state.request_id} - Solicitud recibida para obtener todos los barris")
        offset = (page - 1) * per_page
        with get_db_cursor() as cursor:
            logger.debug(f"Ejecutando consulta: {read_query.READ_ALL_BARRIS}")
            cursor.execute(read_query.READ_ALL_BARRIS)
            columns = [col[0] for col in cursor.description]
            records = cursor.fetchall()
            # logger.debug(f"Resultados de la consulta: {records}")
            # logger.critical(f"RUTA /all_barris FINALIZADA con éxito: {records}")  # Log CRITICAL
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron barrios")
            return [BarriRead(**dict(zip(columns, row))) for row in records]
    except DatabaseQueryError as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error al obtener todos los barrios: {str(e)}")
        raise DatabaseQueryError(detail=str(e))
    except oracledb.OperationalError as e:
        logger.error(f"Request ID: {request.state.request_id} - Error de base de datos: {str(e)}", exc_info=True)
        raise DatabaseQueryError(detail=str(e))      
    except Exception as e:
        logger.error(f"Request ID: {request.state.request_id} - Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/barri/{id}",
    summary="Obtener un barrio por ID",
    description="""
    Obtiene un barrio específico por su ID.

    Parámetros:

    * `id` (int): El ID del barrio a obtener.

    Ejemplo de uso:

    * Obtener el barrio con ID 1: `/barri/1`
    """
)
def read_barri_by_id(id: int = Path(..., description="ID del barrio"), 
    request: Request = None):
    """Endpoint para obtener un barri por ID."""
    logger.info(f"Request ID: {request.state.request_id} - Solicitud recibida para obtener barri con ID: {id}")
    logger.debug(f"Request ID: {request.state.request_id} - Ejecutando consulta para obtener barri con ID: {id}")
    try:
        with get_db_cursor() as cursor:
            logger.debug(f"Request ID: {request.state.request_id} - Ejecutando consulta: {read_query.READ_BARRI_BY_ID}")
            cursor.execute(read_query.READ_BARRI_BY_ID, (id,))

            record = cursor.fetchone()            
            # record = cursor.execute(read_query.READ_BARRI_BY_ID, (id,)).fetchone()
            if record is None:
                raise HTTPException(status_code=404, detail=f"{id} Barri inexistente.")
            return record
    except DatabaseQueryError as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error al obtener barri por ID {id}: {str(e)}")
        raise DatabaseQueryError(detail=str(e))
    except oracledb.OperationalError as e:
        logger.error(f"Request ID: {request.state.request_id} - Error de base de datos: {str(e)}", exc_info=True)
        raise DatabaseQueryError(detail=str(e))      
    except Exception as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error inesperado: {str(e)}", exc_info=True) 
        raise HTTPException( 
            status_code=500, 
            detail="Error interno del servidor" 
        ) 

@router.get("/nom/{nom_barri}",
    summary="Obtener barrios por nombre (búsqueda parcial)",
    description="""
    Obtiene una lista de barrios cuyo nombre coincide parcialmente con la cadena proporcionada.
    Utiliza una búsqueda tipo LIKE.

    Parámetros:

    * `nom_barri` (str): La cadena a buscar en los nombres de los barrios.

    Ejemplo de uso:

    * Buscar barrios que contengan "Centro": `/nom/Centro`
    """
)
def read_barri_by_nom(nom_barri: str, request: Request):
    """Endpoint para obtener un barri por nombre mediante like."""
    logger.info(f"Request ID: {request.state.request_id} - Solicitud recibida para obtener barri con nombre: {nom_barri}")
    logger.debug(f"Request ID: {request.state.request_id} - Ejecutando consulta para obtener barri con nombre: {nom_barri}")
    try:
        pool = get_connection_pool()
        with get_db_cursor() as cursor:
            logger.debug(f"Request ID: {request.state.request_id} - Ejecutando consulta: {read_query.READ_BARRI_BY_NOM}")
            cursor.execute(read_query.READ_BARRI_BY_NOM, (f"%{nom_barri}%",))
            columns = [col[0] for col in cursor.description]
            records = cursor.fetchall()
            if records is None:
                raise HTTPException(status_code=404, detail="No se ha encontrado ninguan semejanza en nombres de Barrios.")
            return [BarriRead(**dict(zip(columns, row))) for row in records]
    except DatabaseQueryError as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error al obtener barri por nombre {nom_barri}: {str(e)}") 
        raise DatabaseQueryError(detail=str(e))
    except oracledb.OperationalError as e:
        logger.error(f"Request ID: {request.state.request_id} - Error de base de datos: {str(e)}", exc_info=True)
        raise DatabaseQueryError(detail=str(e))  
    except Exception as e: 
        logger.error(f"Request ID: {request.state.request_id} - Error inesperado: {str(e)}", exc_info=True) 
        raise HTTPException( 
            status_code=500, 
            detail="Error interno del servidor" 
        ) 






