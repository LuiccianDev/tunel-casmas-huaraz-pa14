"""Trazado urbanístico del Master Plan General para Campamento 1 y Campamento 2."""

from __future__ import annotations

from ..lisp import Dibujo
from .base import Lienzo


def _huella_master_edif(lz: Lienzo, e: dict, x: float, y: float) -> None:
    """Dibuja la huella urbanística de una instalación en el Master Plan según su tipología real."""
    cid = e["id"]
    w = float(e["largo_m"])
    h = float(e["ancho_m"])

    if cid in ("EDIF-24", "EDIF-25", "EDIF-26", "EDIF-27"):
        # T3: Plataforma vial / parqueo abierto (sin muros de edificio)
        lz.rect(x, y, w, h, "PA14-OBRAS-ARTE")
        lz.lin(x + 0.5, y + h / 2, x + w - 0.5, y + h / 2, "PA14-EJE")
        n_b = max(3, int(w // 3.5))
        wb = (w - 1.0) / n_b
        for i in range(n_b):
            lz.rect(x + 0.5 + i * wb, y + 0.4, wb - 0.2, h * 0.30, "PA14-MOBILIARIO")
            lz.rect(
                x + 0.5 + i * wb,
                y + h * 0.70 - 0.4,
                wb - 0.2,
                h * 0.30,
                "PA14-MOBILIARIO",
            )
    elif cid in (
        "EDIF-14",
        "EDIF-15",
        "EDIF-16",
        "EDIF-17",
        "EDIF-18",
        "EDIF-19",
        "EDIF-21",
        "EDIF-30",
        "EDIF-32",
    ):
        # T4: Planta cercada con malla olímpica y unidades de proceso (tanques/reactores)
        lz.rect(x, y, w, h, "PA14-CERCO")
        if cid in ("EDIF-15", "EDIF-16", "EDIF-32"):
            r_t = min(h * 0.32, 3.2)
            lz.circ(x + w - r_t - 1.2, y + h / 2, r_t, "PA14-APARATOS")
            lz.rect(
                x + 0.8, y + 0.8, max(2.0, w - 2 * r_t - 2.8), h - 1.6, "PA14-APARATOS"
            )
        elif cid in ("EDIF-21", "EDIF-30"):
            lz.rect(x + 0.8, y + h * 0.45, w - 1.6, h * 0.45, "PA14-MUROS")
            lz.rect(x + 1.4, y + h * 0.52, w - 2.8, h * 0.30, "PA14-APARATOS")
        else:
            lz.rect(
                x + 0.6, y + 0.6, max(1.0, w - 1.2), max(1.0, h - 1.2), "PA14-APARATOS"
            )
    elif cid == "EDIF-02":
        # T1 Doble Pabellón Paralelo (Pabellón A y Pabellón B)
        h_ala = (h - 3.2) / 2
        for ya in (y, y + h_ala + 3.2):
            lz.rect(x, ya, w, h_ala, "PA14-EDIFICACION")
            lz.rect(x + 0.20, ya + 0.20, w - 0.40, h_ala - 0.40, "PA14-MUROS")
            lz.lin(x, ya + h_ala / 2, x + w, ya + h_ala / 2, "PA14-ESTRUCTURA")
        lz.rect(x - 0.80, y - 0.80, w + 1.60, h + 1.60, "PA14-OBRAS-ARTE")
    else:
        # T1 / T2: Edificación techada con muros perimetrales, cumbrera y vereda
        lz.rect(x, y, w, h, "PA14-EDIFICACION")
        lz.rect(
            x + 0.20, y + 0.20, max(0.4, w - 0.40), max(0.4, h - 0.40), "PA14-MUROS"
        )
        lz.lin(x, y + h / 2, x + w, y + h / 2, "PA14-ESTRUCTURA")
        lz.rect(x - 0.70, y - 0.70, w + 1.40, h + 1.40, "PA14-OBRAS-ARTE")

    lz.txt(x + w / 2, y + h * 0.62, f"{cid}: {e['nombre']}", h=0.42, w_max=w - 0.6)
    lz.txt(
        x + w / 2,
        y + h * 0.34,
        f"{w:.1f}x{h:.1f}m ({e['area_m2']:.0f} m2)",
        h=0.36,
        w_max=w - 0.6,
    )


def dibujo_master_campamento(
    codigo_camp: str,
    titulo_camp: str,
    edifs_camp: list[dict],
    poblacion_pax: int,
) -> Dibujo:
    """Genera el Master Plan General urbanístico de un Campamento (CAMP1 o CAMP2) con zonificación."""
    num_c = "1" if codigo_camp == "CAMP1" else "2"
    comando = f"PA14_CAMP_{num_c}"

    edifs_polvorin = [
        e for e in edifs_camp if e["id"] in ("EDIF-23", "EDIF-28", "EDIF-37", "EDIF-38")
    ]
    edifs_internas = [e for e in edifs_camp if e not in edifs_polvorin]

    z1 = [
        e
        for e in edifs_internas
        if e["grupo"]
        in (
            "Administración y Documentos",
            "Salud y Bienestar",
            "Vigilancia y Transporte",
        )
        and e["area_m2"] <= 650
    ]
    z2 = [
        e
        for e in edifs_internas
        if e["grupo"] in ("Residencia y Habitabilidad", "Comedor y Alimentación")
    ]
    z3 = [
        e
        for e in edifs_internas
        if e["grupo"]
        in (
            "Maquinaria y Mantenimiento",
            "Almacenes y Logística",
            "Operación y Portales",
        )
        or (e["grupo"] == "Vigilancia y Transporte" and e["area_m2"] > 650)
    ]
    z4 = [e for e in edifs_internas if e not in z1 and e not in z2 and e not in z3]

    zonas = [
        ("ZONA I: CONTROL DE ACCESO, ADMINISTRACION Y SALUD OCUPACIONAL", z1),
        ("ZONA II: RESIDENCIA TERMICA, HABITABILIDAD Y COMEDOR CENTRAL", z2),
        (
            "ZONA III: MAESTRANZA, TALLERES, LOGISTICA, CHANGE-HOUSE Y PATIO DE MANIOBRAS",
            z3,
        ),
        (
            "ZONA IV: ENERGIA, ESTACION DE DIESEL (RET. 15m), PTAP/PTAR Y GESTION AMBIENTAL",
            z4,
        ),
    ]

    lz = Lienzo()
    margen_x = 14.0
    sep_x = 8.5
    via_ancho = 8.0
    y_cursor = 14.0
    max_x_usado = 125.0

    for nom_zona, lista_z in zonas:
        if not lista_z:
            continue
        y_via = y_cursor - via_ancho / 2
        x_cursor = margen_x
        alto_fila = max(float(e["ancho_m"]) for e in lista_z)
        for e in lista_z:
            _huella_master_edif(lz, e, x_cursor, y_cursor)
            x_cursor += float(e["largo_m"]) + sep_x
        max_x_usado = max(max_x_usado, x_cursor + margen_x)
        # Vía afirmada transversal con eje y flechas de sentido
        lz.lin(margen_x - 4.0, y_via, max_x_usado - 8.0, y_via, "PA14-EJE")
        lz.flecha(margen_x + 2.0, y_via + 1.2, 5.0, 0, "PA14-EJE")
        lz.txt_izq(
            margen_x,
            y_via - 1.2,
            f"=== {nom_zona} (VIA INTERNA AFIRMADA A = 6.00 m + CUNETAS PLUVIALES) ===",
            h=0.60,
        )
        y_cursor += alto_fila + 18.0

    ancho_camp = max_x_usado
    alto_camp = y_cursor + 6.0

    # Avenida troncal Norte-Sur y Cerco Perimétrico General con Rosa Náutica
    lz.rect(0.0, 0.0, ancho_camp, alto_camp, "PA14-CERCO")
    lz.rect(-1.50, -1.50, ancho_camp + 3.00, alto_camp + 3.00, "PA14-OBRAS-ARTE")
    lz.lin(margen_x - 4.0, 0.0, margen_x - 4.0, alto_camp, "PA14-EJE")
    lz.flecha(margen_x - 4.0, 4.0, 8.0, 90, "PA14-EJE")
    lz.circ(ancho_camp - 8.0, alto_camp - 8.0, 3.0, "PA14-SIMBOLOS")
    lz.flecha(ancho_camp - 8.0, alto_camp - 10.5, 5.0, 90, "PA14-SIMBOLOS")
    lz.txt(ancho_camp - 8.0, alto_camp - 4.0, "N", h=0.80)

    lz.cota(
        0.0,
        0.0,
        ancho_camp,
        0.0,
        ancho_camp / 2,
        -5.0,
        f"{ancho_camp:.1f} m (FRENTE CAMPAMENTO {codigo_camp})",
    )
    lz.cota(
        0.0,
        0.0,
        0.0,
        alto_camp,
        -6.0,
        alto_camp / 2,
        f"{alto_camp:.1f} m (FONDO CAMPAMENTO {codigo_camp})",
    )

    # Complejo Externo Aislado de Explosivos SUCAMEC (Retiro normativo >= 300 m)
    if edifs_polvorin:
        x_polv = ancho_camp + 26.0
        w_box = 52.0
        h_box = 36.0
        lz.rect(x_polv, 10.0, w_box, h_box, "PA14-CERCO")
        lz.lin(ancho_camp, 28.0, x_polv, 28.0, "PA14-EJE")
        lz.cota(
            ancho_camp,
            28.0,
            x_polv,
            28.0,
            (ancho_camp + x_polv) / 2,
            31.5,
            "RETIRO >= 300 m (SUCAMEC LEY 30299)",
        )
        lz.txt(
            x_polv + w_box / 2,
            10.0 + h_box - 2.8,
            f"COMPLEJO AISLADO DE EXPLOSIVOS Y CUSTODIA ARMADA ({codigo_camp})",
            h=0.60,
            w_max=w_box - 4.0,
        )
        xp_i = x_polv + 5.0
        for ep in edifs_polvorin:
            wp = float(ep["largo_m"])
            hp = float(ep["ancho_m"])
            lz.rect(xp_i, 16.0, wp, hp, "PA14-EDIFICACION")
            lz.rect(xp_i - 1.5, 16.0 - 1.5, wp + 3.0, hp + 3.0, "PA14-OBRAS-ARTE")
            lz.txt(
                xp_i + wp / 2,
                16.0 + hp / 2,
                f"{ep['id']}: {ep['nombre']}",
                h=0.38,
                w_max=max(wp + 2.0, 8.0),
            )
            xp_i += wp + 9.0
        ancho_camp_total = x_polv + w_box + 10.0
    else:
        ancho_camp_total = ancho_camp + 10.0

    # Membrete General del Master Plan del Campamento
    area_tot_edif = sum(e["area_m2"] for e in edifs_camp)
    lz.rect(0.0, -18.5, ancho_camp, 10.5, "PA14-MEMBRETE")
    lz.txt_izq(
        3.0,
        -10.8,
        f"MASTER PLAN ARQUITECTONICO Y VIAL: {titulo_camp.upper()} ({codigo_camp})",
        h=1.05,
    )
    lz.txt_izq(
        3.0,
        -13.4,
        f"POBLACION DE DISENO: {poblacion_pax} TRABAJADORES | TOTAL INSTALACIONES: {len(edifs_camp)} | AREA CONSTRUIDA: {area_tot_edif:,.1f} m2",
        h=0.72,
    )
    lz.txt_izq(
        3.0,
        -15.9,
        "NORMATIVA: RNE G.050, A.010, A.060, A.070, A.080, OS.020, OS.090 / D.S. 024-2016-EM / D.S. 052-93-EM / LEY 30299 SUCAMEC (3,850 msnm)",
        h=0.62,
    )

    return Dibujo(
        comando=comando,
        descripcion=f"Master Plan General {codigo_camp} - {titulo_camp}",
        cuerpo=lz.cmds,
        ancho=ancho_camp_total,
    )
