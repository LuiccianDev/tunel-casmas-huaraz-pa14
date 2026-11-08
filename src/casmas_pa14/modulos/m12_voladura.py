"""12 · Voladura Subterránea del Túnel (Jumbo 3 brazos Sandvik DT1131 / XE3C + Catálogo de Explosivos).

Fachada del módulo 12 que delega cálculo matemático, hojas Excel y memoria al subpaquete `voladura/`.
"""

from __future__ import annotations

from typing import Any

from ..modelo import Libro, Memoria
from .voladura import (
    calcular_voladura_tunel,
    construir_libro_voladura,
    construir_memoria_voladura,
)

CLAVE = "voladura"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula la perforación y voladura subterránea del túnel con Jumbo 3 brazos Sandvik DT1131."""
    return calcular_voladura_tunel(p, ctx)


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 12_Voladura.xlsx exclusivo para la Voladura Subterránea del Túnel."""
    return construir_libro_voladura(resultados, p)


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 12_Voladura.md exclusiva para la voladura subterránea del túnel."""
    return construir_memoria_voladura(r, p)
