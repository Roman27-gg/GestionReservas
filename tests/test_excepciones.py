"""Pruebas unitarias para las excepciones personalizadas del proyecto Software FJ.

Verifica que cada excepción personalizada se lanza correctamente,
que la jerarquía de herencia es correcta y que el encadenamiento
(__cause__) está presente donde corresponde.
"""

import unittest
import tempfile
import os

# Configurar logging temporal para pruebas
from src.logger import configurar_logger
from src.excepciones import (
    SoftwareFJError,
    DatosInvalidosError,
    ParametrosFaltantesError,
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class TestExcepciones(unittest.TestCase):
    """Pruebas para la jerarquía de excepciones personalizadas."""

    def setUp(self):
        """Configura logging temporal para cada prueba."""
        self.temp_dir = tempfile.TemporaryDirectory()
        # Redirigir el logger a un archivo temporal
        self.log_handler = None
        self.logger = configurar_logger("test_excepciones")

    def tearDown(self):
        """Limpia el directorio temporal después de cada prueba."""
        self.temp_dir.cleanup()

    def test_software_fj_error_es_base(self):
        """SoftwareFJError es la clase base de todas las excepciones."""
        self.assertTrue(issubclass(DatosInvalidosError, SoftwareFJError))
        self.assertTrue(issubclass(ParametrosFaltantesError, SoftwareFJError))
        self.assertTrue(issubclass(OperacionNoPermitidaError, SoftwareFJError))
        self.assertTrue(issubclass(ReservaIncorrectaError, SoftwareFJError))
        self.assertTrue(issubclass(ServicioNoDisponibleError, SoftwareFJError))
        self.assertTrue(issubclass(CalculoInconsistenteError, SoftwareFJError))

    def test_datos_invalidos_error_se_lanza(self):
        """DatosInvalidosError se lanza y captura correctamente."""
        with self.assertRaises(DatosInvalidosError) as contexto:
            raise DatosInvalidosError("Dato inválido de prueba")
        self.assertEqual(str(contexto.exception), "Dato inválido de prueba")
        self.assertIsInstance(contexto.exception, SoftwareFJError)

    def test_parametros_faltantes_error_se_lanza(self):
        """ParametrosFaltantesError se lanza y captura correctamente."""
        with self.assertRaises(ParametrosFaltantesError) as contexto:
            raise ParametrosFaltantesError("Falta parámetro obligatorio")
        self.assertEqual(str(contexto.exception), "Falta parámetro obligatorio")

    def test_operacion_no_permitida_error_se_lanza(self):
        """OperacionNoPermitidaError se lanza y captura correctamente."""
        with self.assertRaises(OperacionNoPermitidaError) as contexto:
            raise OperacionNoPermitidaError("Operación no permitida")
        self.assertEqual(str(contexto.exception), "Operación no permitida")

    def test_reserva_incorrecta_error_se_lanza(self):
        """ReservaIncorrectaError se lanza y captura correctamente."""
        with self.assertRaises(ReservaIncorrectaError) as contexto:
            raise ReservaIncorrectaError("Reserva incorrecta")
        self.assertEqual(str(contexto.exception), "Reserva incorrecta")

    def test_servicio_no_disponible_error_se_lanza(self):
        """ServicioNoDisponibleError se lanza y captura correctamente."""
        with self.assertRaises(ServicioNoDisponibleError) as contexto:
            raise ServicioNoDisponibleError("Servicio no disponible")
        self.assertEqual(str(contexto.exception), "Servicio no disponible")

    def test_calculo_inconsistente_error_se_lanza(self):
        """CalculoInconsistenteError se lanza y captura correctamente."""
        with self.assertRaises(CalculoInconsistenteError) as contexto:
            raise CalculoInconsistenteError("Cálculo inconsistente")
        self.assertEqual(str(contexto.exception), "Cálculo inconsistente")

    def test_encadenamiento_excepciones(self):
        """El encadenamiento de excepciones (__cause__) está presente."""
        try:
            try:
                raise ValueError("Error original")
            except ValueError as error_original:
                raise DatosInvalidosError("Error envuelto") from error_original
        except DatosInvalidosError as error_envuelto:
            self.assertIsInstance(error_envuelto.__cause__, ValueError)
            self.assertEqual(str(error_envuelto.__cause__), "Error original")

    def test_captura_polimerfica_software_fj_error(self):
        """Todas las excepciones hijas se capturan con SoftwareFJError."""
        excepciones = [
            DatosInvalidosError("e1"),
            ParametrosFaltantesError("e2"),
            OperacionNoPermitidaError("e3"),
            ReservaIncorrectaError("e4"),
            ServicioNoDisponibleError("e5"),
            CalculoInconsistenteError("e6"),
        ]
        for exc in excepciones:
            with self.assertRaises(SoftwareFJError):
                raise exc

    def test_mensaje_excepcion_se_preserva(self):
        """El mensaje de la excepción se preserva en el atributo mensaje."""
        exc = DatosInvalidosError("Mensaje de prueba")
        self.assertEqual(exc.mensaje, "Mensaje de prueba")
        self.assertEqual(str(exc), "Mensaje de prueba")


if __name__ == "__main__":
    unittest.main()
