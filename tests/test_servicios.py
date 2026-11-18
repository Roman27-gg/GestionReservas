"""Pruebas unitarias para los servicios del proyecto Software FJ.

Cobertura:
- Cada servicio concreto calcula el costo correcto
- Variantes sobrecargadas (con impuesto, con descuento, ambos)
- Validación de parámetros incorrectos
- Polimorfismo (lista de servicios tratada como Servicio)
"""

import unittest
from src.servicios_concretos import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    crear_servicio,
)
from src.servicio import Servicio, IVA, DESCUENTO_MAX
from src.excepciones import (
    DatosInvalidosError,
    ParametrosFaltantesError,
    CalculoInconsistenteError,
)


class TestServiciosConcretos(unittest.TestCase):
    """Pruebas para los tres servicios concretos."""

    # --- ReservaSala ---

    def test_reserva_sala_calculo_base(self):
        """ReservaSala calcula costo base correctamente."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        costo = sala.calcular_costo(duracion=3)
        self.assertEqual(costo, 50.0 * 3)  # 150.0

    def test_reserva_sala_con_equipamiento(self):
        """ReservaSala con equipamiento añade costo extra."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=True)
        costo = sala.calcular_costo(duracion=2)
        self.assertEqual(costo, (50.0 + 30.0) * 2)  # 160.0

    def test_reserva_sala_con_impuesto(self):
        """ReservaSala con impuesto aplica IVA (19%)."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        costo = sala.calcular_costo(duracion=1, con_impuesto=True)
        self.assertAlmostEqual(costo, 50.0 * (1 + IVA))

    def test_reserva_sala_con_descuento(self):
        """ReservaSala con descuento aplica descuento."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        costo = sala.calcular_costo(duracion=1, descuento=0.1)
        self.assertAlmostEqual(costo, 50.0 * (1 - 0.1))

    def test_reserva_sala_con_impuesto_y_descuento(self):
        """ReservaSala con impuesto y descuento aplica ambos."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        costo = sala.calcular_costo(duracion=1, con_impuesto=True, descuento=0.1)
        esperado = 50.0 * (1 - 0.1) * (1 + IVA)
        self.assertAlmostEqual(costo, esperado)

    def test_reserva_sala_tipo_vip(self):
        """ReservaSala tipo VIP tiene costo base diferente."""
        sala = ReservaSala(tipo_sala="VIP", capacidad=5, equipamiento=False)
        costo = sala.calcular_costo(duracion=1)
        self.assertEqual(costo, 120.0)

    def test_reserva_sala_duracion_cero_lanza_error(self):
        """ReservaSala con duración 0 lanza DatosInvalidosError."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        with self.assertRaises(DatosInvalidosError):
            sala.calcular_costo(duracion=0)

    def test_reserva_sala_duracion_negativa_lanza_error(self):
        """ReservaSala con duración negativa lanza DatosInvalidosError."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        with self.assertRaises(DatosInvalidosError):
            sala.calcular_costo(duracion=-1)

    def test_reserva_sala_capacidad_invalida(self):
        """ReservaSala con capacidad <= 0 lanza error en validar_parametros."""
        with self.assertRaises(DatosInvalidosError):
            sala = ReservaSala(tipo_sala="estándar", capacidad=0, equipamiento=False)
            sala.validar_parametros()

    def test_reserva_sala_describir(self):
        """ReservaSala.describir() retorna string con datos clave."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=True)
        desc = sala.describir()
        self.assertIn("estándar", desc)
        self.assertIn("10", desc)

    # --- AlquilerEquipo ---

    def test_alquiler_equipo_calculo_base(self):
        """AlquilerEquipo calcula costo base correctamente."""
        equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=2, incluye_tecnico=False)
        costo = equipo.calcular_costo(duracion=3)
        self.assertEqual(costo, 20.0 * 3)  # 60.0

    def test_alquiler_equipo_con_tecnico(self):
        """AlquilerEquipo con técnico añade costo extra."""
        equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=True)
        costo = equipo.calcular_costo(duracion=2)
        self.assertEqual(costo, (20.0 * 2) + (40.0 * 2))  # 120.0

    def test_alquiler_equipo_con_impuesto(self):
        """AlquilerEquipo con impuesto aplica IVA."""
        equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=False)
        costo = equipo.calcular_costo(duracion=1, con_impuesto=True)
        self.assertAlmostEqual(costo, 20.0 * (1 + IVA))

    def test_alquiler_equipo_con_descuento(self):
        """AlquilerEquipo con descuento aplica descuento."""
        equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=False)
        costo = equipo.calcular_costo(duracion=1, descuento=0.2)
        self.assertAlmostEqual(costo, 20.0 * (1 - 0.2))

    def test_alquiler_equipo_tipo_profesional(self):
        """AlquilerEquipo tipo profesional tiene costo base diferente."""
        equipo = AlquilerEquipo(tipo_equipo="profesional", cantidad=1, incluye_tecnico=False)
        costo = equipo.calcular_costo(duracion=1)
        self.assertEqual(costo, 80.0)

    def test_alquiler_equipo_cantidad_invalida(self):
        """AlquilerEquipo con cantidad <= 0 lanza error."""
        with self.assertRaises(DatosInvalidosError):
            equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=0, incluye_tecnico=False)
            equipo.validar_parametros()

    def test_alquiler_equipo_duracion_negativa(self):
        """AlquilerEquipo con duración negativa lanza error."""
        equipo = AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=False)
        with self.assertRaises(DatosInvalidosError):
            equipo.calcular_costo(duracion=-1)

    # --- AsesoriaEspecializada ---

    def test_asesoria_junior_calculo_base(self):
        """AsesoriaEspecializada junior calcula costo base."""
        asesoria = AsesoriaEspecializada(
            especialidad="Contabilidad", nivel_experto="JUNIOR", modalidad="virtual"
        )
        costo = asesoria.calcular_costo(duracion=2)
        self.assertEqual(costo, 60.0 * 2)  # 120.0

    def test_asesoria_senior_calculo_base(self):
        """AsesoriaEspecializada senior calcula costo base."""
        asesoria = AsesoriaEspecializada(
            especialidad="Legal", nivel_experto="SENIOR", modalidad="virtual"
        )
        costo = asesoria.calcular_costo(duracion=1)
        self.assertEqual(costo, 120.0)

    def test_asesoria_experto_calculo_base(self):
        """AsesoriaEspecializada experto calcula costo base."""
        asesoria = AsesoriaEspecializada(
            especialidad="Tributario", nivel_experto="EXPERTO", modalidad="virtual"
        )
        costo = asesoria.calcular_costo(duracion=1)
        self.assertEqual(costo, 200.0)

    def test_asesoria_modalidad_presencial_recargo(self):
        """Asesoría presencial aplica recargo del 10%."""
        asesoria = AsesoriaEspecializada(
            especialidad="Contabilidad", nivel_experto="JUNIOR", modalidad="presencial"
        )
        costo = asesoria.calcular_costo(duracion=1)
        self.assertAlmostEqual(costo, 60.0 * 1.10)

    def test_asesoria_con_impuesto(self):
        """Asesoría con impuesto aplica IVA."""
        asesoria = AsesoriaEspecializada(
            especialidad="Contabilidad", nivel_experto="JUNIOR", modalidad="virtual"
        )
        costo = asesoria.calcular_costo(duracion=1, con_impuesto=True)
        self.assertAlmostEqual(costo, 60.0 * (1 + IVA))

    def test_asesoria_nivel_invalido(self):
        """Asesoría con nivel inválido usa JUNIOR por defecto."""
        asesoria = AsesoriaEspecializada(
            especialidad="Contabilidad", nivel_experto="INVALIDO", modalidad="virtual"
        )
        self.assertEqual(asesoria.costo_base, 60.0)

    def test_asesoria_modalidad_invalida(self):
        """Asesoría con modalidad inválida lanza error en validar_parametros."""
        with self.assertRaises(DatosInvalidosError):
            asesoria = AsesoriaEspecializada(
                especialidad="Contabilidad", nivel_experto="JUNIOR", modalidad="invalida"
            )
            asesoria.validar_parametros()

    def test_asesoria_especialidad_vacia(self):
        """Asesoría con especialidad vacía lanza ParametrosFaltantesError."""
        with self.assertRaises(ParametrosFaltantesError):
            asesoria = AsesoriaEspecializada(
                especialidad="", nivel_experto="JUNIOR", modalidad="virtual"
            )
            asesoria.validar_parametros()

    # --- Polimorfismo ---

    def test_poliformismo_lista_de_servicios(self):
        """Lista de servicios tratados como Servicio funciona polimórficamente."""
        servicios = [
            ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False),
            AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=False),
            AsesoriaEspecializada(
                especialidad="Contabilidad", nivel_experto="JUNIOR", modalidad="virtual"
            ),
        ]
        for servicio in servicios:
            self.assertIsInstance(servicio, Servicio)
            costo = servicio.calcular_costo(duracion=1)
            self.assertGreater(costo, 0)
            desc = servicio.describir()
            self.assertIsInstance(desc, str)

    def test_poliformismo_todos_calculan_costo(self):
        """Todos los servicios concretos implementan calcular_costo."""
        servicios = [
            ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False),
            AlquilerEquipo(tipo_equipo="básico", cantidad=1, incluye_tecnico=False),
            AsesoriaEspecializada(
                especialidad="Legal", nivel_experto="SENIOR", modalidad="virtual"
            ),
        ]
        for servicio in servicios:
            self.assertTrue(hasattr(servicio, "calcular_costo"))
            self.assertTrue(hasattr(servicio, "describir"))
            self.assertTrue(hasattr(servicio, "validar_parametros"))

    # --- Factory crear_servicio ---

    def test_crear_servicio_reserva_sala(self):
        """Factory crea ReservaSala correctamente."""
        servicio = crear_servicio(
            "ReservaSala", tipo_sala="estándar", capacidad=10, equipamiento=False
        )
        self.assertIsInstance(servicio, ReservaSala)

    def test_crear_servicio_alquiler_equipo(self):
        """Factory crea AlquilerEquipo correctamente."""
        servicio = crear_servicio(
            "AlquilerEquipo", tipo_equipo="básico", cantidad=1, incluye_tecnico=False
        )
        self.assertIsInstance(servicio, AlquilerEquipo)

    def test_crear_servicio_asesoria(self):
        """Factory crea AsesoriaEspecializada correctamente."""
        servicio = crear_servicio(
            "AsesoriaEspecializada",
            especialidad="Contabilidad",
            nivel_experto="JUNIOR",
            modalidad="virtual",
        )
        self.assertIsInstance(servicio, AsesoriaEspecializada)

    def test_crear_servicio_tipo_invalido(self):
        """Factory con tipo inválido lanza DatosInvalidosError."""
        with self.assertRaises(DatosInvalidosError):
            crear_servicio("TipoInexistente")

    def test_descuento_maximo_excedido(self):
        """Descuento mayor al máximo lanza DatosInvalidosError."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        with self.assertRaises(DatosInvalidosError):
            sala.calcular_costo(duracion=1, descuento=0.5)

    def test_descuento_negativo(self):
        """Descuento negativo lanza DatosInvalidosError."""
        sala = ReservaSala(tipo_sala="estándar", capacidad=10, equipamiento=False)
        with self.assertRaises(DatosInvalidosError):
            sala.calcular_costo(duracion=1, descuento=-0.1)


if __name__ == "__main__":
    unittest.main()
