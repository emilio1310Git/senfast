from fastapi import APIRouter,Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from senfast.core.logger import logger
from senfast.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="", tags=["Documentation"])
# 

# router = APIRouter(tags=["Documentation"])

@router.get("/changelog", summary="Changelog del proyecto")
def changelog():
    # leer un changelog.md o devolver un string
    return {"changelog": "Aquí va el changelog..."}

@router.get("/about", summary="Sobre la aplicación")
def about():
    return {"about": "API para servir datos alfanuméricos desde Oracle."}

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    if logger:
        request_id = getattr(request.state, "request_id", None)
        logger.info(f"Request ID: {request_id} - Acceso a documentación Swagger")
    
    # Obtener base URL de la solicitud actual
    # base_url = str(request.base_url).rstrip('/')
    # Asegurar que estamos en la ruta correcta
    openapi_path = f"/senfast/{settings.API_PREFIX}/openapi.json".replace("//", "/")
    
    return get_swagger_ui_html(
        openapi_url=openapi_path,
        title=f"{settings.APP_NAME} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@router.get("/redoc", include_in_schema=False)
async def redoc_html(request: Request):
    if logger:
        request_id = getattr(request.state, "request_id", None)
        logger.info(f"Request ID: {request_id} - Acceso a documentación ReDoc")
    
    # Obtener base URL de la solicitud actual
    # base_url = str(request.base_url).rstrip('/')
    # Asegurar que estamos en la ruta correcta
    openapi_path = f"/senfast/{settings.API_PREFIX}/openapi.json".replace("//", "/")
    
    return get_redoc_html(
        openapi_url=openapi_path,
        title=f"{settings.APP_NAME} - API ReDoc",
    )

# @router.get("/openapi.json", include_in_schema=False)
# async def get_open_api_endpoint(request: Request):
#     app = request.app
#     if logger:
#         request_id = getattr(request.state, "request_id", None)
#         logger.info(f"Request ID: {request_id} - Solicitud de OpenAPI JSON")
#     return get_openapi(
#         title=settings.APP_NAME,
#         version=settings.APP_VERSION,
#         description=settings.APP_DESCRIPTION,
#         routes=app.routes,
#     )
@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(request: Request):
    app = request.app
    if hasattr(app, 'logger') and app.logger:
        app.logger.info(f"Request ID: {request.state.request_id} - Solicitud de OpenAPI JSON")
    return app.openapi()