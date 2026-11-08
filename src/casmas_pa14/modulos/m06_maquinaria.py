"""06 · Maquinaria: frente del túnel, botadero, campamento y fichas técnicas."""

from .maquinaria.calculo import calcular
from .maquinaria.hojas import (
    _tabla_equipos,
    _tabla_ficha_individual,
    _tabla_resumen_fichas,
    libro,
)
from .maquinaria.memoria_doc import memoria

CLAVE = "maquinaria"

__all__ = [
    "CLAVE",
    "calcular",
    "libro",
    "memoria",
    "_tabla_equipos",
    "_tabla_ficha_individual",
    "_tabla_resumen_fichas",
]
