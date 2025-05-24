# senfast API

API para servir datos de sensores alfanuméricos con coordenadas geográficas desde Oracle, exponerlos vía REST y generando un fichero KML.

## Descripción

Esta API proporciona endpoints para acceder y consultar datos almacenados en una base de datos Oracle para datos alfanuméricos.
Incluye soporte para:

* Consultas de datos tabulares (Oracle).
* Paginación para manejar grandes conjuntos de datos.
* Generación de ficheros KML para visualización geográfica.
* Logging detallado.
* Health check para monitoreo.
* Métricas Prometheus.

## Requisitos

* Python 3.8+
* Oracle Database (y acceso a usuario con privilegios)
* [oracledb](https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html)

## Instalación

1.  Clonar el repositorio:
    ```bash
    git clone <repositorio>
    cd <directorio_del_proyecto>
    ```
2.  Crear un entorno virtual (recomendado):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```
3.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configurar las variables de entorno (ver `.env.example`).
5.  Ejecutar la API:
    ```bash
    uvicorn api.app.main:app --reload
    ```

## Documentación de la API

La documentación interactiva está disponible en:

* Swagger UI: `/docs`
* ReDoc: `/redoc`

## Tests

Ejecutar los tests:

```bash
pytest
```

## TO-DO

- [ ] Configurar los test completamente
- [ ] Refactorizaciones
    - [ ] Modificar la gestión de querys a repositories
