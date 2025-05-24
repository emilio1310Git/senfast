# senfast

### 1. Estructura del Proyecto

```
📂 senfast/
├── 📂 config/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements_dev.txt
│   └── requirements.txt
├── 📂 senfast/
│   ├── 📂 core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logger.py
│   │   ├── metrics.py
│   │   └── monitoring.py
│   ├── 📂 api/
│   │   ├── 📂 app/
│   │   │   ├── 📂 db/
│   │   │   │   ├── 📂 models/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── models.py
│   │   │   │   │   └── models_sobreeixidors.py
│   │   │   │   ├── 📂 querys/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── read_query.py
│   │   │   │   │   └── read_query_sobreeixidors.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── database.py
│   │   │   ├── 📂 routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── health.py         # Endpoints de healthcheck (pool/db/system)
│   │   │   │   ├── metrics_route.py        # Endpoints de Prometheus/metrics
│   │   │   │   ├── docs.py           # Endpoints relacionados con documentación
│   │   │   │   ├── info.py           # Endpoints que retornan información del sistema/app
│   │   │   │   ├── data_barris.py    # Endpoints de acceso a datos/tablas
│   │   │   │   ├── data_sobreeixidors.py
│   │   │   │   └── data....py (otros por dominio)
│   │   │   ├── __init__.py
│   │   │   └── main.py
│   │   ├── 📂 static/
│   │   │   ├── __init__.py
│   │   │   └── favicon.ico
│   │   └── __init__.py
│   ├── 📂 logs/
│   ├── 📂 tests/
│   │   ├── conftest.py
│   │   ├── test_database.py
│   │   ├── test_health.py
│   │   ├── test_metrics.py
│   │   └── ...
│   └── __init__.py
├── .env
├── .gitignore
├── LICENSE.md
├── README.md
└── setup.py
```

