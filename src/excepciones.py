"""Jerarquía de excepciones personalizadas del proyecto Software FJ.

Todas las excepciones heredan de SoftwareFJError para permitir captura
polimórfica y diferenciada de errores del sistema.

Prohibido silenciar errores con pass; cada excepción capturada debe
registrarse en el log antes de continuar.
"""


class SoftwareFJError(Exception):
    """Excepción base del proyecto Software FJ.

    Todas las excepciones personalizadas del sistema heredan de esta
    clase para permitir captura genérica y diferenciada.
    """

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatosInvalidosError(SoftwareFJError):
    """Datos proporcionados no cumplen las reglas de validación."""


class ParametrosFaltantesError(SoftwareFJError):
    """Faltan parámetros obligatorios para una operación."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida en el estado actual del objeto."""


class ReservaIncorrectaError(SoftwareFJError):
    """Datos de reserva inconsistentes o inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Servicio solicitado no está disponible."""


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculo de costo produjo un resultado inconsistente."""
