from backend.src.errors.custom_error import CustomError
from fastapi import Request
from fastapi.responses import JSONResponse


def error_handler(req: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.status_code, content={"errors": exc.serialize_errors()}
    )
