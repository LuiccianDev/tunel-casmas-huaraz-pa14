"""14 · Afrontonamiento: Diseño de Afrontonamiento y Sellado de Portal del Túnel.

Fachada del módulo 14 que delega cálculo geomecánico, hojas Excel y memoria al subpaquete `afrontonamiento/`.
"""

from __future__ import annotations

from typing import Any

from ..modelo import Libro, Memoria
from .afrontonamiento import (
    calcular_afrontonamiento_portal,
    construir_libro_afrontonamiento,
    construir_memoria_afrontonamiento,
)

CLAVE = "afrontonamiento"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula el dimensionamiento del afrontonamiento y sellado del portal del túnel."""
    return calcular_afrontonamiento_portal(p, ctx)


def libro(r: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 14_Afrontonamiento.xlsx con las 6 hojas dinámicas del sellado del portal."""
    return construir_libro_afrontonamiento(r, p)


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 14_Afrontonamiento.md del afrontonamiento y sellado del portal."""
    return construir_memoria_afrontonamiento(r, p)
