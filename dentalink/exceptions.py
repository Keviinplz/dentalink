class DentalinkClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DentalinkClientHTTPException(DentalinkClientException):
    def __init__(self, code: int, message: str):
        super().__init__(f"[HTTP {code}] {message}")
        self.code = code


class DentalinkClientQueryError(DentalinkClientException):
    def __init__(self, message: str):
        super().__init__(message)


class DentalinkClientFilterError(DentalinkClientQueryError):
    def __init__(self, field: str, message: str):
        super().__init__(f"Error en campo para filtrar '{field}': {message}")
        self.field = field
