"""Widgets reutilizables para la interfaz gráfica de Software FJ.

Todos los textos de la interfaz están en inglés, según lo requerido por
el AGENTS.md.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional


def show_info(parent: tk.Widget, title: str, message: str) -> None:
    """Muestra un mensaje informativo."""
    messagebox.showinfo(title, message, parent=parent)


def show_error(parent: tk.Widget, title: str, message: str) -> None:
    """Muestra un mensaje de error."""
    messagebox.showerror(title, message, parent=parent)


def show_warning(parent: tk.Widget, title: str, message: str) -> None:
    """Muestra un mensaje de advertencia."""
    messagebox.showwarning(title, message, parent=parent)


def ask_confirm(parent: tk.Widget, title: str, message: str) -> bool:
    """Pide confirmación al usuario. Retorna True si acepta."""
    return messagebox.askyesno(title, message, parent=parent)


class LabeledEntry(ttk.Frame):
    """Campo de entrada con etiqueta."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        show: Optional[str] = None,
        width: int = 30,
    ) -> None:
        super().__init__(parent)
        self._label = ttk.Label(self, text=label)
        self._label.pack(side=tk.LEFT, padx=(0, 5))
        self._entry = ttk.Entry(self, width=width, show=show)
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self) -> str:
        """Retorna el texto del campo."""
        return self._entry.get().strip()

    def set(self, value: str) -> None:
        """Establece el texto del campo."""
        self._entry.delete(0, tk.END)
        self._entry.insert(0, value)

    def focus(self) -> None:
        """Da foco al campo."""
        self._entry.focus_set()


class LabeledCombo(ttk.Frame):
    """Combo box con etiqueta."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        values: list,
        width: int = 27,
    ) -> None:
        super().__init__(parent)
        self._label = ttk.Label(self, text=label)
        self._label.pack(side=tk.LEFT, padx=(0, 5))
        self._combo = ttk.Combobox(
            self, values=values, width=width, state="readonly"
        )
        self._combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        if values:
            self._combo.current(0)

    def get(self) -> str:
        """Retorna el valor seleccionado."""
        return self._combo.get()

    def set(self, value: str) -> None:
        """Establece el valor seleccionado."""
        self._combo.set(value)


class LabeledCheck(ttk.Frame):
    """Casilla de verificación con etiqueta."""

    def __init__(self, parent: tk.Widget, label: str) -> None:
        super().__init__(parent)
        self._var = tk.BooleanVar(value=False)
        self._check = ttk.Checkbutton(self, text=label, variable=self._var)
        self._check.pack(side=tk.LEFT)

    def get(self) -> bool:
        """Retorna el estado de la casilla."""
        return self._var.get()

    def set(self, value: bool) -> None:
        """Establece el estado de la casilla."""
        self._var.set(value)


class ScrollableList(ttk.Frame):
    """Lista con barra de desplazamiento."""

    def __init__(self, parent: tk.Widget, columns: list, height: int = 10) -> None:
        super().__init__(parent)
        self._tree = ttk.Treeview(
            self, columns=columns, show="headings", height=height
        )
        for col in columns:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=100)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def clear(self) -> None:
        """Limpia todos los elementos de la lista."""
        for item in self._tree.get_children():
            self._tree.delete(item)

    def insert(self, values: list) -> None:
        """Inserta una fila en la lista."""
        self._tree.insert("", tk.END, values=values)

    def get_selection(self) -> Optional[tuple]:
        """Retorna los valores de la fila seleccionada o None."""
        selection = self._tree.selection()
        if not selection:
            return None
        return self._tree.item(selection[0], "values")

    def bind_select(self, callback: Callable) -> None:
        """Vincula un callback al evento de selección."""
        self._tree.bind("<<TreeviewSelect>>", lambda _: callback())


class StatusBar(ttk.Frame):
    """Barra de estado en la parte inferior de la ventana."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self._label = ttk.Label(self, text="Ready", relief=tk.SUNKEN)
        self._label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def set(self, message: str) -> None:
        """Establece el mensaje de la barra de estado."""
        self._label.config(text=message)
