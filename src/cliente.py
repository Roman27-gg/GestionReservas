"""Clase Cliente del proyecto Software FJ.

Cliente hereda de Entidad y encapsula los datos personales con
validación robusta mediante @property y setters validados.

Datos encapsulados: nombre, documento, correo, teléfono.
"""

import re
from src.entidad import Entidad
from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.logger import logger

# Constantes de validación
NOMBRE_MIN_LONGITUD = 2
NOMBRE_MAX_LONGITUD = 100
DOCUMENTO_MIN_LONGITUD = 6
DOCUMENTO_MAX_LONGITUD = 12
TELEFONO_MIN_LONGITUD = 7
TELEFONO_MAX_LONGITUD = 15

# Patrones regex para validación
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$")
PATRON_DOCUMENTO = re.compile(r"^[A-Za-z0-9]{6,12}$")
PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PATRON_TELEFONO = re.compile(r"^[0-9\s\+\-]{7,15}$")


class Cliente(Entidad):
    """Cliente del sistema con datos personales encapsulados y validados.

    Hereda de Entidad y proporciona validación robusta de nombre,
    documento, correo y teléfono mediante propiedades y setters.
    """

    def __init__(
        self,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str,
    ) -> None:
        super().__init__()
        self._nombre: str = ""
        self._documento: str = ""
        self._correo: str = ""
        self._telefono: str = ""
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametrosFaltantesError("El nombre es obligatorio.")
        valor = valor.strip()
        if len(valor) < NOMBRE_MIN_LONGITUD:
            raise DatosInvalidosError(
                f"El nombre debe tener al menos {NOMBRE_MIN_LONGITUD} caracteres."
            )
        if len(valor) > NOMBRE_MAX_LONGITUD:
            raise DatosInvalidosError(
                f"El nombre no puede exceder {NOMBRE_MAX_LONGITUD} caracteres."
            )
        if not PATRON_NOMBRE.match(valor):
            raise DatosInvalidosError(
                "El nombre solo puede contener letras y espacios."
            )
        self._nombre = valor

    @property
    def documento(self) -> str:
        """Documento de identidad del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametrosFaltantesError("El documento es obligatorio.")
        valor = valor.strip().upper()
        if not PATRON_DOCUMENTO.match(valor):
            raise DatosInvalidosError(
                f"El documento debe ser alfanumérico de {DOCUMENTO_MIN_LONGITUD} a "
                f"{DOCUMENTO_MAX_LONGITUD} caracteres."
            )
        self._documento = valor

    @property
    def correo(self) -> str:
        """Correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametrosFaltantesError("El correo es obligatorio.")
        valor = valor.strip().lower()
        if not PATRON_CORREO.match(valor):
            raise DatosInvalidosError("El formato del correo electrónico es inválido.")
        self._correo = valor

    @property
    def telefono(self) -> str:
        """Teléfono de contacto del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametrosFaltantesError("El teléfono es obligatorio.")
        valor = valor.strip()
        if not PATRON_TELEFONO.match(valor):
            raise DatosInvalidosError(
                f"El teléfono debe tener entre {TELEFONO_MIN_LONGITUD} y "
                f"{TELEFONO_MAX_LONGITUD} caracteres numéricos."
            )
        self._telefono = valor

    def describir(self) -> str:
        """Devuelve una descripción completa del cliente.

        Returns:
            Cadena con los datos del cliente formateados.
        """
        return (
            f"Cliente(id={self.id}, nombre={self._nombre}, "
            f"documento={self._documento}, correo={self._correo}, "
            f"telefono={self._telefono})"
        )

    def __str__(self) -> str:
        return self.describir()


def crear_cliente(
    nombre: str,
    documento: str,
    correo: str,
    telefono: str,
) -> Cliente:
    """Crea un cliente validando todos los campos.

    Args:
        nombre: Nombre completo del cliente.
        documento: Documento de identidad (alfanumérico 6-12 chars).
        correo: Correo electrónico válido.
        telefono: Número de teléfono válido.

    Returns:
        Instancia de Cliente creada y validada.

    Raises:
        DatosInvalidosError: Si algún campo no cumple la validación.
        ParametrosFaltantesError: Si falta algún campo obligatorio.
    """
    try:
        cliente = Cliente(
            nombre=nombre,
            documento=documento,
            correo=correo,
            telefono=telefono,
        )
        logger.info("Cliente creado exitosamente: %s", cliente.describir())
        return cliente
    except (DatosInvalidosError, ParametrosFaltantesError) as error:
        logger.error("Error creando cliente: %s", error)
        raise
