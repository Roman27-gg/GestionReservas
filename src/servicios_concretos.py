"""Servicios concretos del proyecto Software FJ.

Implementa tres servicios concretos que sobrescriben los métodos
abstractos de Servicio: ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Cada uno aplica polimorfismo mediante sobrescritura de calcular_costo,
describir y validar_parametros.
"""

import re
from typing import Optional
from src.servicio import Servicio, IVA, DESCUENTO_MAX
from src.excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametrosFaltantesError,
    ServicioNoDisponibleError,
)
from src.logger import logger

# Constantes específicas de cada servicio
# ReservaSala
COSTO_HORA_SALA_BASICA = 50.0
COSTO_HORA_SALA_VIP = 120.0
COSTO_EXTRA_EQUIPAMIENTO = 30.0

# AlquilerEquipo
COSTO_DIA_EQUIPO_BASICO = 20.0
COSTO_DIA_EQUIPO_PROFESIONAL = 80.0
COSTO_TECNICO_POR_DIA = 40.0

# AsesoriaEspecializada
COSTO_HORA_ASESORIA_JUNIOR = 60.0
COSTO_HORA_ASESORIA_SENIOR = 120.0
COSTO_HORA_ASESORIA_EXPERTO = 200.0
RECARGO_MODALIDAD_PRESENCIAL = 1.10  # 10% extra presencial


