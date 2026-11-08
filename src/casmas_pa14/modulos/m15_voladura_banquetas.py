"""15 · Voladura de Banquetas y Portales en Superficie (Epiroc PowerROC T25 — Modelo de C.J. Konya).

Fachada del módulo 15 que delega el modelo matemático de bancos Konya, hojas Excel y memoria al subpaquete `banquetas/`.
"""

from __future__ import annotations

from typing import Any

from ..modelo import Libro, Memoria
from .banquetas import (
    calcular_voladura_banquetas,
    construir_libro_banquetas,
    construir_memoria_banquetas,
)

CLAVE = "voladura_banquetas"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula el modelo de bancos de C.J. Konya con Epiroc PowerROC T25 para las banquetas."""
    return calcular_voladura_banquetas(p, ctx)


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 15_Voladura_Banquetas.xlsx exclusivo para Banquetas con PowerROC T25."""
    return construir_libro_banquetas(resultados, p)


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 15_Voladura_Banquetas.md exclusiva para las banquetas en superficie."""
    return construir_memoria_banquetas(r, p)
