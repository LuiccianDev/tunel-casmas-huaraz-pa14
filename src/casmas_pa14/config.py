"""Rutas del proyecto y carga validada de parámetros."""

import tomllib
from pathlib import Path
from typing import Any

from .parametros import validar_parametros

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "datos" / "parametros.toml"
SALIDAS = RAIZ / "salidas"
MEMORIAS = RAIZ / "docs" / "memoria"  # memorias Markdown generadas (sí se versionan)


def cargar_parametros(ruta: Path = PARAMETROS, validar: bool = True) -> dict[str, Any]:
    """Lee y valida el archivo TOML de parámetros (única fuente de datos de entrada)."""
    with ruta.open("rb") as archivo:
        datos = tomllib.load(archivo)
    if validar:
        validar_parametros(datos)
    return datos