class ReservaSala(Servicio):
    """Servicio de reserva de salas.

    Parámetros: tipo_sala, capacidad, equipamiento.
    Costo base por hora + extra por equipamiento.
    """

    def __init__(
        self,
        tipo_sala: str,
        capacidad: int,
        equipamiento: bool = False,
        disponible: bool = True,
        costo_base: Optional[float] = None,
        nombre: Optional[str] = None,
    ) -> None:
        if nombre is None:
            nombre = f"Reserva de Sala - {tipo_sala}"
        if costo_base is None:
            costo_base = COSTO_HORA_SALA_VIP if tipo_sala.upper() == "VIP" else COSTO_HORA_SALA_BASICA
        super().__init__(nombre=nombre, costo_base=costo_base, disponible=disponible)
        self.tipo_sala: str = tipo_sala.strip()
        self.capacidad: int = capacidad
        self.equipamiento: bool = equipamiento

    def calcular_costo(
        self,
        duracion: float,
        con_impuesto: bool = False,
        descuento: float = 0.0,
        **kwargs,
    ) -> float:
        """Calcula el costo de reserva de sala.

        Args:
            duracion: Horas de reserva.
            con_impuesto: Aplicar IVA.
            descuento: Descuento porcentual.
            **kwargs: Parámetros adicionales (ignored).

        Returns:
            Costo total de la reserva de sala.
        """
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor a 0 horas.")

        costo = self.costo_base * duracion
        if self.equipamiento:
            costo += COSTO_EXTRA_EQUIPAMIENTO * duracion

        return self._aplicar_impuesto_y_descuento(costo, con_impuesto, descuento)

    def describir(self) -> str:
        """Devuelve descripción del servicio de reserva de sala."""
        return (
            f"ReservaSala(id={self.id}, tipo_sala={self.tipo_sala}, "
            f"capacidad={self.capacidad}, equipamiento={self.equipamiento}, "
            f"costo_base={self.costo_base}/hora, disponible={self.disponible})"
        )

    def validar_parametros(self, **kwargs) -> None:
        """Valida parámetros específicos de ReservaSala."""
        tipo_sala = kwargs.get("tipo_sala", self.tipo_sala)
        capacidad = kwargs.get("capacidad", self.capacidad)

        if not tipo_sala or not isinstance(tipo_sala, str):
            raise ParametrosFaltantesError("El tipo de sala es obligatorio.")
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser un entero positivo.")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos.

    Parámetros: tipo_equipo, cantidad, incluye_tecnico.
    Costo base por día + costo técnico opcional.
    """

    def __init__(
        self,
        tipo_equipo: str,
        cantidad: int,
        incluye_tecnico: bool = False,
        disponible: bool = True,
        costo_base: Optional[float] = None,
        nombre: Optional[str] = None,
    ) -> None:
        if nombre is None:
            nombre = f"Alquiler de Equipo - {tipo_equipo}"
        if costo_base is None:
            costo_base = (
                COSTO_DIA_EQUIPO_PROFESIONAL
                if tipo_equipo.upper() == "PROFESIONAL"
                else COSTO_DIA_EQUIPO_BASICO
            )
        super().__init__(nombre=nombre, costo_base=costo_base, disponible=disponible)
        self.tipo_equipo: str = tipo_equipo.strip()
        self.cantidad: int = cantidad
        self.incluye_tecnico: bool = incluye_tecnico

    def calcular_costo(
        self,
        duracion: float,
        con_impuesto: bool = False,
        descuento: float = 0.0,
        cantidad_reservada: int = 1,
        **kwargs,
    ) -> float:
        """Calcula el costo de alquiler de equipo.

        Args:
            duracion: Días de alquiler.
            con_impuesto: Aplicar IVA.
            descuento: Descuento porcentual.
            cantidad_reservada: Cantidad de equipos a reservar.
            **kwargs: Parámetros adicionales (ignored).

        Returns:
            Costo total del alquiler de equipo.
        """
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor a 0 días.")
        if cantidad_reservada <= 0:
            raise DatosInvalidosError("La cantidad reservada debe ser mayor a 0.")

        costo = self.costo_base * duracion * cantidad_reservada
        if self.incluye_tecnico:
            costo += COSTO_TECNICO_POR_DIA * duracion * cantidad_reservada

        return self._aplicar_impuesto_y_descuento(costo, con_impuesto, descuento)

    def describir(self) -> str:
        """Devuelve descripción del servicio de alquiler de equipo."""
        return (
            f"AlquilerEquipo(id={self.id}, tipo_equipo={self.tipo_equipo}, "
            f"cantidad={self.cantidad}, incluye_tecnico={self.incluye_tecnico}, "
            f"costo_base={self.costo_base}/día, disponible={self.disponible})"
        )

    def validar_parametros(self, **kwargs) -> None:
        """Valida parámetros específicos de AlquilerEquipo."""
        tipo_equipo = kwargs.get("tipo_equipo", self.tipo_equipo)
        cantidad = kwargs.get("cantidad", self.cantidad)

        if not tipo_equipo or not isinstance(tipo_equipo, str):
            raise ParametrosFaltantesError("El tipo de equipo es obligatorio.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser un entero positivo.")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada.

    Parámetros: especialidad, nivel_experto, modalidad.
    Costo base por hora + recargo por modalidad presencial.
    """

    def __init__(
        self,
        especialidad: str,
        nivel_experto: str = "JUNIOR",
        modalidad: str = "virtual",
        disponible: bool = True,
        costo_base: Optional[float] = None,
        nombre: Optional[str] = None,
    ) -> None:
        if nombre is None:
            nombre = f"Asesoría - {especialidad}"
        nivel = nivel_experto.upper()
        if costo_base is None:
            if nivel == "JUNIOR":
                costo_base = COSTO_HORA_ASESORIA_JUNIOR
            elif nivel == "SENIOR":
                costo_base = COSTO_HORA_ASESORIA_SENIOR
            elif nivel == "EXPERTO":
                costo_base = COSTO_HORA_ASESORIA_EXPERTO
            else:
                costo_base = COSTO_HORA_ASESORIA_JUNIOR

        super().__init__(nombre=nombre, costo_base=costo_base, disponible=disponible)
        self.especialidad: str = especialidad.strip()
        self.nivel_experto: str = nivel
        self.modalidad: str = modalidad.strip().lower()

    def calcular_costo(
        self,
        duracion: float,
        con_impuesto: bool = False,
        descuento: float = 0.0,
        **kwargs,
    ) -> float:
        """Calcula el costo de asesoría especializada.

        Args:
            duracion: Horas de asesoría.
            con_impuesto: Aplicar IVA.
            descuento: Descuento porcentual.
            **kwargs: Parámetros adicionales (ignored).

        Returns:
            Costo total de la asesoría.
        """
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor a 0 horas.")

        costo = self.costo_base * duracion

        if self.modalidad == "presencial":
            costo *= RECARGO_MODALIDAD_PRESENCIAL

        return self._aplicar_impuesto_y_descuento(costo, con_impuesto, descuento)

    def describir(self) -> str:
        """Devuelve descripción del servicio de asesoría."""
        return (
            f"AsesoriaEspecializada(id={self.id}, especialidad={self.especialidad}, "
            f"nivel_experto={self.nivel_experto}, modalidad={self.modalidad}, "
            f"costo_base={self.costo_base}/hora, disponible={self.disponible})"
        )

    def validar_parametros(self, **kwargs) -> None:
        """Valida parámetros específicos de AsesoriaEspecializada."""
        especialidad = kwargs.get("especialidad", self.especialidad)
        nivel_experto = kwargs.get("nivel_experto", self.nivel_experto)
        modalidad = kwargs.get("modalidad", self.modalidad)

        if not especialidad or not isinstance(especialidad, str):
            raise ParametrosFaltantesError("La especialidad es obligatoria.")
        if nivel_experto.upper() not in ("JUNIOR", "SENIOR", "EXPERTO"):
            raise DatosInvalidosError(
                "El nivel de experto debe ser JUNIOR, SENIOR o EXPERTO."
            )
        if modalidad.lower() not in ("presencial", "virtual"):
            raise DatosInvalidosError("La modalidad debe ser 'presencial' o 'virtual'.")


def crear_servicio(
    tipo: str,
    **kwargs,
) -> Servicio:
    """Factory para crear servicios concretos por tipo.

    Args:
        tipo: Tipo de servicio ('ReservaSala', 'AlquilerEquipo', 'AsesoriaEspecializada').
        **kwargs: Parámetros específicos del servicio.

    Returns:
        Instancia del servicio concreto creado.

    Raises:
        DatosInvalidosError: Si el tipo de servicio no es válido.
    """
    try:
        if tipo == "ReservaSala":
            servicio = ReservaSala(**kwargs)
        elif tipo == "AlquilerEquipo":
            servicio = AlquilerEquipo(**kwargs)
        elif tipo == "AsesoriaEspecializada":
            servicio = AsesoriaEspecializada(**kwargs)
        else:
            raise DatosInvalidosError(
                f"Tipo de servicio no válido: {tipo}. "
                f"Opciones: ReservaSala, AlquilerEquipo, AsesoriaEspecializada."
            )

        servicio.validar_parametros(**kwargs)
        logger.info("Servicio creado: %s", servicio.describir())
        return servicio
    except (
        DatosInvalidosError,
        ParametrosFaltantesError,
        CalculoInconsistenteError,
    ) as error:
        logger.error("Error creando servicio %s: %s", tipo, error)
        raise
