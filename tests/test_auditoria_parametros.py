"""Arnés de Detección Automática de Parámetros Huérfanos en parametros.toml."""

import re
import tomllib
from pathlib import Path


def obtener_claves_toml(d: dict, prefijo: str = "") -> list[tuple[str, str]]:
    """Extrae tuplas (ruta_completa, clave_hoja) de un diccionario cargado de TOML."""
    claves = []
    for k, v in d.items():
        ruta = f"{prefijo}.{k}" if prefijo else k
        if isinstance(v, dict):
            claves.extend(obtener_claves_toml(v, ruta))
        else:
            claves.append((ruta, k))
    return claves


def obtener_parametros_huerfanos(
    toml_path: Path = Path("datos/parametros.toml"),
    src_dir: Path = Path("src/casmas_pa14"),
) -> list[str]:
    """Detecta claves en parametros.toml que no son referenciadas en ningún archivo de src/."""
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    py_files = list(src_dir.rglob("*.py"))
    py_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore") for p in py_files
    )

    huerfanas = []
    for full_key, leaf_key in obtener_claves_toml(data):
        patron = re.compile(r"['\"]" + re.escape(leaf_key) + r"['\"]")
        if not patron.search(py_text):
            huerfanas.append(full_key)

    return huerfanas


def test_cero_parametros_huerfanos_en_toml():
    """Valida que todas las claves en parametros.toml sean consumidas por src/casmas_pa14."""
    huerfanas = obtener_parametros_huerfanos()
    assert len(huerfanas) == 0, (
        f"Se detectaron {len(huerfanas)} claves huérfanas en parametros.toml: "
        f"{huerfanas[:10]}..."
    )
