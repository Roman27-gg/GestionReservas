"""Vista de gestión de servicios para la GUI de Software FJ.

Todos los textos de la interfaz están en inglés.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from src.servicios_concretos import (
    crear_servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.logger import logger
from src.gui.widgets import (
    LabeledEntry,
    LabeledCombo,
    LabeledCheck,
    ScrollableList,
    StatusBar,
    show_info,
    show_error,
    show_warning,
    ask_confirm,
)


class ServiciosView(ttk.Frame):
    """Vista para gestionar servicios: crear, listar y eliminar."""

    TIPOS_SERVICIO = [
        "ReservaSala",
        "AlquilerEquipo",
        "AsesoriaEspecializada",
    ]

    def __init__(
        self,
        parent: tk.Widget,
        gestor,
        on_servicio_selected: Optional[Callable] = None,
    ) -> None:
        super().__init__(parent)
        self._gestor = gestor
        self._on_servicio_selected = on_servicio_selected
        self._campos_extra_frame: Optional[ttk.Frame] = None
        self._crear_formulario()
        self._crear_lista()
        self._crear_botones()
        self._crear_estado()
        self._cargar_servicios()

    def _crear_formulario(self) -> None:
        frame = ttk.LabelFrame(self, text="Create Service")
        frame.pack(fill=tk.X, padx=10, pady=5)

        self._tipo_combo = LabeledCombo(
            frame, "Service type:", self.TIPOS_SERVICIO
        )
        self._tipo_combo.pack(fill=tk.X, padx=5, pady=2)
        self._tipo_combo._combo.bind("<<ComboboxSelected>>", self._on_tipo_cambiado)

        self._nombre_entry = LabeledEntry(frame, "Name:")
        self._nombre_entry.pack(fill=tk.X, padx=5, pady=2)

        self._precio_entry = LabeledEntry(frame, "Base price per unit:")
        self._precio_entry.pack(fill=tk.X, padx=5, pady=2)

        self._campos_extra_frame = ttk.Frame(frame)
        self._campos_extra_frame.pack(fill=tk.X, padx=5, pady=2)

        self._disponible_check = LabeledCheck(frame, "Available")
        self._disponible_check.set(True)
        self._disponible_check.pack(fill=tk.X, padx=5, pady=2)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(
            btn_frame, text="Create", command=self._crear_servicio
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame, text="Clear", command=self._limpiar_formulario
        ).pack(side=tk.LEFT, padx=2)

        self._on_tipo_cambiado()

    def _on_tipo_cambiado(self, _event=None) -> None:
        for widget in self._campos_extra_frame.winfo_children():
            widget.destroy()

        tipo = self._tipo_combo.get()

        if tipo == "ReservaSala":
            self._sala_tipo_entry = LabeledEntry(
                self._campos_extra_frame, "Room type (e.g., standard, VIP):"
            )
            self._sala_tipo_entry.pack(fill=tk.X, padx=5, pady=2)
            self._capacidad_entry = LabeledEntry(
                self._campos_extra_frame, "Capacity:"
            )
            self._capacidad_entry.pack(fill=tk.X, padx=5, pady=2)
            self._equipamiento_check = LabeledCheck(
                self._campos_extra_frame, "Includes equipment"
            )
            self._equipamiento_check.pack(fill=tk.X, padx=5, pady=2)

        elif tipo == "AlquilerEquipo":
            self._equipo_tipo_entry = LabeledEntry(
                self._campos_extra_frame, "Equipment type:"
            )
            self._equipo_tipo_entry.pack(fill=tk.X, padx=5, pady=2)
            self._cantidad_entry = LabeledEntry(
                self._campos_extra_frame, "Quantity:"
            )
            self._cantidad_entry.pack(fill=tk.X, padx=5, pady=2)
            self._tecnico_check = LabeledCheck(
                self._campos_extra_frame, "Includes technician"
            )
            self._tecnico_check.pack(fill=tk.X, padx=5, pady=2)

        elif tipo == "AsesoriaEspecializada":
            self._especialidad_entry = LabeledEntry(
                self._campos_extra_frame, "Specialty:"
            )
            self._especialidad_entry.pack(fill=tk.X, padx=5, pady=2)
            self._nivel_entry = LabeledEntry(
                self._campos_extra_frame, "Level (e.g., JUNIOR, SENIOR, EXPERTO):"
            )
            self._nivel_entry.pack(fill=tk.X, padx=5, pady=2)
            self._modalidad_entry = LabeledEntry(
                self._campos_extra_frame, "Modality (e.g., virtual, presencial):"
            )
            self._modalidad_entry.pack(fill=tk.X, padx=5, pady=2)

    def _crear_lista(self) -> None:
        frame = ttk.LabelFrame(self, text="Services")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self._lista = ScrollableList(
            frame, ["ID", "Name", "Type", "Cost Base", "Qty Avail", "Available"], height=8
        )
        self._lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._lista.bind_select(self._on_seleccion_servicio)

    def _crear_botones(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            frame, text="Refresh", command=self._cargar_servicios
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Toggle Availability", command=self._toggle_disponible
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Delete Selected", command=self._eliminar_servicio
        ).pack(side=tk.LEFT, padx=2)

    def _crear_estado(self) -> None:
        self._status = StatusBar(self)
        self._status.pack(fill=tk.X, padx=10, pady=2)

    def _crear_servicio(self) -> None:
        tipo = self._tipo_combo.get()
        nombre = self._nombre_entry.get()
        precio_str = self._precio_entry.get()
        disponible = self._disponible_check.get()

        if not nombre:
            show_warning(self, "Validation Error", "Name is required.")
            return
        if not precio_str:
            show_warning(self, "Validation Error", "Base price is required.")
            return

        try:
            precio_base = float(precio_str)
        except ValueError:
            show_error(self, "Validation Error", "Base price must be a number.")
            return

        kwargs: dict = {"costo_base": precio_base, "disponible": disponible, "nombre": nombre}

        try:
            if tipo == "ReservaSala":
                kwargs["tipo_sala"] = self._sala_tipo_entry.get()
                kwargs["capacidad"] = int(self._capacidad_entry.get())
                kwargs["equipamiento"] = self._equipamiento_check.get()
            elif tipo == "AlquilerEquipo":
                kwargs["tipo_equipo"] = self._equipo_tipo_entry.get()
                kwargs["cantidad"] = int(self._cantidad_entry.get())
                kwargs["incluye_tecnico"] = self._tecnico_check.get()
            elif tipo == "AsesoriaEspecializada":
                kwargs["especialidad"] = self._especialidad_entry.get()
                kwargs["nivel_experto"] = self._nivel_entry.get()
                kwargs["modalidad"] = self._modalidad_entry.get()

            servicio = crear_servicio(tipo, **kwargs)
            self._gestor.registrar_servicio(servicio)
            show_info(self, "Success", f"Service created: {servicio.nombre}")
            self._limpiar_formulario()
            self._cargar_servicios()
            self._status.set(f"Service created: {servicio.nombre}")
        except (
            DatosInvalidosError,
            ParametrosFaltantesError,
            ValueError,
        ) as error:
            logger.error("Error creating service: %s", error)
            show_error(self, "Creation Error", str(error))

    def _limpiar_formulario(self) -> None:
        self._nombre_entry.set("")
        self._precio_entry.set("")
        self._disponible_check.set(True)

    def _cargar_servicios(self) -> None:
        self._lista.clear()
        for servicio in self._gestor.listar_servicios():
            tipo = servicio.__class__.__name__
            # Determinar unidad y cantidad según el tipo de servicio
            if tipo == "ReservaSala":
                unidad = "/hour"
                cantidad = servicio.capacidad
            elif tipo == "AlquilerEquipo":
                unidad = "/day"
                cantidad = servicio.cantidad
            else:
                unidad = "/hour"
                cantidad = 1
            self._lista.insert(
                [
                    str(servicio.id),
                    servicio.nombre,
                    tipo,
                    f"{servicio.costo_base:.2f}{unidad}",
                    str(cantidad),
                    "Yes" if servicio.disponible else "No",
                ]
            )

    def _on_seleccion_servicio(self) -> None:
        values = self._lista.get_selection()
        if values and self._on_servicio_selected:
            servicio_id = int(values[0])
            servicio = self._gestor.obtener_servicio(servicio_id)
            if servicio:
                self._on_servicio_selected(servicio)

    def _toggle_disponible(self) -> None:
        values = self._lista.get_selection()
        if not values:
            show_warning(
                self, "Selection Required", "Please select a service to toggle availability."
            )
            return
        servicio_id = int(values[0])
        servicio = self._gestor.obtener_servicio(servicio_id)
        if servicio:
            servicio.disponible = not servicio.disponible
            estado = "available" if servicio.disponible else "unavailable"
            show_info(
                self, "Availability Changed",
                f"Service '{servicio.nombre}' is now {estado}."
            )
            self._cargar_servicios()
            self._status.set(f"Service {servicio.nombre}: {estado}")

    def _eliminar_servicio(self) -> None:
        values = self._lista.get_selection()
        if not values:
            show_warning(
                self, "Selection Required", "Please select a service to delete."
            )
            return
        servicio_id = int(values[0])
        nombre = values[1]
        if not ask_confirm(
            self, "Confirm Delete", f"Delete service '{nombre}' (ID: {servicio_id})?"
        ):
            return
        try:
            servicios = self._gestor.listar_servicios()
            self._gestor._servicios = [
                s for s in servicios if s.id != servicio_id
            ]
            self._cargar_servicios()
            show_info(self, "Deleted", f"Service '{nombre}' deleted.")
            self._status.set(f"Service deleted: {nombre}")
        except Exception as error:
            logger.error("Error deleting service: %s", error)
            show_error(self, "Delete Error", str(error))
