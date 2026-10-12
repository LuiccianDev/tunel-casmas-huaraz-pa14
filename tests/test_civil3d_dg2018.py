"""Pruebas del generador de criterios Civil 3D DG-2018 (carpeta civil3d/)."""

import importlib.util
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1] / "civil3d"
NS = "{urn:Civil3DRoadwayDesignStandards-schema}"


def _gen():
    spec = importlib.util.spec_from_file_location(
        "gen_dg2018", RAIZ / "generar_dg2018.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_radios_concuerdan_con_formula():
    gen = _gen()
    assert gen.verificar_radios(gen.cargar_datos()) == []


def test_xml_estructura_y_cuatro_tablas_de_radio():
    gen = _gen()
    raiz = gen.construir_xml(gen.cargar_datos()).getroot()
    assert len(list(raiz.iter(f"{NS}MinimumRadiusTable"))) == 4
    assert raiz.find(f"{NS}Profiles/{NS}MinimumKTables") is not None


def test_xml_generado_es_valido_y_en_el_proyecto():
    gen = _gen()
    destino = gen.generar()
    assert destino.parent == RAIZ
    ET.parse(destino)


def test_peralte_y_radios_mismo_nombre_con_transicion():
    gen = _gen()
    raiz = gen.construir_xml(gen.cargar_datos()).getroot()
    radios = {t.get("name") for t in raiz.iter(f"{NS}MinimumRadiusTable")}
    peraltes = {t.get("name"): t for t in raiz.iter(f"{NS}SuperelevationTable")}
    assert radios == set(peraltes)
    for tabla in peraltes.values():
        nombres = {t.get("name") for t in tabla.iter(f"{NS}TransitionLengthTable")}
        assert nombres == {"2 Lane", "4 Lane"}
        assert list(tabla.iter(f"{NS}TransitionLength"))


def test_curvas_verticales_k_oficial_dg2018():
    gen = _gen()
    raiz = gen.construir_xml(gen.cargar_datos()).getroot()
    tabla_k = raiz.find(f".//{NS}MinimumKTable")
    assert tabla_k is not None
    assert tabla_k.get("name") == "DG-2018 MTC Curvas Verticales (Art. 303.04)"
    psd_30 = tabla_k.find(f".//{NS}MinimumK_PSD[@speed='30']")
    assert psd_30 is not None and psd_30.get("K") == str(round(200**2 / 946.0))
