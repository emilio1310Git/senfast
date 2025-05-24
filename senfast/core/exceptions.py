

from fastapi import HTTPException, status 

class DatabaseConnectionError(HTTPException): 
    def __init__(self, detail="Error al conectar a la base de datos"): 
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail) 

class DatabaseQueryError(HTTPException): 
    def __init__(self, detail="Error al ejecutar la consulta"): 
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail) 

class TableNotFoundError(HTTPException): 
    def __init__(self, table_name: str): 
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tabla '{table_name}' no encontrada") 

class GeometryColumnNotFoundError(HTTPException): 
    def __init__(self, table_name: str): 
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"La tabla '{table_name}' no tiene una columna de geometría")