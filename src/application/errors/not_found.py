from src.application.errors import HttpException


class NotFound(HttpException):
    def __init__(self, message) -> None:
        super().__init__(status_code=404, message=message)
