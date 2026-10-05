"""Estructuras de salida comunes a todos los módulos (Libro → Hojas → Tablas)."""

import math
from dataclasses import dataclass, field
from datetime import date
from typing import Any

COLUMNAS_PARAMETRO = ["Descripción", "Símbolo", "Valor", "Unidad", "Fórmula / Fuente"]


@dataclass
class OpcionLista:
    """Representa una celda que debe tener una lista desplegable (Data Validation)."""

    valor_inicial: str
    id_rango_ref: str  # ID del rango de la tabla de referencia

    def __str__(self) -> str:
        return self.valor_inicial


@dataclass
class Tabla:
    columnas: list[str]
    filas: list[list[Any]]
    titulo: str = ""
    id_rango: str = ""


@dataclass
class Gantt:
    inicio: date
    actividades: list[tuple[str, date, date]]  # (nombre, inicio, fin inclusive)


@dataclass
class Hoja:
    nombre: str  # nombre de la pestaña (máx. 31 caracteres)
    titulo: str
    tablas: list[Tabla] = field(default_factory=list)
    gantt: Gantt | None = None


@dataclass
class Libro:
    archivo: str  # p. ej. "03_Seccion.xlsx"
    hojas: list[Hoja]


@dataclass
class Memoria:
    """Documento Markdown generado: secciones con párrafos (str) y Tablas."""

    archivo: str  # p. ej. "03_Seccion.md"
    titulo: str
    secciones: list[tuple[str, list[str | Tabla]]]


def tabla_parametros(filas: list[tuple], titulo: str = "") -> Tabla:
    """Tabla estándar: Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente."""
    return Tabla(COLUMNAS_PARAMETRO, [list(f) for f in filas], titulo)


def redondear_arriba(valor: float, paso: float) -> float:
    """Redondea hacia arriba al múltiplo de `paso` (p. ej. 0.5 m)."""
    return math.ceil(round(valor / paso, 9)) * paso
