from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime


def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail,
            "codigo": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "erro": "Erro interno do servidor",
            "codigo": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )