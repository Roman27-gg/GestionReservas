"""Pruebas unitarias para la clase Gestor del proyecto Software FJ.

Cobertura:
- Registro y obtención de clientes, servicios y reservas
- Creación de reservas con validaciones
- Confirmar, cancelar y procesar reservas a través del gestor
- Validaciones de integridad (cliente no existe, servicio no disponible)
"""

import unittest
from src.cliente import Cliente
from src.servicios_concretos import ReservaSala, AlquilerEquipo
from src.reserva import EstadoReserva
from src.gestor import Gestor
from src.excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)


class TestGestor(unittest.TestCase):
    """Pruebas para la clase Gestor."""

    def setUp(self):
        """Configura un gestor limpio para cada test."""
        self.gestor = Gestor()
        self.cliente = Cliente(
            nombre="Juan Pérez",
            documento="ABC12345",
            correo="juan@email.com",
            telefono="3001234567",
        )
        self.servicio = ReservaSala(
            tipo_sala="estándar", capacidad=10, equipamiento=False
        )

    def test_registrar_y_obtener_cliente(self):
        """Registrar cliente y obtenerlo por ID funciona."""
        self.gestor.registrar_cliente(self.cliente)
        obtenido = self.gestor.obtener_cliente(self.cliente.id)
        self.assertEqual(obtenido, self.cliente)

    def test_obtener_cliente_no_existente_retorna_none(self):
        """Obtener cliente inexistente retorna None."""
        resultado = self.gestor.obtener_cliente(999)
        self.assertIsNone(resultado)

    def test_listar_clientes(self):
        """Listar clientes retorna todos registrados."""
        self.gestor.registrar_cliente(self.cliente)
        cliente2 = Cliente(
            nombre="María García",
            documento="XYZ98765",
            correo="maria@email.com",
            telefono="3019876543",
        )
        self.gestor.registrar_cliente(cliente2)
        self.assertEqual(len(self.gestor.listar_clientes()), 2)

    def test_registrar_y_obtener_servicio(self):
        """Registrar servicio y obtenerlo por ID funciona."""
        self.gestor.registrar_servicio(self.servicio)
        obtenido = self.gestor.obtener_servicio(self.servicio.id)
        self.assertEqual(obtenido, self.servicio)

    def test_listar_servicios(self):
        """Listar servicios retorna todos registrados."""
        self.gestor.registrar_servicio(self.servicio)
        servicio2 = AlquilerEquipo(
            tipo_equipo="básico", cantidad=1, incluye_tecnico=False
        )
        self.gestor.registrar_servicio(servicio2)
        self.assertEqual(len(self.gestor.listar_servicios()), 2)

    def test_crear_reserva_exitoso(self):
        """Crear reserva con cliente y servicio existentes funciona."""
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.servicio)
        reserva = self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=2.0,
        )
        self.assertIsInstance(reserva.id, int)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)

    def test_crear_reserva_cliente_no_existe(self):
        """Crear reserva con cliente inexistente lanza DatosInvalidosError."""
        self.gestor.registrar_servicio(self.servicio)
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear_reserva(
                cliente_id=999,
                servicio_id=self.servicio.id,
                duracion=2.0,
            )

    def test_crear_reserva_servicio_no_existe(self):
        """Crear reserva con servicio inexistente lanza DatosInvalidosError."""
        self.gestor.registrar_cliente(self.cliente)
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear_reserva(
                cliente_id=self.cliente.id,
                servicio_id=999,
                duracion=2.0,
            )

    def test_crear_reserva_servicio_no_disponible(self):
        """Crear reserva con servicio no disponible lanza ServicioNoDisponibleError."""
        self.gestor.registrar_cliente(self.cliente)
        servicio_no_disp = ReservaSala(
            tipo_sala="estándar", capacidad=10, equipamiento=False, disponible=False
        )
        self.gestor.registrar_servicio(servicio_no_disp)
        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva(
                cliente_id=self.cliente.id,
                servicio_id=servicio_no_disp.id,
                duracion=1.0,
            )

    def test_confirmar_reserva_a_tres(self):
        """Confirmar reserva a través del gestor."""
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.servicio)
        reserva = self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=1.0,
        )
        self.gestor.confirmar_reserva(reserva.id)
        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)

    def test_confirmar_reserva_no_existente(self):
        """Confirmar reserva inexistente lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            self.gestor.confirmar_reserva(999)

    def test_cancelar_reserva_a_traves_del_gestor(self):
        """Cancelar reserva a través del gestor."""
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.servicio)
        reserva = self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=1.0,
        )
        self.gestor.cancelar_reserva(reserva.id)
        self.assertEqual(reserva.estado, EstadoReserva.CANCELADA)

    def test_procesar_reserva_a_traves_del_gestor(self):
        """Procesar reserva a través del gestor retorna costo."""
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.servicio)
        reserva = self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=2.0,
        )
        self.gestor.confirmar_reserva(reserva.id)
        costo = self.gestor.procesar_reserva(reserva.id)
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)
        self.assertEqual(costo, 100.0)  # 50.0 * 2

    def test_listar_reservas(self):
        """Listar reservas retorna todas creadas."""
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.servicio)
        self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=1.0,
        )
        self.gestor.crear_reserva(
            cliente_id=self.cliente.id,
            servicio_id=self.servicio.id,
            duracion=2.0,
        )
        self.assertEqual(len(self.gestor.listar_reservas()), 2)

    def test_obtener_reserva_no_existente_retorna_none(self):
        """Obtener reserva inexistente retorna None."""
        resultado = self.gestor.obtener_reserva(999)
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
