"""Pruebas unitarias para la clase Cliente del proyecto Software FJ.

Cobertura:
- Datos válidos
- Datos inválidos por cada campo (nombre, documento, correo, teléfono)
- Encapsulación (no se puede asignar valor inválido vía property)
"""

import unittest
import tempfile

from src.cliente import Cliente, crear_cliente
from src.excepciones import (
    DatosInvalidosError,
    ParametrosFaltantesError,
)


class TestCliente(unittest.TestCase):
    """Pruebas para la clase Cliente."""

    def test_crear_cliente_valido(self):
        """Cliente con datos válidos se crea correctamente."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="juan@email.com",
            telefono="3001234567",
        )
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.documento, "ABC12345")
        self.assertEqual(cliente.correo, "juan@email.com")
        self.assertEqual(cliente.telefono, "3001234567")
        self.assertIsInstance(cliente.id, int)
        self.assertGreater(cliente.id, 0)

    def test_crear_cliente_via_factory(self):
        """crear_cliente factory crea un cliente válido."""
        cliente = crear_cliente(
            nombre="María García",
            documento="XYZ98765",
            correo="maria@email.com",
            telefono="3019876543",
        )
        self.assertIsInstance(cliente, Cliente)
        self.assertEqual(cliente.nombre, "María García")

    def test_nombre_vacio_lanza_parametros_faltantes(self):
        """Nombre vacío lanza ParametrosFaltantesError."""
        with self.assertRaises(ParametrosFaltantesError):
            Cliente(
                nombre="",
                documento="ABC12345",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_nombre_solo_espacios_lanza_datos_invalidos(self):
        """Nombre solo espacios lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="   ",
                documento="ABC12345",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_nombre_con_numeros_lanza_datos_invalidos(self):
        """Nombre con números lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan123",
                documento="ABC12345",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_documento_muy_corto_lanza_datos_invalidos(self):
        """Documento menor a 6 caracteres lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="AB12",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_documento_muy_largo_lanza_datos_invalidos(self):
        """Documento mayor a 12 caracteres lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="ABCDEFGHIJKLM",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_documento_con_espacios_lanza_datos_invalidos(self):
        """Documento con espacios lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="AB 12345",
                correo="test@email.com",
                telefono="3001234567",
            )

    def test_correo_invalido_lanza_datos_invalidos(self):
        """Correo sin @ lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="ABC12345",
                correo="correo-invalido",
                telefono="3001234567",
            )

    def test_correo_sin_dominio_lanza_datos_invalidos(self):
        """Correo sin dominio lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="ABC12345",
                correo="usuario@",
                telefono="3001234567",
            )

    def test_telefono_muy_corto_lanza_datos_invalidos(self):
        """Teléfono menor a 7 caracteres lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="ABC12345",
                correo="test@email.com",
                telefono="12345",
            )

    def test_telefono_con_letras_lanza_datos_invalidos(self):
        """Teléfono con letras lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Cliente(
                nombre="Juan Pérez",
                documento="ABC12345",
                correo="test@email.com",
                telefono="abc-defg",
            )

    def test_encapsulacion_nombre_no_se_puede_asignar_invalido(self):
        """No se puede asignar un nombre inválido vía property setter."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="test@email.com",
            telefono="3001234567",
        )
        nombre_original = cliente.nombre
        with self.assertRaises(DatosInvalidosError):
            cliente.nombre = "123"
        # El valor original se preserva
        self.assertEqual(cliente.nombre, nombre_original)

    def test_encapsulacion_documento_no_se_puede_asignar_invalido(self):
        """No se puede asignar un documento inválido vía property setter."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="test@email.com",
            telefono="3001234567",
        )
        doc_original = cliente.documento
        with self.assertRaises(DatosInvalidosError):
            cliente.documento = "AB"
        self.assertEqual(cliente.documento, doc_original)

    def test_encapsulacion_correo_no_se_puede_asignar_invalido(self):
        """No se puede asignar un correo inválido vía property setter."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="test@email.com",
            telefono="3001234567",
        )
        correo_original = cliente.correo
        with self.assertRaises(DatosInvalidosError):
            cliente.correo = "correo-invalido"
        self.assertEqual(cliente.correo, correo_original)

    def test_encapsulacion_telefono_no_se_puede_asignar_invalido(self):
        """No se puede asignar un teléfono inválido vía property setter."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="test@email.com",
            telefono="3001234567",
        )
        tel_original = cliente.telefono
        with self.assertRaises(DatosInvalidosError):
            cliente.telefono = "abc"
        self.assertEqual(cliente.telefono, tel_original)

    def test_describir_retorna_string(self):
        """describir() retorna una cadena con los datos del cliente."""
        cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="test@email.com",
            telefono="3001234567",
        )
        descripcion = cliente.describir()
        self.assertIn("Juan Pérez", descripcion)
        self.assertIn("ABC12345", descripcion)
        self.assertIn("test@email.com", descripcion)

    def test_ids_auto_incrementales(self):
        """Los IDs de clientes son auto-incrementales."""
        c1 = Cliente(
            nombre="Cliente Uno",
            documento="AAA11111",
            correo="uno@email.com",
            telefono="3001111111",
        )
        c2 = Cliente(
            nombre="Cliente Dos",
            documento="BBB22222",
            correo="dos@email.com",
            telefono="3002222222",
        )
        self.assertEqual(c2.id, c1.id + 1)


if __name__ == "__main__":
    unittest.main()
