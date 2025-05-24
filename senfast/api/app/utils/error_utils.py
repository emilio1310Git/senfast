from fastapi import HTTPException, status

def standard_http_exception(detail: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    return HTTPException(status_code=code, detail=detail)