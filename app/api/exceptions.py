from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    exceptions = exc.errors()

    if len(exceptions) == 1:
        return JSONResponse(
            content={
                "detail": f"{'.'.join(exceptions[0]['loc'])}: {exceptions[0]["msg"].capitalize()}"
            },
            status_code=422
        )
    else:
        return JSONResponse(
            content={
                "detail": [error["msg"] for error in exceptions]
            },
            status_code=422
        ) 