"""Pruebas básicas: fórmulas clave y ejecución completa del flujo."""

import math
from datetime import date

import pytest
from openpyxl import load_workbook

from casmas_pa14.config import PARAMETROS, cargar_parametros
from casmas_pa14.main import ejecutar
from casmas_pa14.modulos.m01_ubicacion import distancia
from casmas_pa14.modulos.m03_seccion import area_herradura
from casmas_pa14.modulos.m03_seccion import calcular as calcular_seccion
from casmas_pa14.modulos.m09_electricidad import caudal_por_persona, grupo_comercial


def test_area_herradura():
    # B = 2, H = 2 → hw = 1 → A = 2·1 + π·4/8
    assert area_herradura(2.0, 2.0) == pytest.approx(2 + math.pi / 2)


def test_area_herradura_invalida():
    with pytest.raises(ValueError):
        area_herradura(6.0, 2.0)


def test_seccion_proyecto():
    # Plano CAD: 13.30 × 9.58 m, gálibo 11.80 × 5.50 inscrito en la bóveda
    p = cargar_parametros(PARAMETROS)
    r = calcular_seccion(p, {"ubicacion": {"longitud_m": 1000.0}})
    assert r["hastial_m"] == pytest.approx(2.93)
    assert r["area_m2"] == pytest.approx(13.30 * 2.93 + math.pi * 13.30**2 / 8)
    assert r["ancho_galibo_m"] == pytest.approx(11.80)
    assert r["holgura_galibo_m"] == pytest.approx(0.0, abs=0.01)
    assert all(f[4] == "Sí" for f in r["verificacion"])


def test_distancia():
    assert distancia({"este": 0, "norte": 0}, {"este": 3, "norte": 4}) == 5


def test_caudal_por_altitud():
    assert caudal_por_persona(1000) == 3
    assert caudal_por_persona(3500) == 5
    assert caudal_por_persona(4100) == 6


def test_grupo_comercial():
    assert grupo_comercial(480) == 500
    assert grupo_comercial(500) == 500


def test_parametros_cargan():
    p = cargar_parametros(PARAMETROS)
    assert isinstance(p["proyecto"]["fecha_inicio"], date)


def test_flujo_completo(tmp_path):
    ctx, archivos = ejecutar(PARAMETROS, tmp_path, tmp_path / "memoria")
    excels = sorted(a.name for a in archivos if a.suffix == ".xlsx")
    assert excels == [
        "01_Ubicacion.xlsx",
        "02_Geologia.xlsx",
        "03_Seccion.xlsx",
        "04_Personal.xlsx",
        "05_Campamento.xlsx",
        "06_Maquinaria.xlsx",
        "07_Polvorin.xlsx",
        "08_Agua.xlsx",
        "09_Electricidad.xlsx",
        "10_Cronograma.xlsx",
        "11_Portales.xlsx",
        "12_Voladura.xlsx",
    ]
    for a in archivos:
        assert a.exists() and a.stat().st_size > 0
    assert load_workbook(tmp_path / "excel" / "08_Agua.xlsx").sheetnames == [
        "Consumo",
        "PETAP",
        "PETAR",
        "Pozo",
    ]
    assert load_workbook(tmp_path / "excel" / "03_Seccion.xlsx").sheetnames == [
        "Geometria",
        "Galibo",
        "Justificacion MTC",
        "Perforacion y avance",
        "Volumenes",
    ]
    hojas_maq = load_workbook(tmp_path / "excel" / "06_Maquinaria.xlsx").sheetnames
    assert hojas_maq[0:5] == [
        "Frente",
        "Accesos",
        "Banquetas",
        "Botadero",
        "Campamento",
    ]
    assert "Resumen_Flota" in hojas_maq
    assert "Sandvik DT820" in hojas_maq
    assert "Volvo FMX 6x4" in hojas_maq
    assert "Caterpillar D8" in hojas_maq
    memoria = (tmp_path / "memoria" / "03_Seccion.md").read_text(encoding="utf-8")
    assert "Verificación normativa" in memoria
    lsp = (tmp_path / "lisp" / "PA14_dibujos.lsp").read_text(encoding="ascii")
    assert lsp.count("(") == lsp.count(")"), "paréntesis LISP desbalanceados"
    assert "defun c:PA14_TODO" in lsp
    assert "defun c:PA14_CAMP1_EDIF01_DORMITORIO" in lsp
    assert "defun c:PA14_CAMP1_DORMITORIO" in lsp
    assert ctx["cronograma"]["plazo_dias"] > ctx["seccion"]["dias_excavacion"]


def test_personal_formulas_dinamicas(tmp_path):
    ejecutar(PARAMETROS, tmp_path, tmp_path / "memoria")
    wb = load_workbook(tmp_path / "excel" / "04_Personal.xlsx", data_only=False)
    ws = wb["Resumen"]

    # Fila 6: Personal de Campamento (F6 total, G6 pct)
    assert str(ws["F6"].value).startswith("="), "F6 debe ser fórmula"
    assert str(ws["G6"].value).startswith("="), "G6 porcentaje debe ser fórmula"
    assert ws["G6"].number_format == "0.0%", "G6 debe tener formato de porcentaje"

    # Fila 9: Total Proyecto
    assert str(ws["B9"].value).startswith("="), "B9 debe ser fórmula"
    assert str(ws["F9"].value).startswith("="), "F9 debe ser fórmula"
    assert str(ws["G9"].value).startswith("="), "G9 debe ser fórmula"

    # Fila 13: Mano de Obra Directa (D13 total, E13 pct)
    assert str(ws["D13"].value).startswith("="), "D13 debe ser fórmula"
    assert str(ws["E13"].value).startswith("="), "E13 porcentaje debe ser fórmula"
    assert ws["E13"].number_format == "0.0%", "E13 debe tener formato de porcentaje"

    # Fila 36 y 40: Parámetros calculados
    assert str(ws["C36"].value).startswith("="), "C36 Obreros debe ser fórmula"
    assert str(ws["C40"].value).startswith("="), "C40 Planilla debe ser fórmula"
