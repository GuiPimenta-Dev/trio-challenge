from src.application.errors import HttpException


class Unauthorized(HttpException):
    def __init__(self, message) -> None:
        super().__init__(status_code=401, message=message)
