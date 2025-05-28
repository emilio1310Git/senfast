
import os
from typing import Any, Optional
from pydantic import Field, field_validator

from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import (
#     ValidationInfo,
#     FieldValidationInfo,
# )
from functools import lru_cache

class Settings(BaseSettings):
    """Configuración principal de la aplicación con variables de entorno."""

    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file_encoding="utf-8",
        env_file=".env", 
        extra="allow",
        # extra="forbid",
        validate_default=True,
        arbitrary_types_allowed=True
    )
    # Configuración básica    
    APP_NAME: str = Field("senfast", json_schema_extra={"env":'APP_NAME'})
    API_PREFIX: str = Field("/api", json_schema_extra={"env": "API_PREFIX"}) 
    APP_VERSION: str = Field(default="0.1.0", json_schema_extra={"env": "APP_VERSION"})
    APP_DESCRIPTION: str = Field(..., json_schema_extra={"env": "APP_DESCRIPTION"})
    ENVIRONMENT: str = Field(default="development", json_schema_extra={"env": "ENVIRONMENT"})
    DEBUG: bool = Field(default=False, json_schema_extra={"env": "DEBUG"}) 
    LOG_LEVEL: str = Field(default="info", json_schema_extra={"env": "LOG_LEVEL"})

    # Configuración API
    API_HOST: str = Field(default="localhost", json_schema_extra={"env": "API_HOST"})
    API_PORT: Optional[str] = Field("8000", json_schema_extra={"env": "API_PORT"}) 
    EXTRA_CORS_ORIGINS: list[str] = Field(default=["*"], json_schema_extra={"env": "EXTRA_CORS_ORIGINS"})

    @property
    def cookie_name(self) -> str:
        """Get the cookie name for the domain."""
        import re
        return re.sub(r'[^a-zA-Z0-9_]', '_', self.API_HOST)

    # Configuración Base de Datos

    DB_HOST: str = Field(default="localhost", json_schema_extra={"env": "DB_HOST"})
    DB_PORT: int = Field(default=1521, json_schema_extra={"env": "DB_PORT"})  # Puerto por defecto de Oracle
    DB_NAME: str = Field(default="ORCLPDB1", json_schema_extra={"env": "DB_NAME"})  # SID o Service Name
    DB_USER: str = Field(default="usuario", json_schema_extra={"env": "DB_USER"})
    DB_PASSWORD: str = Field(default="", json_schema_extra={"env": 'DB_PASSWORD'})

    
    POOL_MIN_CONN: int = Field(default=3, ge=1, json_schema_extra={"env": "POOL_MIN_CONN"}) 
    POOL_MAX_CONN: int = Field(default=15, ge=5, json_schema_extra={"env": "POOL_MAX_CONN"}) 
    DB_CONNECT_TIMEOUT: int = Field(default=5, json_schema_extra={"env": "DB_CONNECT_TIMEOUT"}) 
    DB_STATEMENT_TIMEOUT: int =Field(default=30, json_schema_extra={"env": "DB_STATEMENT_TIMEOUT"}) 
    CURSOR_FACTORY: str = Field(default="RealDictCursor", json_schema_extra={"env": "CURSOR_FACTORY"}) 

    # Tablas permitidas para consultas dinámicas
    ALLOWED_TABLES: dict[str, list[str]] = Field(
    	default={"CODI": ["BARRIS", "otra_tabla"]}
	)

    @field_validator("DB_URL", mode="before", check_fields=False)
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> Any:
        """Construye la cadena de conexión a Oracle desde variables de entorno."""
        if isinstance(v, str):
            return v
        # cadena de conexión Oracle: oracle+cx_oracle://usuario:contraseña@host:puerto/?service_name=servicio
        user = values.get("DB_USER")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = str(values.get("DB_PORT", 1521))
        service = values.get("DB_NAME", "")
        return f"oracle+cx_oracle://{user}:{password}@{host}:{port}/?service_name={service}"
    # OTROS VELORES PROPIOS DE LOS ENDPOINTS
    PATH_ICONES_SOBREEIXIDORS: str = Field(default="RealDictCursor", json_schema_extra={"env": "PATH_ICONES_SOBREEIXIDORS"})

@lru_cache
def get_settings() -> Settings:
    """Factory function para evitar instanciación temprana"""
    return Settings()