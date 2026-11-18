"""Clase abstracta Servicio del proyecto Software FJ.

Define la interfaz común para todos los servicios: calcular costo,
describir y validar parámetros. Incluye variantes sobrecargadas de
calculo de costo usando argumentos por defecto y **kwargs.
"""

from abc import ABC, abstractmethod
from src.entidad import Entidad
from src.excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametrosFaltantesError,
)
from src.logger import logger

# Constantes de cálculo de costo
IVA = 0.19
DESCUENTO_MAX = 0.30


class Servicio(Entidad, ABC):
    """Clase abstracta base para todos los servicios del sistema.

    Define los métodos abstractos que todo servicio concreto debe
    implementar: calcular_costo, describir y validar_parametros.
    """

    def __init__(
        self,
        nombre: str,
        costo_base: float,
        disponible: bool = True,
    ) -> None:
        super().__init__()
        self._nombre: str = nombre
        self._costo_base: float = costo_base
        self.disponible: bool = disponible

    @property
    def nombre(self) -> str:
        """Nombre del servicio."""
        return self._nombre

    @property
    def costo_base(self) -> float:
        """Costo base del servicio."""
        return self._costo_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo(
        self,
        duracion: float,
        con_impuesto: bool = False,
        descuento: float = 0.0,
        **kwargs,
    ) -> float:
        """Calcula el costo del servicio para una duración dada.

        Técnica de sobrecarga: argumentos por defecto y **kwargs.
        Variantes:
            - calcular_costo(duracion) -> costo base sin extras
            - calcular_costo(duracion, con_impuesto=True) -> con IVA
            - calcular_costo(duracion, descuento=0.1) -> con descuento
            - calcular_costo(duracion, con_impuesto=True, descuento=0.1) -> ambos

        Args:
            duracion: Duración del servicio en horas.
            con_impuesto: Si se aplica el IVA (19%).
            descuento: Descuento porcentual (0.0 a 0.30).
            **kwargs: Parámetros adicionales específicos del servicio.

        Returns:
            Costo total calculado.

        Raises:
            DatosInvalidosError: Si duracion es inválida o descuento fuera de rango.
            CalculoInconsistenteError: Si el resultado del cálculo es negativo.
        """

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción del servicio."""

    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        """Valida los parámetros específicos del servicio."""

    def _aplicar_impuesto_y_descuento(self, costo: float, con_impuesto: bool, descuento: float) -> float:
        """Aplica impuesto y descuento a un costo base.

        Args:
            costo: Costo base.
            con_impuesto: Si aplicar IVA.
            descuento: Descuento porcentual.

        Returns:
            Costo final con impuesto y/o descuento.

        Raises:
            DatosInvalidosError: Si descuento está fuera de rango.
            CalculoInconsistenteError: Si el resultado es negativo.
        """
        if descuento < 0 or descuento > DESCUENTO_MAX:
            raise DatosInvalidosError(
                f"El descuento debe estar entre 0 y {DESCUENTO_MAX * 100:.0f}%."
            )

        resultado = costo
        if descuento > 0:
            resultado = resultado * (1 - descuento)

        if con_impuesto:
            resultado = resultado * (1 + IVA)

        if resultado < 0:
            raise CalculoInconsistenteError(
                f"El costo calculado es negativo: {resultado}"
            )

        return resultado

    def __str__(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return f"{self.__class__.__name__}(id={self.id}, nombre={self._nombre}, {estado})"
