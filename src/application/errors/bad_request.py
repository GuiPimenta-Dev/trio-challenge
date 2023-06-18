from src.application.errors import HttpException


class BadRequest(HttpException):
    def __init__(self, message) -> None:
        super().__init__(status_code=400, message=message)
