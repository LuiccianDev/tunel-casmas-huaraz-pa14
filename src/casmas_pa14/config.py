"""Rutas del proyecto y carga de parámetros."""

import tomllib
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "datos" / "parametros.toml"
SALIDAS = RAIZ / "salidas"
MEMORIAS = RAIZ / "docs" / "memoria"  # memorias Markdown generadas (sí se versionan)


def cargar_parametros(ruta: Path = PARAMETROS) -> dict[str, Any]:
    """Lee el archivo TOML de parámetros (única fuente de datos de entrada)."""
    with ruta.open("rb") as archivo:
        return tomllib.load(archivo)
