import typing

class ApiError(Exception):
    status_code: int
    body: typing.Any

    def __init__(self, status_code: int, body: typing.Any = None):
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return f'Status Code: {self.status_code}, body: {self.body}'