"""07 · Polvorín: consumo de explosivos/accesorios y dimensiones."""

import math

from ..modelo import Hoja, Libro, redondear_arriba, tabla_parametros

CLAVE = "polvorin"


def dimensionar(cajas: int, c: dict) -> dict:
    """Distribuye las cajas en rumas y obtiene las dimensiones del polvorín."""
    cajas_por_ruma = math.floor(c["altura_max_ruma_m"] / c["caja_alto_m"])
    rumas = math.ceil(cajas / cajas_por_ruma)
    rumas_por_fila = math.ceil(rumas / c["filas"])
    largo_int = (
        rumas_por_fila * c["caja_largo_m"]
        + (rumas_por_fila - 1) * c["separacion_rumas_m"]
        + 2 * c["separacion_pared_m"]
    )
    ancho_int = (
        c["filas"] * c["caja_ancho_m"]
        + max(c["filas"] - 1, 1) * c["pasillo_m"]
        + 2 * c["separacion_pared_m"]
    )
    alto_int = cajas_por_ruma * c["caja_alto_m"] + c["altura_libre_m"]
    largo_int, ancho_int = (
        redondear_arriba(largo_int, 0.1),
        redondear_arriba(ancho_int, 0.1),
    )
    return {
        "cajas": cajas,
        "cajas_por_ruma": cajas_por_ruma,
        "rumas": rumas,
        "rumas_por_fila": rumas_por_fila,
        "largo_int_m": largo_int,
        "ancho_int_m": ancho_int,
        "alto_int_m": alto_int,
        "largo_ext_m": largo_int + 2 * c["espesor_muro_m"],
        "ancho_ext_m": ancho_int + 2 * c["espesor_muro_m"],
        "area_int_m2": largo_int * ancho_int,
        "config": c,
    }


def calcular(p: dict, ctx: dict) -> dict:
    sec, pol, f = ctx["seccion"], p["polvorin"], p["perforacion"]
    disparos_dia = f["disparos_por_dia_frente"] * f["frentes"]
    kg_disparo = f["factor_carga_kg_m3"] * sec["v_disparo_m3"]
    kg_stock = kg_disparo * disparos_dia * pol["dias_stock"]
    acc = pol["accesorios"]
    det_disparo = sec["taladros"] * acc["detonadores_por_taladro"]
    det_stock = det_disparo * disparos_dia * pol["dias_stock"]
    exp = pol["explosivos"]
    return {
        "disparos_dia": disparos_dia,
        "kg_disparo": kg_disparo,
        "kg_dia": kg_disparo * disparos_dia,
        "kg_stock": kg_stock,
        "det_disparo": det_disparo,
        "det_dia": det_disparo * disparos_dia,
        "det_stock": det_stock,
        "explosivos": dimensionar(math.ceil(kg_stock / exp["unidades_por_caja"]), exp),
        "accesorios": dimensionar(math.ceil(det_stock / acc["unidades_por_caja"]), acc),
    }


def _tabla_dimensiones(d: dict, titulo: str):
    c = d["config"]
    return tabla_parametros(
        [
            (
                "Cajas a almacenar",
                "nc",
                d["cajas"],
                "und",
                "⌈stock / unidades por caja⌉",
            ),
            (
                "Caja (largo × ancho × alto)",
                "",
                f"{c['caja_largo_m']} × {c['caja_ancho_m']} × {c['caja_alto_m']}",
                "m",
                "Dato",
            ),
            (
                "Cajas por ruma",
                "cr",
                d["cajas_por_ruma"],
                "und",
                "⌊h máx ruma / alto caja⌋",
            ),
            ("Número de rumas", "nr", d["rumas"], "und", "⌈nc / cr⌉"),
            ("Filas de rumas", "nf", c["filas"], "und", "Dato"),
            ("Rumas por fila", "rf", d["rumas_por_fila"], "und", "⌈nr / nf⌉"),
            ("Largo interior", "Li", d["largo_int_m"], "m", "rf·l + (rf−1)·s + 2·sp"),
            ("Ancho interior", "Ai", d["ancho_int_m"], "m", "nf·a + pasillo + 2·sp"),
            ("Alto interior", "Hi", d["alto_int_m"], "m", "cr·h + altura libre"),
            ("Área interior", "Si", d["area_int_m2"], "m²", "Li · Ai"),
            (
                "Dimensiones exteriores (L × A)",
                "",
                f"{d['largo_ext_m']:.2f} × {d['ancho_ext_m']:.2f}",
                "m",
                "Interior + 2·muro",
            ),
        ],
        titulo,
    )


def libro(r: dict, p: dict) -> Libro:
    f, pol = p["perforacion"], p["polvorin"]
    consumo = tabla_parametros(
        [
            ("Factor de carga", "fc", f["factor_carga_kg_m3"], "kg/m³", "Dato"),
            (
                "Disparos por día (todos los frentes)",
                "nd",
                r["disparos_dia"],
                "und",
                "03_Seccion",
            ),
            ("Explosivo por disparo", "Qd", r["kg_disparo"], "kg", "fc · Vd"),
            ("Explosivo por día", "Qdía", r["kg_dia"], "kg", "Qd · nd"),
            ("Días de stock", "ds", pol["dias_stock"], "días", "Dato"),
            ("Explosivo almacenado", "Qs", r["kg_stock"], "kg", "Qdía · ds"),
            (
                "Detonadores por disparo",
                "Dd",
                r["det_disparo"],
                "und",
                "N taladros · det/taladro",
            ),
            ("Detonadores por día", "Ddía", r["det_dia"], "und", "Dd · nd"),
            ("Detonadores almacenados", "Ds", r["det_stock"], "und", "Ddía · ds"),
        ]
    )
    return Libro(
        "07_Polvorin.xlsx",
        [
            Hoja("Consumo", "Consumo y stock de explosivos y accesorios", [consumo]),
            Hoja(
                "Dimensiones",
                "Dimensiones de polvorines (explosivos y accesorios separados)",
                [
                    _tabla_dimensiones(r["explosivos"], "Polvorín de explosivos"),
                    _tabla_dimensiones(r["accesorios"], "Polvorín de accesorios"),
                ],
            ),
        ],
    )
