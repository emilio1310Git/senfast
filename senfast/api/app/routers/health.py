from fastapi import APIRouter, Request
from senfast.api.app.db import database
from senfast.api.app.db.database import get_db_cursor, get_connection_pool
from senfast.core.exceptions import DatabaseQueryError
from senfast.core.monitoring import logger
from senfast.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/",
    summary="Verificar estado del servicio",
    description="""
    Comprueba la conectividad con la base de datos y el estado del pool de conexiones.
    Útil para monitoreo y comprobaciones de salud del servicio.

    Ejemplo de uso:

    * Realizar un health check: `/health`
    """
    )
def healthcheck():
    pool = database.get_connection_pool()
    try:
        with database.get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM DUAL")
                status = cursor.fetchone()
        estado_db = "ok" if status and status[0] == 1 else "error"
        pool_status = {
            "open": True,
            "busy": getattr(pool, 'busy', None),
            "size": getattr(pool, 'size', None),
        }
        return {
            "database": estado_db,
            "pool": pool_status,
            "version": database.settings.APP_NAME,
        }
    except Exception as e:
        return {"database": "error", "error": str(e)}

# @router.get(
#     "/health",
#     summary="Verificar estado del servicio",
#     description="""
#     Comprueba la conectividad con la base de datos y el estado del pool de conexiones.
#     Útil para monitoreo y comprobaciones de salud del servicio.

#     Ejemplo de uso:

#     * Realizar un health check: `/health`
#     """
# )
# async def health_check(request: Request):
#     """Endpoint mejorado para verificar el estado del servicio."""
#     logger.info(f"Request ID: {request.state.request_id} - Health check")
#     try:
#         pool = get_connection_pool()
#         with get_db_cursor() as cursor:
#             # Verificación básica de la base de datos
#             cursor.execute("SELECT 1")
            
#             # Estadísticas detalladas del pool
#             try:
#                 # Intentamos acceder a los atributos del pool
#                 available = pool.maxconn - len(pool._used) if hasattr(pool, '_used') else "N/A"
#                 waiting = pool._waiting if hasattr(pool, '_waiting') else 0
#             except Exception:
#                 # Si hay error, usamos valores por defecto
#                 available = "N/A"
#                 waiting = 0
                
#             pool_stats = {
#                 "min_connections": settings.POOL_MIN_CONN,
#                 "max_connections": settings.POOL_MAX_CONN,
#                 "available": available,
#                 "waiting": waiting,
#                 "timeout": settings.DB_CONNECT_TIMEOUT
#             }
            
#             return {
#                 "status": "healthy",
#                 "database": "connected",
#                 "pool_stats": pool_stats,
#                 "version": settings.APP_NAME,
#                 "environment": settings.ENVIRONMENT
#             }
#     except DatabaseQueryError as e: 
#         logger.error(f"Request ID: {request.state.request_id} - Error en el health check: {str(e)}") 
#         raise DatabaseQueryError(detail=str(e))
#     except oracledb.OperationalError as e:
#         logger.error(f"Request ID: {request.state.request_id} - Error de base de datos: {str(e)}", exc_info=True)
#         raise DatabaseQueryError(detail=str(e))  
#     except Exception as e:
#         logger.error(f"Request ID: {request.state.request_id} - Health check failed: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail="Service unavailable"
#         )
