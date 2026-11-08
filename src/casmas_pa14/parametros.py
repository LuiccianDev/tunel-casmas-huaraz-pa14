"""Motor de validación de esquema e invariantes físicos de parámetros (TOML)."""

from __future__ import annotations

from typing import Any

SECCIONES_REQUERIDAS: tuple[str, ...] = (
    "proyecto",
    "ubicacion",
    "seccion",
    "perforacion",
    "regimen",
    "personal",
    "campamento",
    "maquinaria",
    "polvorin",
    "agua",
    "electricidad",
    "cronograma",
    "portales",
    "voladura",
    "voladura_banquetas",
    "geologia",
    "sostenimiento",
    "afrontonamiento",
)


def validar_esquema_parametros(p: dict[str, Any]) -> None:
    """Verifica que todas las secciones raíz obligatorias existan en el diccionario de parámetros."""
    faltantes = [sec for sec in SECCIONES_REQUERIDAS if sec not in p]
    if faltantes:
        raise ValueError(
            f"Esquema paramétrico incompleto; faltan secciones obligatorias: {faltantes}"
        )


def validar_invariantes_fisicos(p: dict[str, Any]) -> None:
    """Valida invariantes físicos, geométricos y operativos del proyecto."""
    sec = p.get("seccion", {})
    ancho = float(sec.get("ancho_m", 0.0))
    altura = float(sec.get("altura_m", 0.0))
    esponj = float(sec.get("factor_esponjamiento", 0.0))
    densidad = float(sec.get("densidad_roca_t_m3", 0.0))

    if ancho <= 0:
        raise ValueError(
            f"Invariante violado: seccion.ancho_m debe ser > 0 (recibido: {ancho})"
        )
    if altura <= ancho / 2.0:
        raise ValueError(
            f"Invariante violado: seccion.altura_m ({altura}) debe superar el radio de bóveda B/2 ({ancho / 2.0})"
        )
    if esponj <= 1.0:
        raise ValueError(
            f"Invariante violado: seccion.factor_esponjamiento ({esponj}) debe ser > 1.0"
        )
    if densidad <= 0:
        raise ValueError(
            f"Invariante violado: seccion.densidad_roca_t_m3 ({densidad}) debe ser > 0"
        )

    proy = p.get("proyecto", {})
    if float(proy.get("altitud_msnm", 0.0)) <= 0:
        raise ValueError("Invariante violado: proyecto.altitud_msnm debe ser > 0")

    ubic = p.get("ubicacion", {})
    if not ubic.get("puntos"):
        raise ValueError("Invariante violado: ubicacion.puntos no puede estar vacío")

    geo = p.get("geologia", {})
    if not geo.get("tramos"):
        raise ValueError("Invariante violado: geologia.tramos no puede estar vacío")


def validar_parametros(p: dict[str, Any]) -> dict[str, Any]:
    """Ejecuta la validación integral de esquema e invariantes físicos y retorna el diccionario."""
    validar_esquema_parametros(p)
    validar_invariantes_fisicos(p)
    return p
