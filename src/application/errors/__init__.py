from functools import wraps

from fastapi.responses import JSONResponse


def error_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            return JSONResponse(status_code=400, content={"error": error_message})

    return wrapper
