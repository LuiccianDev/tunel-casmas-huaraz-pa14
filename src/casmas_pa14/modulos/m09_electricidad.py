"""09 · Electricidad: ventilación, cargas dinámicas, demanda y grupo electrógeno."""

from .electricidad.calculo import (
    GRUPOS_KVA,
    calcular,
    caudal_por_persona,
    grupo_comercial,
)
from .electricidad.hojas import libro

CLAVE = "electricidad"

__all__ = [
    "CLAVE",
    "GRUPOS_KVA",
    "caudal_por_persona",
    "grupo_comercial",
    "calcular",
    "libro",
]
