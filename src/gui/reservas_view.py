"""Vista de gestión de reservas para la GUI de Software FJ.

Todos los textos de la interfaz están en inglés.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from src.cliente import Cliente
from src.servicio import Servicio
from src.reserva import Reserva, EstadoReserva
from src.gestor import Gestor
from src.excepciones import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)
from src.logger import logger
from src.gui.widgets import (
    LabeledEntry,
    LabeledCombo,
    ScrollableList,
    StatusBar,
    show_info,
    show_error,
    show_warning,
    ask_confirm,
)


class ReservasView(ttk.Frame):
    """Vista para gestionar reservas: crear, confirmar, cancelar, procesar."""

    def __init__(
        self,
        parent: tk.Widget,
        gestor: Gestor,
    ) -> None:
        super().__init__(parent)
        self._gestor = gestor
        self._cantidad_combo: Optional[LabeledCombo] = None
        self._precio_unitario_label: Optional[ttk.Label] = None
        self._precio_total_label: Optional[ttk.Label] = None
        self._unidad_label: Optional[ttk.Label] = None
        self._crear_formulario()
        self._crear_lista()
        self._crear_botones()
        self._crear_estado()
        self._cargar_clientes_combo()
        self._cargar_servicios_combo()
        self._cargar_reservas()

    def _crear_formulario(self) -> None:
        frame = ttk.LabelFrame(self, text="Create Reservation")
        frame.pack(fill=tk.X, padx=10, pady=5)

        combo_frame = ttk.Frame(frame)
        combo_frame.pack(fill=tk.X, padx=5, pady=2)

        self._cliente_combo = LabeledCombo(combo_frame, "Client:", [])
        self._cliente_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self._servicio_combo = LabeledCombo(combo_frame, "Service:", [])
        self._servicio_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self._servicio_combo._combo.bind(
            "<<ComboboxSelected>>", self._on_servicio_cambiado
        )

        refresh_frame = ttk.Frame(frame)
        refresh_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(
            refresh_frame, text="Refresh Clients", command=self._cargar_clientes_combo
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            refresh_frame, text="Refresh Services", command=self._cargar_servicios_combo
        ).pack(side=tk.LEFT, padx=2)

        dur_frame = ttk.Frame(frame)
        dur_frame.pack(fill=tk.X, padx=5, pady=2)

        self._duracion_entry = LabeledEntry(dur_frame, "Duration:")
        self._duracion_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self._unidad_label = ttk.Label(dur_frame, text="", width=12)
        self._unidad_label.pack(side=tk.LEFT, padx=(5, 0))

        # Combo de cantidad (solo para AlquilerEquipo)
        self._cantidad_combo = LabeledCombo(dur_frame, "Quantity:", [str(i) for i in range(1, 11)])
        self._cantidad_combo.pack(side=tk.LEFT, padx=(10, 0))
        self._cantidad_combo._combo.bind("<<ComboboxSelected>>", self._calcular_precio_total)

        precio_frame = ttk.Frame(frame)
        precio_frame.pack(fill=tk.X, padx=5, pady=2)

        self._precio_unitario_label = ttk.Label(
            precio_frame, text="Unit price: --", width=50
        )
        self._precio_unitario_label.pack(side=tk.LEFT)

        self._precio_total_label = ttk.Label(
            precio_frame, text="Total: --", width=15
        )
        self._precio_total_label.pack(side=tk.LEFT, padx=(10, 0))

        self._duracion_entry._entry.bind(
            "<KeyRelease>", self._calcular_precio_total
        )

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(
            btn_frame, text="Create Reservation", command=self._crear_reserva
        ).pack(side=tk.LEFT, padx=2)

    def _crear_lista(self) -> None:
        frame = ttk.LabelFrame(self, text="Reservations")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self._lista = ScrollableList(
            frame,
            ["ID", "Client", "Service", "Duration", "Qty", "Unit Price", "Total", "Status"],
            height=8,
        )
        self._lista.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._lista.bind_select(self._on_seleccion_reserva)

    def _crear_botones(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            frame, text="Refresh", command=self._cargar_reservas
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Confirm", command=self._confirmar_reserva
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Cancel", command=self._cancelar_reserva
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            frame, text="Process", command=self._procesar_reserva
        ).pack(side=tk.LEFT, padx=2)

    def _crear_estado(self) -> None:
        self._status = StatusBar(self)
        self._status.pack(fill=tk.X, padx=10, pady=2)

    def _cargar_clientes_combo(self) -> None:
        """Recarga el combo de clientes desde el gestor."""
        clientes = self._gestor.listar_clientes()
        valores = [f"{c.id}: {c.nombre}" for c in clientes]
        self._cliente_combo._combo.config(values=valores)
        if valores:
            seleccion_actual = self._cliente_combo.get()
            if seleccion_actual in valores:
                self._cliente_combo._combo.set(seleccion_actual)
            else:
                self._cliente_combo._combo.current(0)
        else:
            self._cliente_combo._combo.set("")
        self._status.set(f"Clients loaded: {len(valores)}")

    def _cargar_servicios_combo(self) -> None:
        """Recarga el combo de servicios desde el gestor."""
        servicios = self._gestor.listar_servicios()
        valores = [f"{s.id}: {s.nombre}" for s in servicios]
        self._servicio_combo._combo.config(values=valores)
        if valores:
            seleccion_actual = self._servicio_combo.get()
            if seleccion_actual in valores:
                self._servicio_combo._combo.set(seleccion_actual)
                self._on_servicio_cambiado()
            else:
                self._servicio_combo._combo.current(0)
                self._on_servicio_cambiado()
        else:
            self._servicio_combo._combo.set("")
            self._precio_unitario_label.config(text="Unit price: --")
            self._precio_total_label.config(text="Total: --")
            self._unidad_label.config(text="")
        self._status.set(f"Services loaded: {len(valores)}")

    def _cargar_reservas(self) -> None:
        self._lista.clear()
        for reserva in self._gestor.listar_reservas():
            servicio = reserva.servicio
            tipo = servicio.__class__.__name__
            if tipo == "AlquilerEquipo":
                unidad = "days"
            else:
                unidad = "hours"
            cantidad = getattr(reserva, '_cantidad_reservada', 1)
            precio_unitario = servicio.costo_base
            total = servicio.calcular_costo(reserva.duracion, cantidad_reservada=cantidad)
            self._lista.insert(
                [
                    str(reserva.id),
                    reserva.cliente.nombre,
                    servicio.nombre,
                    f"{reserva.duracion:.2f} {unidad}",
                    str(cantidad),
                    f"{precio_unitario:.2f}",
                    f"{total:.2f}",
                    reserva.estado.value,
                ]
            )

    def _on_servicio_cambiado(self, _event=None) -> None:
        """Actualiza el precio unitario y unidad cuando se selecciona un servicio."""
        texto = self._servicio_combo.get()
        if not texto:
            self._precio_unitario_label.config(text="Unit price: --")
            self._precio_total_label.config(text="Total: --")
            self._unidad_label.config(text="")
            return

        try:
            servicio_id = int(texto.split(":")[0])
        except (ValueError, IndexError):
            return

        servicio = self._gestor.obtener_servicio(servicio_id)
        if servicio:
            tipo = servicio.__class__.__name__
            if tipo == "AlquilerEquipo":
                self._unidad_label.config(text="(days)")
                # Mostrar cantidad disponible
                max_qty = servicio.cantidad
                self._cantidad_combo._combo.config(
                    values=[str(i) for i in range(1, max_qty + 1)]
                )
                self._cantidad_combo._combo.current(0)
                self._cantidad_combo.pack_configure(after=self._unidad_label)
            else:
                self._unidad_label.config(text="(hours)")
                self._cantidad_combo._combo.config(values=["1"])
                self._cantidad_combo._combo.current(0)
            # Mostrar precio unitario real por día (incluye técnico/equipamiento si aplica)
            precio_unitario_real = servicio.calcular_costo(
                1, cantidad_reservada=1
            )
            extras = []
            if tipo == "AlquilerEquipo" and servicio.incluye_tecnico:
                extras.append("includes technician")
            if tipo == "ReservaSala" and servicio.equipamiento:
                extras.append("includes equipment")
            suffix = f" ({', '.join(extras)})" if extras else ""
            self._precio_unitario_label.config(
                text=f"Unit price: {precio_unitario_real:.2f}{suffix}"
            )
            self._calcular_precio_total()

    def _calcular_precio_total(self, _event=None) -> None:
        """Calcula y muestra el precio total basado en duración × precio unitario × cantidad."""
        texto = self._servicio_combo.get()
        if not texto:
            self._precio_total_label.config(text="Total: --")
            return

        try:
            servicio_id = int(texto.split(":")[0])
        except (ValueError, IndexError):
            return

        servicio = self._gestor.obtener_servicio(servicio_id)
        if not servicio:
            return

        duracion_str = self._duracion_entry.get()
        if not duracion_str:
            self._precio_total_label.config(text="Total: --")
            return

        try:
            duracion = float(duracion_str)
        except ValueError:
            self._precio_total_label.config(text="Total: --")
            return

        if duracion <= 0:
            self._precio_total_label.config(text="Total: --")
            return

        try:
            cantidad_str = self._cantidad_combo.get()
            cantidad = int(cantidad_str) if cantidad_str else 1
        except (ValueError, TypeError):
            cantidad = 1

        try:
            total = servicio.calcular_costo(duracion, cantidad_reservada=cantidad)
            self._precio_total_label.config(text=f"Total: {total:.2f}")
        except Exception:
            self._precio_total_label.config(text="Total: --")

    def _obtener_id_de_combo(self, combo: LabeledCombo) -> Optional[int]:
        texto = combo.get()
        if not texto:
            return None
        try:
            return int(texto.split(":")[0])
        except (ValueError, IndexError):
            return None

    def _crear_reserva(self) -> None:
        cliente_id = self._obtener_id_de_combo(self._cliente_combo)
        servicio_id = self._obtener_id_de_combo(self._servicio_combo)
        duracion_str = self._duracion_entry.get()

        if cliente_id is None:
            show_warning(self, "Validation Error", "Please select a client.")
            return
        if servicio_id is None:
            show_warning(self, "Validation Error", "Please select a service.")
            return
        if not duracion_str:
            show_warning(self, "Validation Error", "Duration is required.")
            return

        try:
            duracion = float(duracion_str)
        except ValueError:
            show_error(self, "Validation Error", "Duration must be a number.")
            return

        if duracion <= 0:
            show_error(self, "Validation Error", "Duration must be greater than 0.")
            return

        # Obtener cantidad seleccionada
        try:
            cantidad = int(self._cantidad_combo.get())
        except (ValueError, TypeError):
            cantidad = 1

        servicio = self._gestor.obtener_servicio(servicio_id)
        if servicio and servicio.__class__.__name__ == "AlquilerEquipo":
            if cantidad > servicio.cantidad:
                show_error(
                    self, "Validation Error",
                    f"Only {servicio.cantidad} unit(s) available."
                )
                return

        try:
            reserva = self._gestor.crear_reserva(
                cliente_id=cliente_id,
                servicio_id=servicio_id,
                duracion=duracion,
            )
            # Almacenar la cantidad reservada como atributo para mostrarla después
            reserva._cantidad_reservada = cantidad
            total = servicio.calcular_costo(duracion, cantidad_reservada=cantidad)
            show_info(
                self, "Success",
                f"Reservation created: ID {reserva.id}\nTotal cost: {total:.2f}",
            )
            self._duracion_entry.set("")
            self._precio_total_label.config(text="Total: --")
            self._cargar_reservas()
            self._status.set(f"Reservation created: ID {reserva.id}")
        except (
            DatosInvalidosError,
            ServicioNoDisponibleError,
        ) as error:
            logger.error("Error creating reservation: %s", error)
            show_error(self, "Reservation Error", str(error))

    def _obtener_reserva_seleccionada(self) -> Optional[int]:
        values = self._lista.get_selection()
        if not values:
            show_warning(
                self, "Selection Required", "Please select a reservation."
            )
            return None
        try:
            return int(values[0])
        except (ValueError, IndexError):
            return None

    def _confirmar_reserva(self) -> None:
        reserva_id = self._obtener_reserva_seleccionada()
        if reserva_id is None:
            return
        try:
            self._gestor.confirmar_reserva(reserva_id)
            show_info(self, "Success", f"Reservation {reserva_id} confirmed.")
            self._cargar_reservas()
            self._status.set(f"Reservation {reserva_id} confirmed.")
        except (
            DatosInvalidosError,
            OperacionNoPermitidaError,
            ServicioNoDisponibleError,
        ) as error:
            logger.error("Error confirming reservation: %s", error)
            show_error(self, "Confirm Error", str(error))

    def _cancelar_reserva(self) -> None:
        reserva_id = self._obtener_reserva_seleccionada()
        if reserva_id is None:
            return
        if not ask_confirm(
            self, "Confirm Cancel", f"Cancel reservation {reserva_id}?"
        ):
            return
        try:
            self._gestor.cancelar_reserva(reserva_id)
            show_info(self, "Success", f"Reservation {reserva_id} cancelled.")
            self._cargar_reservas()
            self._status.set(f"Reservation {reserva_id} cancelled.")
        except (
            DatosInvalidosError,
            OperacionNoPermitidaError,
        ) as error:
            logger.error("Error cancelling reservation: %s", error)
            show_error(self, "Cancel Error", str(error))

    def _procesar_reserva(self) -> None:
        reserva_id = self._obtener_reserva_seleccionada()
        if reserva_id is None:
            return
        try:
            costo = self._gestor.procesar_reserva(reserva_id)
            show_info(
                self, "Success",
                f"Reservation {reserva_id} processed. Cost: {costo:.2f}",
            )
            self._cargar_reservas()
            self._status.set(f"Reservation {reserva_id} processed. Cost: {costo:.2f}")
        except (
            DatosInvalidosError,
            OperacionNoPermitidaError,
        ) as error:
            logger.error("Error processing reservation: %s", error)
            show_error(self, "Process Error", str(error))

    def _on_seleccion_reserva(self) -> None:
        pass
