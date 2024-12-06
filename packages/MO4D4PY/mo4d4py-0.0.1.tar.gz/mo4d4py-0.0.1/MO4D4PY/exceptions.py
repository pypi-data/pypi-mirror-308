class APIError(Exception):
    """Excepción genérica para errores de la API"""
    pass

class TimeoutError(Exception):
    """Excepción para errores de timeout"""
    pass