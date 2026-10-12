"""Genera el archivo de criterios de diseño de Civil 3D según el DG-2018 (MTC Perú).

Lee `civil3d/dg2018_datos.toml` y escribe el XML en esta misma carpeta del proyecto.
No toca ninguna carpeta global de Autodesk Civil 3D.

Uso:  uv run python civil3d/generar_dg2018.py
"""

from __future__ import annotations

import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
NS = "urn:Civil3DRoadwayDesignStandards-schema"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
G = 127.0  # constante de la fórmula R = V² / (127 (p + f)), V en km/h


def cargar_datos(ruta: Path | None = None) -> dict:
    """Lee el TOML normativo."""
    with open(ruta or CARPETA / "dg2018_datos.toml", "rb") as f:
        return tomllib.load(f)


def verificar_radios(datos: dict) -> list[str]:
    """Contrasta R calculado de la tabla con R = V²/(127(p+f)). Devuelve discrepancias."""
    tol = datos["verificacion"]["tolerancia_radio_m"]
    fallos = []
    for clave, t in datos["tabla_302_02"].items():
        p = t["p_max"] / 100
        filas = zip(t["velocidades"], t["f_max"], t["radio_calculado"], strict=True)
        for v, f, r_tab in filas:
            r = v**2 / (G * (p + f))
            if abs(r - r_tab) > tol:
                fallos.append(f"{clave} V={v}: formula {r:.1f} vs tabla {r_tab}")
    return fallos


def _el(padre: ET.Element, etiqueta: str, **atr) -> ET.Element:
    return ET.SubElement(
        padre, f"{{{NS}}}{etiqueta}", {k: str(v) for k, v in atr.items()}
    )


def _tabla_radios(padre: ET.Element, nombre: str, t: dict) -> None:
    tabla = _el(padre, "MinimumRadiusTable", name=nombre)
    for v, r in zip(t["velocidades"], t["radio_redondeado"], strict=True):
        _el(tabla, "MinimumRadius", speed=v, radius=r)


def _metodo_bombeo(padre: ET.Element, nombre: str) -> None:
    """Método estándar de transición de peralte con bombeo (formulas, sin datos)."""
    m = _el(padre, "SuperelevationAttainmentMethod", name=nombre)
    estilo = _el(m, "TransitionStyleStandard")
    formulas = {
        "LCtoFS": "{t}",
        "LCtoBC": "{p}*{t}",
        "NCtoLC": "{t}*{c}/{e}",
        "LCtoRC": "{t}*{c}/{e}",
        "NStoNC": "{t}*({s}-{c})/{e}",
    }
    for tipo, formula in formulas.items():
        _el(estilo, "TransitionFormula", type=tipo, formula=formula)


def _sobreancho(padre: ET.Element, nombre: str, datos: dict) -> None:
    s = datos["sobreancho"]
    m = _el(padre, "WideningMethod", name=nombre)
    por_formula = _el(m, "WideningTypeByFormula")
    formula = (
        f"{{n}}*({{r}}-sqrt({{r}}^2-{{wl}}^2))+{s['coef_velocidad']}*{{v}}/sqrt({{r}})"
    )
    _el(por_formula, "WideningFormula", roundingFactor=s["redondeo"], formula=formula)


def _filas_peralte(t: dict, v: int, rmin: float, pp: dict) -> list[tuple[int, str]]:
    """Filas (radio, eRate) de una velocidad: NC, RC y e creciente hasta p_max."""
    p, b = t["p_max"], pp["bombeo"]
    filas = [
        (round(rmin * p / (b * pp["fraccion_nc"])), "NC"),
        (round(rmin * p / b), "RC"),
    ]
    e = b + pp["paso_e"]
    while e < p + 1e-9:
        filas.append((round(rmin * p / e), f"{e:.1f}"))
        e += pp["paso_e"]
    return filas


def nombre_tabla(datos: dict, t: dict) -> str:
    """Nombre común de radio mínimo y peralte: Civil 3D las vincula por nombre exacto."""
    return f"{datos['general']['prefijo_tablas']} eMax {t['p_max']:g}% - {t['nombre']}"


def _longitud_transicion(e: float, v: int, ancho: float, tp: dict) -> int:
    """Lt = e / ip_max * B, con ip_max = ip_base - ip_factor_v * V (en %)."""
    ip = tp["ip_base"] - tp["ip_factor_v"] * v
    return max(tp["lt_minima"], round(e / ip * ancho))


