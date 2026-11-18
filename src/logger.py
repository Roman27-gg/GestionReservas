"""Configuración del sistema de logging para el proyecto Software FJ.

Registra todos los errores y eventos relevantes en el archivo
logs/eventos.log con fecha, nivel y mensaje. Utiliza únicamente la
librería estándar de Python (modulo logging).
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Constantes de configuración del log
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "eventos.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Nivel de logging
CONSOLE_LEVEL = logging.INFO
FILE_LEVEL = logging.DEBUG


def configurar_logger(nombre: str = "software_fj") -> logging.Logger:
    """Configura y devuelve un logger con handlers de archivo y consola.

    Args:
        nombre: Nombre del logger.

    Returns:
        Logger configurado listo para registrar eventos y errores.
    """
    # Crear directorio de logs si no existe
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si el logger ya está configurado
    if logger.handlers:
        return logger

    # Handler de archivo con rotación
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(FILE_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LEVEL)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Logger por defecto del módulo
logger = configurar_logger(__name__)
