"""Ventana principal de la GUI de Software FJ.

Todos los textos de la interfaz están en inglés.
"""

import tkinter as tk
from tkinter import ttk
from src.gestor import Gestor
from src.gui.clientes_view import ClientesView
from src.gui.servicios_view import ServiciosView
from src.gui.reservas_view import ReservasView
from src.logger import logger


class MainWindow(tk.Tk):
    """Ventana principal de la aplicación con pestañas para clientes,
    servicios y reservas."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Software FJ - Client, Service & Reservation Management")
        self.geometry("900x700")

        self._gestor = Gestor()

        self._crear_menu()
        self._crear_pestañas()
        self._crear_estado()

    def _crear_menu(self) -> None:
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=archivo_menu)

        ayuda_menu = tk.Menu(menubar, tearoff=0)
        ayuda_menu.add_command(label="About", command=self._mostrar_acerca)
        menubar.add_cascade(label="Help", menu=ayuda_menu)

    def _crear_pestañas(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._clientes_view = ClientesView(notebook, self._gestor)
        notebook.add(self._clientes_view, text="Clients")

        self._servicios_view = ServiciosView(notebook, self._gestor)
        notebook.add(self._servicios_view, text="Services")

        self._reservas_view = ReservasView(notebook, self._gestor)
        notebook.add(self._reservas_view, text="Reservations")

    def _crear_estado(self) -> None:
        self._status = ttk.Label(
            self, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self._status.pack(side=tk.BOTTOM, fill=tk.X)

    def _mostrar_acerca(self) -> None:
        from tkinter import messagebox
        messagebox.showinfo(
            "About",
            "Software FJ\n"
            "Client, Service & Reservation Management System\n"
            "Python 3.10+ with tkinter\n"
            "All GUI text in English",
        )

    def ejecutar(self) -> None:
        """Inicia el bucle principal de la GUI."""
        logger.info("GUI launched")
        self.mainloop()


def main() -> None:
    """Punto de entrada para la interfaz gráfica."""
    app = MainWindow()
    app.ejecutar()


if __name__ == "__main__":
    main()
