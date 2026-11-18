"""Clase Gestor del proyecto Software FJ.

Orquesta las operaciones del sistema manteniendo listas internas de
clientes, servicios y reservas en memoria. No utiliza base de datos.
"""

from typing import Optional, List
from src.cliente import Cliente
from src.servicio import Servicio
from src.reserva import Reserva, EstadoReserva
from src.excepciones import (
    DatosInvalidosError,
    ParametrosFaltantesError,
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
)
from src.logger import logger


class Gestor:
    """Gestor centralizado de clientes, servicios y reservas.

    Mantiene listas internas en memoria y proporciona métodos para
    crear, consultar y operar sobre las entidades del sistema.
    """

    def __init__(self) -> None:
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

    # --- Clientes ---

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Registra un cliente en el sistema.

        Args:
            cliente: Instancia de Cliente a registrar.

        Raises:
            DatosInvalidosError: Si el cliente no es válido.
            ParametrosFaltantesError: Si falta el cliente.
        """
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto no es una instancia de Cliente.")
        self._clientes.append(cliente)
        logger.info("Cliente registrado en gestor: id=%d", cliente.id)

    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Busca un cliente por su ID.

        Args:
            cliente_id: ID del cliente.

        Returns:
            Cliente encontrado o None si no existe.
        """
        for cliente in self._clientes:
            if cliente.id == cliente_id:
                return cliente
        return None

    def listar_clientes(self) -> List[Cliente]:
        """Devuelve la lista de todos los clientes registrados."""
        return list(self._clientes)

    # --- Servicios ---

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Registra un servicio en el sistema.

        Args:
            servicio: Instancia de Servicio a registrar.

        Raises:
            DatosInvalidosError: Si el servicio no es válido.
        """
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto no es una instancia de Servicio.")
        self._servicios.append(servicio)
        logger.info("Servicio registrado en gestor: id=%d", servicio.id)

    def obtener_servicio(self, servicio_id: int) -> Optional[Servicio]:
        """Busca un servicio por su ID.

        Args:
            servicio_id: ID del servicio.

        Returns:
            Servicio encontrado o None si no existe.
        """
        for servicio in self._servicios:
            if servicio.id == servicio_id:
                return servicio
        return None

    def listar_servicios(self) -> List[Servicio]:
        """Devuelve la lista de todos los servicios registrados."""
        return list(self._servicios)

    # --- Reservas ---

    def crear_reserva(
        self,
        cliente_id: int,
        servicio_id: int,
        duracion: float,
    ) -> Reserva:
        """Crea una reserva asociando cliente y servicio.

        Args:
            cliente_id: ID del cliente.
            servicio_id: ID del servicio.
            duracion: Duración de la reserva.

        Returns:
            Instancia de Reserva creada.

        Raises:
            DatosInvalidosError: Si cliente o servicio no existen.
            ServicioNoDisponibleError: Si el servicio no está disponible.
        """
        cliente = self.obtener_cliente(cliente_id)
        servicio = self.obtener_servicio(servicio_id)

        if cliente is None:
            raise DatosInvalidosError(
                f"No existe un cliente con id={cliente_id}."
            )
        if servicio is None:
            raise DatosInvalidosError(
                f"No existe un servicio con id={servicio_id}."
            )
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible."
            )

        reserva = Reserva(cliente=cliente, servicio=servicio, duracion=duracion)
        self._reservas.append(reserva)
        logger.info(
            "Reserva creada: id=%d, cliente_id=%d, servicio_id=%d, duracion=%.2f",
            reserva.id,
            cliente_id,
            servicio_id,
            duracion,
        )
        return reserva

    def obtener_reserva(self, reserva_id: int) -> Optional[Reserva]:
        """Busca una reserva por su ID.

        Args:
            reserva_id: ID de la reserva.

        Returns:
            Reserva encontrada o None si no existe.
        """
        for reserva in self._reservas:
            if reserva.id == reserva_id:
                return reserva
        return None

    def listar_reservas(self) -> List[Reserva]:
        """Devuelve la lista de todas las reservas."""
        return list(self._reservas)

    def confirmar_reserva(self, reserva_id: int) -> None:
        """Confirma una reserva por su ID.

        Args:
            reserva_id: ID de la reserva.

        Raises:
            DatosInvalidosError: Si la reserva no existe.
            OperacionNoPermitidaError: Si no se puede confirmar.
        """
        reserva = self.obtener_reserva(reserva_id)
        if reserva is None:
            raise DatosInvalidosError(
                f"No existe una reserva con id={reserva_id}."
            )
        reserva.confirmar()

    def cancelar_reserva(self, reserva_id: int) -> None:
        """Cancela una reserva por su ID.

        Args:
            reserva_id: ID de la reserva.

        Raises:
            DatosInvalidosError: Si la reserva no existe.
            OperacionNoPermitidaError: Si no se puede cancelar.
        """
        reserva = self.obtener_reserva(reserva_id)
        if reserva is None:
            raise DatosInvalidosError(
                f"No existe una reserva con id={reserva_id}."
            )
        reserva.cancelar()

    def procesar_reserva(self, reserva_id: int) -> float:
        """Procesa una reserva por su ID y devuelve el costo calculado.

        Args:
            reserva_id: ID de la reserva.

        Returns:
            Costo calculado de la reserva procesada.

        Raises:
            DatosInvalidosError: Si la reserva no existe.
            OperacionNoPermitidaError: Si no se puede procesar.
        """
        reserva = self.obtener_reserva(reserva_id)
        if reserva is None:
            raise DatosInvalidosError(
                f"No existe una reserva con id={reserva_id}."
            )
        reserva.procesar()
        costo = reserva.servicio.calcular_costo(reserva.duracion)
        return costo

    def resumen_operaciones(
        self,
        exitosas: int,
        errores: int,
    ) -> str:
        """Genera un resumen de las operaciones realizadas.

        Args:
            exitosas: Cantidad de operaciones exitosas.
            errores: Cantidad de errores controlados.

        Returns:
            Cadena con el resumen formateado.
        """
        total = exitosas + errores
        return (
            f"\n{'='*50}\n"
            f"RESUMEN DE OPERACIONES\n"
            f"{'='*50}\n"
            f"Total de operaciones: {total}\n"
            f"Exitosas: {exitosas}\n"
            f"Errores controlados: {errores}\n"
            f"{'='*50}\n"
        )
