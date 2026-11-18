"""Pruebas unitarias para la simulación main.py del proyecto Software FJ.

Verifica que main.py ejecuta al menos 10 operaciones completas,
incluyendo válidas e inválidas, sin excepciones no controladas,
y que el archivo de log se genera correctamente.
"""

import unittest
import tempfile
import os
import sys

# Agregar el directorio raíz al path para importar main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logger import configurar_logger


class TestSimulacion(unittest.TestCase):
    """Pruebas para la simulación main.py."""

    def setUp(self):
        """Configura logging temporal para pruebas."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.temp_dir.name, "eventos.log")

    def tearDown(self):
        """Limpia el directorio temporal."""
        self.temp_dir.cleanup()

    def test_main_ejecuta_sin_excepciones_no_controladas(self):
        """main.py se ejecuta completo sin lanzar excepciones no controladas."""
        from main import simular
        # No debe lanzar excepciones no controladas
        try:
            resultado = simular()
            self.assertIsNotNone(resultado)
        except Exception as error:
            self.fail(f"main.py lanzó excepción no controlada: {error}")

    def test_log_se_genera_despues_de_main(self):
        """Después de ejecutar main, el archivo de log existe."""
        from main import simular

        simular()

        log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "logs",
            "eventos.log",
        )
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, "r", encoding="utf-8") as f:
            contenido = f.read()
        self.assertIn("ERROR", contenido)
        self.assertIn("INFO", contenido)

    def test_main_retorna_resumen(self):
        """main.py retorna un resumen con exitosas y errores."""
        from main import simular
        resumen = simular()
        self.assertIsInstance(resumen, dict)
        self.assertIn("exitosas", resumen)
        self.assertIn("errores", resumen)
        self.assertGreaterEqual(resumen["exitosas"] + resumen["errores"], 10)


if __name__ == "__main__":
    unittest.main()
