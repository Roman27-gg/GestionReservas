"""Vista de gestión de clientes para la GUI de Software FJ.

Todos los textos de la interfaz están en inglés.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from src.cliente import Cliente, crear_cliente
from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.logger import logger
from src.gui.widgets import (
    LabeledEntry,
    ScrollableList,
    StatusBar,
    show_info,
    show_error,
    show_warning,
    ask_confirm,
)


class ClientesView(ttk.Frame):
    """Vista para gestionar clientes: crear, listar y eliminar."""

    def __init__(
        self,
        parent: tk.Widget,
        gestor,
        on_cliente_selected: Optional[callable] = None,
    ) -> None:
        super().__init__(parent)
        self._gestor = gestor
        self._on_cliente_selected = on_cliente_selected
        self._crear_formulario()
        self._crear_lista()
        self._crear_botones()
        self._crear_estado()
        self._cargar_clientes()

    def _crear_formulario(self) -> None:
        frame = ttk.LabelFrame(self, text="Register Client")
        frame.pack(fill=tk.X, padx=10, pady=5)

        self._nombre_entry = LabeledEntry(frame, "Full name:")
        self._nombre_entry.pack(fill=tk.X, padx=5, pady=2)

        self._documento_entry = LabeledEntry(frame, "Document (6-12 alphanumeric):")
        self._documento_entry.pack(fill=tk.X, padx=5, pady=2)

        self._correo_entry = LabeledEntry(frame, "Email:")
        self._correo_entry.pack(fill=tk.X, padx=5, pady=2)

        self._telefono_entry = LabeledEntry(frame, "Phone:")
        self._telefono_entry.pack(fill=tk.X, padx=5, pady=2)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(
            btn_frame, text="Register", command=self._registrar_cliente
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame, text="Clear", command=self._limpiar_formulario
        ).pack(side=tk.LEFT, padx=2)

    def _crear_lista(self) -> None:
        frame = ttk.LabelFrame(self, text="Clients")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self._lista = ScrollableList(
            frame, ["ID", "Name", "Document", "Email", "Phone"], height=8
        )
        self._lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._lista.bind_select(self._on_seleccion_cliente)

    def _crear_botones(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            frame, text="Refresh", command=self._cargar_clientes
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Delete Selected", command=self._eliminar_cliente
        ).pack(side=tk.LEFT, padx=2)

    def _crear_estado(self) -> None:
        self._status = StatusBar(self)
        self._status.pack(fill=tk.X, padx=10, pady=2)

    def _registrar_cliente(self) -> None:
        nombre = self._nombre_entry.get()
        documento = self._documento_entry.get()
        correo = self._correo_entry.get()
        telefono = self._telefono_entry.get()

        if not all([nombre, documento, correo, telefono]):
            show_warning(self, "Validation Error", "All fields are required.")
            return

        try:
            cliente = crear_cliente(
                nombre=nombre,
                documento=documento,
                correo=correo,
                telefono=telefono,
            )
            self._gestor.registrar_cliente(cliente)
            show_info(self, "Success", f"Client registered: {cliente.nombre}")
            self._limpiar_formulario()
            self._cargar_clientes()
            self._status.set(f"Client registered: {cliente.nombre}")
        except (DatosInvalidosError, ParametrosFaltantesError) as error:
            logger.error("Error registering client: %s", error)
            show_error(self, "Registration Error", str(error))

    def _limpiar_formulario(self) -> None:
        self._nombre_entry.set("")
        self._documento_entry.set("")
        self._correo_entry.set("")
        self._telefono_entry.set("")
        self._nombre_entry.focus()

    def _cargar_clientes(self) -> None:
        self._lista.clear()
        for cliente in self._gestor.listar_clientes():
            self._lista.insert(
                [
                    str(cliente.id),
                    cliente.nombre,
                    cliente.documento,
                    cliente.correo,
                    cliente.telefono,
                ]
            )

    def _on_seleccion_cliente(self) -> None:
        values = self._lista.get_selection()
        if values and self._on_cliente_selected:
            cliente_id = int(values[0])
            cliente = self._gestor.obtener_cliente(cliente_id)
            if cliente:
                self._on_cliente_selected(cliente)

    def _eliminar_cliente(self) -> None:
        values = self._lista.get_selection()
        if not values:
            show_warning(self, "Selection Required", "Please select a client to delete.")
            return
        cliente_id = int(values[0])
        nombre = values[1]
        if not ask_confirm(
            self, "Confirm Delete", f"Delete client '{nombre}' (ID: {cliente_id})?"
        ):
            return
        try:
            clientes = self._gestor.listar_clientes()
            self._gestor._clientes = [
                c for c in clientes if c.id != cliente_id
            ]
            self._cargar_clientes()
            show_info(self, "Deleted", f"Client '{nombre}' deleted.")
            self._status.set(f"Client deleted: {nombre}")
        except Exception as error:
            logger.error("Error deleting client: %s", error)
            show_error(self, "Delete Error", str(error))
