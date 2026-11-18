"""Clase abstracta base Entidad del proyecto Software FJ.

Representa entidades generales del sistema con un identificador único
auto-incremental y un método abstracto describir().
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema.

    Proporciona un identificador único auto-incremental y define la
    interfaz común que todas las entidades deben implementar.
    """

    _contador_id: int = 0

    def __init__(self) -> None:
        Entidad._contador_id += 1
        self.id: int = Entidad._contador_id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción textual de la entidad.

        Returns:
            Cadena con la descripción de la entidad.
        """

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __repr__(self) -> str:
        return self.__str__()
