"""Fachada de generación del archivo AutoLISP (.lsp) con los planos básicos del proyecto.

Delega la geometría detallada al subpaquete `lisp_cad/` respetando el principio SRP.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

from .lisp_cad import (
    _LIBRERIA,
    ARCHIVO,
    CAPAS,
    DESFASE_DETALLES,
    SEPARACION,
    Dibujo,
    _arco,
    _circulo,
    _cota,
    _cota_angular,
    _hatch_cunetas,
    _linea,
    _n,
    _origenes,
    _rect,
    _taladros_cune,
    _taladros_malla,
    _texto,
    _texto_cen,
    _txt,
    dibujo_cortes_accesos,
    dibujo_geologia,
    dibujo_malla,
    dibujo_seccion,
    dibujo_ubicacion,
)


def generar_lisp(ctx: dict, carpeta: Path, proyecto: str) -> Path:
    """Compila todos los planos básicos del proyecto hacia `PA14_dibujos.lsp`."""
    ubicacion = dibujo_ubicacion(ctx["ubicacion"])
    detalles = [
        dibujo_seccion(ctx["seccion"]),
        dibujo_malla(ctx["seccion"], ctx.get("voladura")),
        dibujo_geologia(ctx["geologia"]),
        dibujo_cortes_accesos(ctx.get("portales", {})),
    ]
    dibujos = [ubicacion, *detalles]
    origenes = [(0.0, 0.0), *_origenes(ctx["ubicacion"], detalles)]
    lineas = [
        f";;; {_txt(proyecto)[1:-1]} - generado con `uv run pa14`. NO EDITAR A MANO.",
        ";;; APPLOAD -> cargar este archivo -> comandos: "
        + ", ".join(d.comando for d in dibujos)
        + ", PA14_TODO",
        ";;; Unidades: metros. Coordenadas UTM WGS84 zona 18L (X = Este, Y = Norte).",
        _LIBRERIA,
        "(defun pa14:capas ()",
        *[f'  (pa14:capa "{n}" {c})' for n, c in CAPAS.items()],
        ")",
    ]
    todo = ["\n(defun c:PA14_TODO ()", "  (pa14:inicio)"]
    for d, (ox, oy) in zip(dibujos, origenes, strict=True):
        nombre = d.comando.lower().replace("pa14_", "pa14:d-")
        lineas += [f"\n;;; {_txt(d.descripcion)[1:-1]}", f"(defun {nombre} ()"]
        lineas += [f"  {c}" for c in d.cuerpo]
        lineas += [
            ")",
            f"(defun c:{d.comando} () (pa14:inicio)"
            f" (pa14:origen {_n(ox)} {_n(oy)}) ({nombre}) (pa14:fin))",
        ]
        todo += [f"  (pa14:origen {_n(ox)} {_n(oy)})", f"  ({nombre})"]
    todo += [
        "  (pa14:fin))",
        '(princ "\\nPA14 cargado. Escriba PA14_TODO o PA14_GEOLOGIA.")',
        "(princ)",
    ]
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / ARCHIVO
    contenido = "\n".join(lineas + todo) + "\n"
    contenido_ascii = (
        unicodedata.normalize("NFKD", contenido)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    ruta.write_text(contenido_ascii, encoding="ascii")
    return ruta


__all__ = [
    "ARCHIVO",
    "CAPAS",
    "DESFASE_DETALLES",
    "Dibujo",
    "SEPARACION",
    "_LIBRERIA",
    "_arco",
    "_circulo",
    "_cota",
    "_cota_angular",
    "_hatch_cunetas",
    "_linea",
    "_n",
    "_origenes",
    "_rect",
    "_taladros_cune",
    "_taladros_malla",
    "_texto",
    "_texto_cen",
    "_txt",
    "dibujo_cortes_accesos",
    "dibujo_geologia",
    "dibujo_malla",
    "dibujo_seccion",
    "dibujo_ubicacion",
    "generar_lisp",
]
