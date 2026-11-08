"""04 · Personal: relación de cargos, organigrama y población del campamento."""

from .personal.calculo import calcular
from .personal.hojas import (
    _tabla_cruce_campamentos,
    _tabla_macro_areas,
    _tabla_mano_obra,
    libro,
)
from .personal.memoria_doc import memoria

CLAVE = "personal"

__all__ = [
    "CLAVE",
    "calcular",
    "libro",
    "memoria",
    "_tabla_macro_areas",
    "_tabla_cruce_campamentos",
    "_tabla_mano_obra",
]
