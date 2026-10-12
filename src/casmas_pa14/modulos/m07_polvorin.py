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
        "v_disparo_m3": sec["v_disparo_m3"],
        "taladros_disparo": sec["taladros"],
        "det_por_taladro": acc["detonadores_por_taladro"],
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


def _tabla_dimensiones(d: dict, titulo: str, suf: str = ""):
    c = d["config"]
    pasillo_total = max(c["filas"] - 1, 1) * c["pasillo_m"]
    nc, lc, ac, hc = f"nc{suf}", f"lc{suf}", f"ac{suf}", f"hc{suf}"
    hm, cr, nr, nf, rf = f"hm{suf}", f"cr{suf}", f"nr{suf}", f"nf{suf}", f"rf{suf}"
    li, ai, hi, si = f"Li{suf}", f"Ai{suf}", f"Hi{suf}", f"Si{suf}"
    le, ae = f"Le{suf}", f"Ae{suf}"
    return tabla_parametros(
        [
            (
                "Cajas a almacenar",
                nc,
                d["cajas"],
                "und",
                "⌈stock / unidades por caja⌉",
            ),
            ("Largo de caja", lc, c["caja_largo_m"], "m", "Dato"),
            ("Ancho de caja", ac, c["caja_ancho_m"], "m", "Dato"),
            ("Alto de caja", hc, c["caja_alto_m"], "m", "Dato"),
            ("Altura máxima de ruma", hm, c["altura_max_ruma_m"], "m", "SUCAMEC"),
            (
                "Cajas por ruma",
                cr,
                f"=FLOOR({{{hm}}}/{{{hc}}}, 1)",
                "und",
                "⌊h máx ruma / alto caja⌋",
            ),
            (
                "Número de rumas",
                nr,
                f"=CEILING({{{nc}}}/{{{cr}}}, 1)",
                "und",
                "⌈nc / cr⌉",
            ),
            ("Filas de rumas", nf, c["filas"], "und", "Dato"),
            (
                "Rumas por fila",
                rf,
                f"=CEILING({{{nr}}}/{{{nf}}}, 1)",
                "und",
                "⌈nr / nf⌉",
            ),
            (
                "Largo interior",
                li,
                f"=CEILING({{{rf}}}*{{{lc}}}+({{{rf}}}-1)*{c['separacion_rumas_m']}+2*{c['separacion_pared_m']}, 0.1)",
                "m",
                "rf·l + (rf−1)·s + 2·sp",
            ),
            (
                "Ancho interior",
                ai,
                f"=CEILING({{{nf}}}*{{{ac}}}+{pasillo_total}+2*{c['separacion_pared_m']}, 0.1)",
                "m",
                "nf·a + pasillo + 2·sp",
            ),
            (
                "Alto interior",
                hi,
                f"={{{cr}}}*{{{hc}}}+{c['altura_libre_m']}",
                "m",
                "cr·h + altura libre",
            ),
            ("Área interior", si, f"={{{li}}}*{{{ai}}}", "m²", "Li · Ai"),
            (
                "Largo exterior",
                le,
                f"={{{li}}}+2*{c['espesor_muro_m']}",
                "m",
                "Li + 2·muro",
            ),
            (
                "Ancho exterior",
                ae,
                f"={{{ai}}}+2*{c['espesor_muro_m']}",
                "m",
                "Ai + 2·muro",
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
                "Volumen por disparo (03_Seccion)",
                "Vd",
                round(r["v_disparo_m3"], 2),
                "m³",
                "03_Seccion",
            ),
            (
                "Disparos por día (todos los frentes)",
                "nd",
                r["disparos_dia"],
                "und",
                "03_Seccion",
            ),
            ("Explosivo por disparo", "Qd", "={fc}*{Vd}", "kg", "fc · Vd"),
            ("Explosivo por día", "Qdia", "={Qd}*{nd}", "kg", "Qd · nd"),
            ("Días de stock", "ds", pol["dias_stock"], "días", "Dato"),
            ("Explosivo almacenado", "Qs", "={Qdia}*{ds}", "kg", "Qdía · ds"),
            (
                "Taladros por disparo (03_Seccion)",
                "Ntal",
                r["taladros_disparo"],
                "und",
                "03_Seccion",
            ),
            (
                "Detonadores por taladro",
                "dpt",
                r["det_por_taladro"],
                "und",
                "Dato",
            ),
            (
                "Detonadores por disparo",
                "Dd",
                "={Ntal}*{dpt}",
                "und",
                "N taladros · det/taladro",
            ),
            ("Detonadores por día", "Ddia", "={Dd}*{nd}", "und", "Dd · nd"),
            ("Detonadores almacenados", "Ds", "={Ddia}*{ds}", "und", "Ddía · ds"),
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
                    _tabla_dimensiones(r["explosivos"], "Polvorín de explosivos", "_e"),
                    _tabla_dimensiones(r["accesorios"], "Polvorín de accesorios", "_a"),
                ],
            ),
        ],
    )