def _tablas_transicion(
    padre: ET.Element, t: dict, pp: dict, tp: dict, filas: dict[int, list]
) -> None:
    """Bloque TransitionLengthTables (2 Lane, 4 Lane) con los radios de cada velocidad."""
    bloque = _el(padre, "TransitionLengthTables")
    for nombre, factor in tp["tablas"].items():
        ancho = tp["ancho_carril"] * factor
        tabla = _el(bloque, "TransitionLengthTable", name=nombre)
        por_tabla = _el(tabla, "TransitionLengthTypeByTable")
        for v, lista in filas.items():
            vel = _el(por_tabla, "TransitionLengthDesignSpeed", speed=v)
            for radio, tasa in lista:
                e = pp["bombeo"] if tasa in ("NC", "RC") else float(tasa)
                lt = _longitud_transicion(e, v, ancho, tp)
                _el(vel, "TransitionLength", radius=radio, tLength=lt)


def _tablas_peralte(padre: ET.Element, datos: dict) -> None:
    pp, tp = datos["peralte"], datos["transicion_peralte"]
    for t in datos["tabla_302_02"].values():
        padre.append(
            ET.Comment(
                " Discretizacion (S) de Figuras 302.02-302.05; Lt oficial Art. 302.08 "
            )
        )
        por_tabla = _el(
            _el(padre, "SuperelevationTable", name=nombre_tabla(datos, t)),
            "SuperelevationTypeByTable",
        )
        filas = {}
        for v, rmin in zip(t["velocidades"], t["radio_redondeado"], strict=True):
            vel = _el(por_tabla, "SuperelevationDesignSpeed", speed=v)
            filas[v] = _filas_peralte(t, v, rmin, pp)
            for radio, tasa in filas[v]:
                _el(vel, "SuperelevationRate", radius=radio, eRate=tasa)
        _tablas_transicion(por_tabla, t, pp, tp, filas)


def _tabla_k(padre: ET.Element, datos: dict) -> None:
    k, pref = datos["curvas_verticales_k"], datos["general"]["prefijo_tablas"]
    tabla = _el(padre, "MinimumKTable", name=f"{pref} Curvas Verticales (Art. 303.04)")
    ssd, psd = _el(tabla, "StoppingSightDistance"), _el(tabla, "PassingSightDistance")
    hsd = _el(tabla, "HeadlightSightDistance")
    for v, dp, da in zip(
        k["velocidades"], k["dp_parada"], k["da_adelantamiento"], strict=True
    ):
        _el(ssd, "MinimumK_SSD", speed=v, K=round(dp**2 / k["divisor_convexa_parada"]))
        _el(psd, "MinimumK_PSD", speed=v, K=round(da**2 / k["divisor_convexa_paso"]))
        _el(
            hsd,
            "MinimumK_HSD",
            speed=v,
            K=round(dp**2 / (k["concava_a"] + k["concava_b"] * dp)),
        )


def construir_xml(datos: dict) -> ET.ElementTree:
    """Arma el árbol XML con el esquema oficial de Civil 3D."""
    ET.register_namespace("", NS)
    ET.register_namespace("xsi", XSI)
    pref = datos["general"]["prefijo_tablas"]
    raiz = ET.Element(f"{{{NS}}}Civil3DRoadwayDesignStandards", {"version": "2.0"})
    unidades = _el(raiz, "Units")
    _el(
        unidades,
        "Metric",
        linearUnit="meter",
        areaUnit="squareMeter",
        volumeUnit="cubicMeter",
        speedUnit=datos["general"]["unidad_velocidad"],
    )
    alin = _el(raiz, "Alignments")
    radios = _el(alin, "MinimumRadiusTables")
    for t in datos["tabla_302_02"].values():
        _tabla_radios(radios, nombre_tabla(datos, t), t)
    metodos = _el(alin, "SuperelevationAttainmentMethods")
    _metodo_bombeo(metodos, f"{pref} Bombeo (Crowned Roadway)")
    _tablas_peralte(_el(alin, "SuperelevationTables"), datos)
    anchos = _el(alin, "WideningMethods")
    _sobreancho(anchos, f"{pref} Sobreancho (formula)", datos)
    _tabla_k(_el(_el(raiz, "Profiles"), "MinimumKTables"), datos)
    ET.indent(raiz, space="  ")
    return ET.ElementTree(raiz)


def generar(ruta_datos: Path | None = None) -> Path:
    """Verifica y escribe el XML. Devuelve la ruta generada."""
    datos = cargar_datos(ruta_datos)
    fallos = verificar_radios(datos)
    if fallos:
        raise ValueError("Radios no concuerdan con la formula:\n" + "\n".join(fallos))
    destino = CARPETA / datos["general"]["archivo_salida"]
    construir_xml(datos).write(destino, encoding="utf-8", xml_declaration=True)
    return destino


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("Generado:", generar())
