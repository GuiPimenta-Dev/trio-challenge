from src.application.errors import HttpException


class Forbidden(HttpException):
    def __init__(self, message) -> None:
        super().__init__(status_code=403, message=message)
