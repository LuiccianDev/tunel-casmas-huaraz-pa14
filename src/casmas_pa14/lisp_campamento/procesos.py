"""Fachada de plantas civiles, sanitarias, energéticas, viales y de seguridad."""

from .procesos_energia import (
    planta_casa_fuerza,
    planta_estacion_combustible,
    planta_polvorin_sucamec,
)
from .procesos_sanitarios import (
    planta_edif_14,
    planta_edif_15,
    planta_edif_16,
    planta_edif_17,
    planta_edif_18,
    planta_edif_19,
    planta_edif_32,
)
from .procesos_viales import (
    planta_caseta_polvorin,
    planta_edif_24,
    planta_edif_25,
    planta_edif_26,
    planta_edif_27,
    planta_edif_36,
)

__all__ = [
    "planta_casa_fuerza",
    "planta_caseta_polvorin",
    "planta_edif_14",
    "planta_edif_15",
    "planta_edif_16",
    "planta_edif_17",
    "planta_edif_18",
    "planta_edif_19",
    "planta_edif_24",
    "planta_edif_25",
    "planta_edif_26",
    "planta_edif_27",
    "planta_edif_32",
    "planta_edif_36",
    "planta_estacion_combustible",
    "planta_polvorin_sucamec",
]
