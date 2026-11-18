"""Clase Reserva del proyecto Software FJ.

Reserva integra cliente, servicio, duración y estado.
Implementa confirmar(), cancelar() y procesar() con manejo de
excepciones. Utiliza try/except, try/except/else y try/except/finally.

Estados: PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA.
"""

from enum import Enum
from src.entidad import Entidad
from src.cliente import Cliente
from src.servicio import Servicio
from src.excepciones import (
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
    DatosInvalidosError,
)
from src.logger import logger


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"


class Reserva(Entidad):
    """Reserva que integra cliente, servicio, duración y estado.

    Atributos:
        cliente: Cliente asociado a la reserva.
        servicio: Servicio reservado.
        duracion: Duración del servicio.
        estado: Estado actual de la reserva (Enum EstadoReserva).
    """

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
    ) -> None:
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente debe ser una instancia de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio debe ser una instancia de Servicio.")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser un número mayor a 0.")

        self._cliente: Cliente = cliente
        self._servicio: Servicio = servicio
        self._duracion: float = float(duracion)
        self._estado: EstadoReserva = EstadoReserva.PENDIENTE

    @property
    def cliente(self) -> Cliente:
        """Cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Servicio reservado."""
        return self._servicio

    @property
    def duracion(self) -> float:
        """Duración de la reserva."""
        return self._duracion

    @property
    def estado(self) -> EstadoReserva:
        """Estado actual de la reserva."""
        return self._estado

    def confirmar(self) -> None:
        """Confirma la reserva si está pendiente y el servicio está disponible.

        Raises:
            OperacionNoPermitidaError: Si la reserva ya no está pendiente.
            ServicioNoDisponibleError: Si el servicio no está disponible.
        """
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado {self._estado.value}."
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible."
                )
        except (OperacionNoPermitidaError, ServicioNoDisponibleError) as error:
            logger.error(
                "Error confirmando reserva id=%s: %s", self.id, error
            )
            raise
        else:
            self._estado = EstadoReserva.CONFIRMADA
            logger.info(
                "Reserva id=%s confirmada para cliente %s", self.id, self._cliente.nombre
            )
        finally:
            logger.debug(
                "Finalizó intento de confirmar reserva id=%s, estado=%s",
                self.id,
                self._estado.value,
            )

    def cancelar(self) -> None:
        """Cancela la reserva si no está procesada.

        Raises:
            OperacionNoPermitidaError: Si la reserva ya está procesada.
        """
        try:
            if self._estado == EstadoReserva.PROCESADA:
                raise OperacionNoPermitidaError(
                    "No se puede cancelar una reserva ya procesada."
                )
            if self._estado == EstadoReserva.CANCELADA:
                raise OperacionNoPermitidaError(
                    "La reserva ya está cancelada."
                )
        except OperacionNoPermitidaError as error:
            logger.error(
                "Error cancelando reserva id=%s: %s", self.id, error
            )
            raise
        else:
            self._estado = EstadoReserva.CANCELADA
            logger.info(
                "Reserva id=%s cancelada para cliente %s", self.id, self._cliente.nombre
            )
        finally:
            logger.debug(
                "Finalizó intento de cancelar reserva id=%s, estado=%s",
                self.id,
                self._estado.value,
            )

    def procesar(self) -> None:
        """Procesa la reserva ejecutando el servicio.

        Solo se puede procesar una reserva confirmada.
        Calcula el costo del servicio y marca como procesada.

        Raises:
            OperacionNoPermitidaError: Si la reserva no está confirmada.
        """
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas confirmadas. "
                    f"Estado actual: {self._estado.value}."
                )
            costo = self._servicio.calcular_costo(self._duracion)
        except OperacionNoPermitidaError as error:
            logger.error(
                "Error procesando reserva id=%s: %s", self.id, error
            )
            raise
        except Exception as error_original:
            logger.error(
                "Error inesperado procesando reserva id=%s: %s",
                self.id,
                error_original,
            )
            raise CalculoInconsistenteError(
                f"Error calculando costo para reserva id={self.id}"
            ) from error_original
        else:
            self._estado = EstadoReserva.PROCESADA
            logger.info(
                "Reserva id=%s procesada. Costo: %.2f",
                self.id,
                costo,
            )
        finally:
            logger.debug(
                "Finalizó intento de procesar reserva id=%s, estado=%s",
                self.id,
                self._estado.value,
            )

    def describir(self) -> str:
        """Devuelve una descripción completa de la reserva.

        Returns:
            Cadena con todos los datos de la reserva.
        """
        return (
            f"Reserva(id={self.id}, cliente={self._cliente.nombre}, "
            f"servicio={self._servicio.nombre}, duracion={self._duracion}, "
            f"estado={self._estado.value})"
        )

    def __str__(self) -> str:
        return self.describir()
