"""Arnés de Detección Automática de Parámetros Huérfanos y Validación Paramétrica."""

import copy
import re
import tomllib
from pathlib import Path

import pytest

from casmas_pa14.config import PARAMETROS, cargar_parametros
from casmas_pa14.parametros import (
    SECCIONES_REQUERIDAS,
    validar_esquema_parametros,
    validar_invariantes_fisicos,
    validar_parametros,
)


def obtener_claves_toml(d: dict, prefijo: str = "") -> list[tuple[str, str]]:
    """Extrae tuplas (ruta_completa, clave_hoja) de un diccionario cargado de TOML."""
    claves = []
    for k, v in d.items():
        ruta = f"{prefijo}.{k}" if prefijo else k
        if isinstance(v, dict):
            claves.extend(obtener_claves_toml(v, ruta))
        elif isinstance(v, list):
            for i, elem in enumerate(v):
                if isinstance(elem, dict):
                    claves.extend(obtener_claves_toml(elem, f"{ruta}[{i}]"))
                else:
                    claves.append((ruta, k))
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


def test_validacion_esquema_parametros_oficial():
    """El archivo parametros.toml oficial debe pasar todas las validaciones de esquema e invariantes."""
    p = cargar_parametros(PARAMETROS)
    for seccion in SECCIONES_REQUERIDAS:
        assert seccion in p, f"Falta sección requerida: {seccion}"
    assert validar_parametros(p) is p


def test_validar_esquema_detecta_seccion_faltante():
    """Debe lanzar ValueError si falta una sección raíz obligatoria."""
    p = copy.deepcopy(cargar_parametros(PARAMETROS))
    del p["voladura"]
    with pytest.raises(ValueError, match="voladura"):
        validar_esquema_parametros(p)


def test_validar_invariantes_fisicos_detecta_valores_invalidos():
    """Debe lanzar ValueError ante geometrías o factores físicamente imposibles."""
    p_ancho = copy.deepcopy(cargar_parametros(PARAMETROS))
    p_ancho["seccion"]["ancho_m"] = -5.0
    with pytest.raises(ValueError, match="ancho_m"):
        validar_invariantes_fisicos(p_ancho)

    p_esponj = copy.deepcopy(cargar_parametros(PARAMETROS))
    p_esponj["seccion"]["factor_esponjamiento"] = 0.85
    with pytest.raises(ValueError, match="factor_esponjamiento"):
        validar_invariantes_fisicos(p_esponj)

