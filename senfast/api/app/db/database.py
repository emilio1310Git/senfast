import os
import re
import time
from contextlib import contextmanager
from typing import Iterator, Optional
import oracledb
from fastapi import HTTPException, status

from senfast.core.monitoring import logger
from senfast.core.config import get_settings
from senfast.core.exceptions import DatabaseConnectionError, DatabaseQueryError 
from senfast.core.metrics import update_db_pool_metrics, measure_db_query, DB_POOL_CONNECTIONS

# Obtenemos settings cuando realmente se necesitan
settings = get_settings()


# (pool global):
POOL = None
# Inicializa el modo thick si no está ya inicializado
if oracledb.is_thin_mode():
    lib_dir = os.getenv("ORACLE_CLIENT_LIB")
    if not lib_dir:
        if settings.ENVIRONMENT == "production":
            lib_dir = "/opt/oracle/instantclient"
        else:
            lib_dir = r"C:\oracle\instantclient"
    oracledb.init_oracle_client(lib_dir=lib_dir)

def get_connection_pool():
    global POOL
    if POOL is None:
        POOL = create_connection_pool()
    return POOL

# Pool de conexiones con manejo de reintentos
def create_connection_pool(retries: int = 3, delay: float = 1.0) -> oracledb.ConnectionPool:
    """Crea un pool de conexiones con reintentos automáticos."""
    last_error = None
    for attempt in range(retries):
        try:
            dsn = f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            new_pool = oracledb.create_pool(
                min=settings.POOL_MIN_CONN,
                max=settings.POOL_MAX_CONN,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                dsn=dsn,
                # application_name=settings.APP_NAME,
                # connect_timeout=settings.DB_CONNECT_TIMEOUT,
                increment = 1,
            )
            logger.info("Pool de conexiones creado exitosamente")
            # Inicializar métricas del pool
            DB_POOL_CONNECTIONS.labels(state='active').set(0)
            DB_POOL_CONNECTIONS.labels(state='idle').set(settings.POOL_MIN_CONN)
            DB_POOL_CONNECTIONS.labels(state='total').set(settings.POOL_MIN_CONN)            
            return new_pool
        except oracledb.OperationalError as e:
            last_error = e
            logger.error(f"Error al intentar conectar (intento {attempt+1}/{retries}): {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
    logger.error("No se pudo establecer el pool de conexiones después de varios intentos")
    raise DatabaseConnectionError(f"Failed to create connection pool: {str(last_error)}")

@contextmanager
def get_db_connection() -> Iterator[oracledb.Connection]:
    """Context manager para obtener conexiones del pool con manejo robusto de errores."""
    conn = None
    pool = get_connection_pool()
    
    try:
        conn = pool.acquire() 
        conn.autocommit = False
        # Actualizar métricas del pool después de obtener conexión
        update_db_pool_metrics(pool)        
        yield conn
    except oracledb.OperationalError as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {str(e)}", exc_info=True)
        raise DatabaseQueryError(detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado en get_db_connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}" 
        )
    finally:
        if conn:
            try:
                conn.close()  
                # Actualizar métricas del pool después de devolver conexión
                update_db_pool_metrics(pool)                
            except Exception as e:
                logger.error(f"Error al devolver conexión al pool: {str(e)}")

@contextmanager
def get_db_cursor() -> Iterator[oracledb.Cursor]:
    """Context manager para obtener cursores con manejo de transacciones."""
    with get_db_connection() as conn:
        cursor = None
        try:
            cursor = conn.cursor()
         
            # cursor.execute(f"SET statement_timeout TO {settings.DB_STATEMENT_TIMEOUT * 1000};")
            yield cursor
            conn.commit()
        except oracledb.OperationalError as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise DatabaseQueryError(detail=str(e))
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error inesperado en get_db_cursor: {str(e)}")
            raise             
        finally:
            if cursor:
                cursor.close()
# Los métodos específicos para consultas con métricas
@measure_db_query(query_type='select')
def execute_select(cursor, query, params=None):
    """Ejecuta una consulta SELECT con métricas"""
    cursor.execute(query, params)
    return cursor.fetchall()

@measure_db_query(query_type='insert')
def execute_insert(cursor, query, params=None):
    """Ejecuta una consulta INSERT con métricas"""
    cursor.execute(query, params)
    return cursor.rowcount

@measure_db_query(query_type='update')
def execute_update(cursor, query, params=None):
    """Ejecuta una consulta UPDATE con métricas"""
    cursor.execute(query, params)
    return cursor.rowcount

@measure_db_query(query_type='delete')
def execute_delete(cursor, query, params=None):
    """Ejecuta una consulta DELETE con métricas"""
    cursor.execute(query, params)
    return cursor.rowcount

# Los métodos de validación
def validate_table_name(table_name: str) -> bool:
    """Valida nombres de tabla contra inyección SQL y lista de tablas permitidas."""
    if not table_name:
        return False    
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', table_name):
        return False
    # Separar esquema y tabla si existe
    parts = table_name.split('.')
    if len(parts) == 1:
        return any(table_name in settings.ALLOWED_TABLES.get(schema, []) for schema in settings.ALLOWED_TABLES)
    elif len(parts) == 2:
        schema, table = parts
        return table in settings.ALLOWED_TABLES.get(schema, [])


