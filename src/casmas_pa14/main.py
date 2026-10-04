"""Punto de entrada: `uv run pa14` → genera todos los Excel y el archivo .lsp."""

import argparse
import sys
from pathlib import Path

from .config import MEMORIAS, PARAMETROS, SALIDAS, cargar_parametros
from .excel import escribir_libro
from .lisp import generar_lisp
from .memoria import escribir_memoria
from .modulos import (
    m01_ubicacion,
    m03_seccion,
    m04_personal,
    m05_campamento,
    m06_maquinaria,
    m07_polvorin,
    m08_agua,
    m09_electricidad,
    m10_cronograma,
)

# Orden = dependencias (cada módulo usa resultados de los anteriores).
# m02_geologia se agregará aquí cuando estén los datos.
MODULOS = [
    m01_ubicacion,
    m03_seccion,
    m04_personal,
    m05_campamento,
    m06_maquinaria,
    m07_polvorin,
    m08_agua,
    m09_electricidad,
    m10_cronograma,
]


def ejecutar(
    parametros: Path = PARAMETROS, salida: Path = SALIDAS, memorias: Path = MEMORIAS
) -> tuple[dict, list[Path]]:
    """Corre todos los módulos; devuelve el contexto de resultados y los archivos creados."""
    p = cargar_parametros(parametros)
    proyecto = p["proyecto"]["nombre"]
    ctx: dict = {}
    archivos: list[Path] = []
    for modulo in MODULOS:
        ctx[modulo.CLAVE] = modulo.calcular(p, ctx)
        archivos.append(
            escribir_libro(
                modulo.libro(ctx[modulo.CLAVE], p), salida / "excel", proyecto
            )
        )
        if hasattr(modulo, "memoria"):
            archivos.append(
                escribir_memoria(
                    modulo.memoria(ctx[modulo.CLAVE], p), memorias, proyecto
                )
            )
    archivos.append(generar_lisp(ctx, salida / "lisp", proyecto))
    return ctx, archivos


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cálculos del túnel Casmas Huaraz PA14"
    )
    parser.add_argument(
        "--parametros", type=Path, default=PARAMETROS, help="archivo TOML de entrada"
    )
    parser.add_argument(
        "--salida", type=Path, default=SALIDAS, help="carpeta de salida"
    )
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # consolas Windows

    ctx, archivos = ejecutar(args.parametros, args.salida)
    for ruta in archivos:
        print(f"  ✔ {ruta}")
    sec, ele, cro = ctx["seccion"], ctx["electricidad"], ctx["cronograma"]
    print(
        f"\nL = {sec['longitud_m']:.1f} m · A = {sec['area_m2']:.2f} m² · "
        f"Población = {ctx['personal']['total']} · Grupo = {ele['grupo_kva']} kVA · "
        f"Plazo = {cro['plazo_dias']} días"
    )
    incumple = [r for r in ctx["ubicacion"]["restricciones"] if not r["cumple"]]
    for r in incumple:
        print(
            f"  ⚠ Distancia {r['desde']}–{r['hasta']} = {r['distancia_m']:.0f} m < {r['minimo_m']:.0f} m"
        )


if __name__ == "__main__":
    main()
