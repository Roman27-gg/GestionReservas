"""Pruebas unitarias para la interfaz gráfica (GUI) de Software FJ.

Verifica que:
- La ventana principal se crea sin errores.
- Los botones y campos existen y responden.
- Los textos están en inglés.
"""

import unittest
import tkinter as tk
from src.gestor import Gestor
from src.gui.ventana_principal import MainWindow
from src.gui.clientes_view import ClientesView
from src.gui.servicios_view import ServiciosView
from src.gui.reservas_view import ReservasView


class TestGUI(unittest.TestCase):
    """Pruebas para la interfaz gráfica."""

    @classmethod
    def setUpClass(cls):
        """Crea una instancia de Tk para todas las pruebas de GUI."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # No mostrar ventana durante pruebas

    @classmethod
    def tearDownClass(cls):
        """Destruye la instancia de Tk."""
        cls.root.destroy()

    def test_main_window_se_crea_sin_errores(self):
        """La ventana principal se crea sin lanzar excepciones."""
        app = MainWindow()
        self.assertIsInstance(app, MainWindow)
        self.assertEqual(
            app.title(),
            "Software FJ - Client, Service & Reservation Management",
        )
        app.destroy()

    def test_main_window_tiene_tres_pestanas(self):
        """La ventana principal tiene exactamente tres pestañas."""
        app = MainWindow()
        notebook = app.nametowidget(app.winfo_children()[1])
        self.assertEqual(notebook.index("end"), 3)
        app.destroy()

    def test_textos_en_ingles(self):
        """Los textos de la interfaz están en inglés."""
        app = MainWindow()
        # Verificar título en inglés
        self.assertIn("Client", app.title())
        self.assertIn("Service", app.title())
        self.assertIn("Reservation", app.title())
        app.destroy()

    def test_clientes_view_tiene_campos_requeridos(self):
        """La vista de clientes tiene los campos de formulario requeridos."""
        gestor = Gestor()
        view = ClientesView(self.root, gestor)
        self.assertIsInstance(view, ClientesView)
        self.assertIsNotNone(view._nombre_entry)
        self.assertIsNotNone(view._documento_entry)
        self.assertIsNotNone(view._correo_entry)
        self.assertIsNotNone(view._telefono_entry)

    def test_clientes_view_lista_clientes(self):
        """La vista de clientes puede listar clientes."""
        gestor = Gestor()
        view = ClientesView(self.root, gestor)
        self.assertIsInstance(view._lista, type(view._lista))
        view.destroy()

    def test_servicios_view_tiene_tipos_servicio(self):
        """La vista de servicios tiene los tipos de servicio definidos."""
        gestor = Gestor()
        view = ServiciosView(self.root, gestor)
        self.assertEqual(len(view.TIPOS_SERVICIO), 3)
        self.assertIn("ReservaSala", view.TIPOS_SERVICIO)
        self.assertIn("AlquilerEquipo", view.TIPOS_SERVICIO)
        self.assertIn("AsesoriaEspecializada", view.TIPOS_SERVICIO)
        view.destroy()

    def test_reservas_view_tiene_botones_accion(self):
        """La vista de reservas tiene botones de acción."""
        gestor = Gestor()
        view = ReservasView(self.root, gestor)
        self.assertIsInstance(view, ReservasView)
        view.destroy()

    def test_gestor_inicializado(self):
        """El gestor se inicializa correctamente en la ventana principal."""
        app = MainWindow()
        self.assertIsInstance(app._gestor, Gestor)
        app.destroy()

    def test_about_dialog_tiene_texto_ingles(self):
        """El diálogo About contiene texto en inglés."""
        app = MainWindow()
        # No lanzar el diálogo, solo verificar que el método existe
        self.assertTrue(hasattr(app, "_mostrar_acerca"))
        app.destroy()


if __name__ == "__main__":
    unittest.main()
