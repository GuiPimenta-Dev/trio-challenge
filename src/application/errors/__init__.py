from functools import wraps

from fastapi.responses import JSONResponse


class HttpException(Exception):
    def __init__(self, status_code, message) -> None:
        self.status_code = status_code
        self.message = message

    @staticmethod
    def handle_exceptions(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)

            except HttpException as e:
                return JSONResponse(
                    status_code=e.status_code, content={"error": e.message}
                )

            except Exception as e:
                error_message = str(e)
                return JSONResponse(status_code=500, content={"error": error_message})

        return wrapper
