"""Catálogos técnicos, fichas de maquinaria, tablas normativas y especificaciones."""

from .maquinaria import FICHAS_TECNICAS
from .prompts_cad import generar_prompts_cad
from .rendimientos import generar_tablas_rendimiento_equipo

__all__ = [
    "FICHAS_TECNICAS",
    "generar_prompts_cad",
    "generar_tablas_rendimiento_equipo",
]
