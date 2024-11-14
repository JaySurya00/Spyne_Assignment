from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_error(request: Request, exc: RequestValidationError):
    errorsList: list = []

    for error in exc.errors():
        errorsList.append({"message": error["msg"], "field": error["loc"][1]})

    return JSONResponse(
        status_code=400,
        content={"errors": errorsList},
    )
