"""Pruebas unitarias para la clase Reserva del proyecto Software FJ.

Cobertura:
- confirmar, cancelar, procesar
- Transiciones de estado válidas e inválidas
- Duración inválida
- Servicio no disponible
- Encadenamiento de excepciones
"""

import unittest
from src.cliente import Cliente
from src.servicios_concretos import ReservaSala
from src.reserva import Reserva, EstadoReserva
from src.excepciones import (
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    DatosInvalidosError,
)


class TestReserva(unittest.TestCase):
    """Pruebas para la clase Reserva."""

    def setUp(self):
        """Configura datos de prueba para cada test."""
        self.cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="juan@email.com",
            telefono="3001234567",
        )
        self.servicio = ReservaSala(
            tipo_sala="estándar", capacidad=10, equipamiento=False
        )
        self.reserva = Reserva(
            cliente=self.cliente,
            servicio=self.servicio,
            duracion=2.0,
        )

    def test_crear_reserva_valida(self):
        """Reserva con datos válidos se crea en estado PENDIENTE."""
        self.assertEqual(self.reserva.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(self.reserva.cliente, self.cliente)
        self.assertEqual(self.reserva.servicio, self.servicio)
        self.assertEqual(self.reserva.duracion, 2.0)

    def test_crear_reserva_duracion_cero(self):
        """Reserva con duración 0 lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Reserva(cliente=self.cliente, servicio=self.servicio, duracion=0)

    def test_crear_reserva_duracion_negativa(self):
        """Reserva con duración negativa lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Reserva(cliente=self.cliente, servicio=self.servicio, duracion=-1)

    def test_crear_reserva_cliente_invalido(self):
        """Reserva con cliente no válido lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Reserva(cliente="no es cliente", servicio=self.servicio, duracion=2)

    def test_crear_reserva_servicio_invalido(self):
        """Reserva con servicio no válido lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            Reserva(cliente=self.cliente, servicio="no es servicio", duracion=2)

    def test_confirmar_reserva_pasaje_paso_a_confirmada(self):
        """Confirmar reserva pendiente cambia estado a CONFIRMADA."""
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)

    def test_confirmar_reserva_ya_confirmada(self):
        """Confirmar reserva ya confirmada lanza OperacionNoPermitidaError."""
        self.reserva.confirmar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

    def test_confirmar_reserva_cancelada(self):
        """Confirmar reserva cancelada lanza OperacionNoPermitidaError."""
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

    def test_confirmar_reserva_procesada(self):
        """Confirmar reserva procesada lanza OperacionNoPermitidaError."""
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

    def test_cancelar_reserva_pasaje_a_cancelada(self):
        """Cancelar reserva pendiente cambia estado a CANCELADA."""
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_reserva_confirmada(self):
        """Cancelar reserva confirmada cambia estado a CANCELADA."""
        self.reserva.confirmar()
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_cancelar_reserva_ya_cancelada(self):
        """Cancelar reserva ya cancelada lanza OperacionNoPermitidaError."""
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    def test_cancelar_reserva_procesada(self):
        """Cancelar reserva procesada lanza OperacionNoPermitidaError."""
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    def test_procesar_reserva_desde_confirmada(self):
        """Procesar reserva confirmada cambia estado a PROCESADA."""
        self.reserva.confirmar()
        self.reserva.procesar()
        self.assertEqual(self.reserva.estado, EstadoReserva.PROCESADA)

    def test_procesar_reserva_desde_pendiente(self):
        """Procesar reserva pendiente lanza OperacionNoPermitidaError."""
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()

    def test_procesar_reserva_desde_cancelada(self):
        """Procesar reserva cancelada lanza OperacionNoPermitidaError."""
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()

    def test_procesar_reserva_desde_procesada(self):
        """Procesar reserva ya procesada lanza OperacionNoPermitidaError."""
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()

    def test_servicio_no_disponible_al_confirmar(self):
        """Confirmar reserva con servicio no disponible lanza ServicioNoDisponibleError."""
        servicio_no_disp = ReservaSala(
            tipo_sala="estándar", capacidad=10, equipamiento=False, disponible=False
        )
        reserva_no_disp = Reserva(
            cliente=self.cliente, servicio=servicio_no_disp, duracion=1.0
        )
        with self.assertRaises(ServicioNoDisponibleError):
            reserva_no_disp.confirmar()

    def test_describir_retorna_string(self):
        """describir() retorna cadena con datos de la reserva."""
        desc = self.reserva.describir()
        self.assertIn("Juan Pérez", desc)
        self.assertIn("Reserva de Sala", desc)
        self.assertIn("PENDIENTE", desc)

    def test_estado_es_enum(self):
        """EstadoReserva es un Enum con los valores esperados."""
        self.assertEqual(EstadoReserva.PENDIENTE.value, "PENDIENTE")
        self.assertEqual(EstadoReserva.CONFIRMADA.value, "CONFIRMADA")
        self.assertEqual(EstadoReserva.CANCELADA.value, "CANCELADA")
        self.assertEqual(EstadoReserva.PROCESADA.value, "PROCESADA")


if __name__ == "__main__":
    unittest.main()
