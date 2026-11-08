"""Pruebas unitarias para los scripts de cálculo NATM y excavación por secciones."""

import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.pruebas.prueba_convergencia_natm import (  # noqa: E402
    generar_libro_convergencia,
)
from scripts.pruebas.prueba_voladura_natm_secciones import (  # noqa: E402
    generar_libro_natm,
)


def test_generar_libro_natm_seccion_dividida(tmp_path: Path):
    """Verifica la generación del libro de voladura y excavación por secciones NATM."""
    ruta_salida = tmp_path / "Prueba_NATM_Seccion_Dividida.xlsx"
    ruta_gen = generar_libro_natm(ruta_salida)

    assert ruta_gen.exists(), f"El archivo {ruta_gen} no se generó."
    wb = load_workbook(ruta_gen, data_only=False)

    hojas_esperadas = [
        "01_Comparativa_Metodos",
        "02_Seccion_Plena_Base",
        "03_Calota_NATM",
        "04_Destroza_NATM",
        "05_Sostenimiento_NATM",
    ]
    for nombre in hojas_esperadas:
        assert nombre in wb.sheetnames, (
            f"Falta la pestaña '{nombre}' en el libro generado."
        )

    # Verificar que el área geométrica de calota + destroza sea consistente
    ws_comp = wb["01_Comparativa_Metodos"]
    # Fila 6 es Área de excavación
    area_plena = ws_comp["C6"].value
    area_calota = ws_comp["D6"].value
    area_destroza = ws_comp["E6"].value

    assert area_plena == 108.43
    assert area_calota == 69.46
    assert area_destroza == 38.97
    assert round(area_calota + area_destroza, 2) == 108.43


def test_generar_libro_convergencia_natm(tmp_path: Path):
    """Verifica la generación del libro de curvas de convergencia-confinamiento (CCM)."""
    ruta_salida = tmp_path / "Prueba_Curvas_Convergencia_NATM.xlsx"
    ruta_gen = generar_libro_convergencia(ruta_salida)

    assert ruta_gen.exists(), f"El archivo {ruta_gen} no se generó."
    wb = load_workbook(ruta_gen, data_only=False)

    hojas_esperadas = [
        "01_Convergencia_Equilibrio",
        "02_Curvas_GRC_SCC",
    ]
    for nombre in hojas_esperadas:
        assert nombre in wb.sheetnames, (
            f"Falta la pestaña '{nombre}' en el libro generado."
        )
