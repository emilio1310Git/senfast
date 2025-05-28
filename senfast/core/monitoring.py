
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from senfast.core.config import get_settings

from fastapi import Request 
import uuid 

global_settings = get_settings()
# Configuración de logging

class RequestIDFilter(logging.Filter):
    """
    Filtro para inyectar un ID de request único en cada registro de log.
    """     
    def filter(self, record):
        record.request_id = getattr(record, 'request_id', 'NO_REQUEST_ID')
        return True

# Middleware para añadir un identificador único a cada request 
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    return response

def setup_logging():
    """Configura el logging para la aplicación."""    
    if hasattr(setup_logging, 'executed'):
        return logging.getLogger(global_settings.APP_NAME)
    setup_logging.executed = True    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(base_dir, "logs", global_settings.APP_NAME)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = os.path.join(log_dir, f"{global_settings.APP_NAME}_{datetime.now().strftime('%Y%m%d')}.log")
    
    logger = logging.getLogger(global_settings.APP_NAME)
    logger.addFilter(RequestIDFilter())

    # Limpiar handlers existentes para evitar duplicados
    if logger.hasHandlers():
        logger.handlers.clear()    
    
    # Nivel de logging basado en entorno
    # logger.setLevel(getattr(global_settings, "LOG_LEVEL", "INFO"))
    level = getattr(global_settings, "LOG_LEVEL", "INFO").upper()
    logger.setLevel(level)
    # Formato estructurado para mejor análisis
    formatter = logging.Formatter(
        '%(asctime)s|%(levelname)s|%(name)s|%(module)s|%(funcName)s|%(message)s'
    )    
    
    # Handler para archivo (rotativo)
    file_handler = RotatingFileHandler(
        log_filename, maxBytes=1024*1024*5, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para consola SIEMPRE (puedes quitarlo luego si quieres solo archivo)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
logger.info("Logger inicializado correctamente")