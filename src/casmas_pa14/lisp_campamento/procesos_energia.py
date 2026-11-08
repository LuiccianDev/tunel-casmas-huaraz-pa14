"""Plantas de energía, hidrocarburos y polvorines SUCAMEC (EDIF-20, 21, 23, 28, 30, 31)."""

from __future__ import annotations

from .base import (
    Lienzo,
    Vano,
    cerco_malla,
    cerramiento,
    columnas,
    cotas_totales,
    ejes,
    estante,
    grupo_electrogeno,
    tabique,
    vehiculo,
)


def planta_casa_fuerza(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-20 (20x10m, 2500 kVA, 3 grupos) y EDIF-31 (15x8m, 1000 kVA, 2 grupos)."""
    esp = 0.15
    pot_kva = float(eq.get("potencia_kva", 2500.0 if largo >= 18 else 1000.0))
    n_gen = int(eq.get("n_grupos", 3 if largo >= 18 else 2))
    kva_unit = pot_kva / n_gen
    x_sala = round(largo * 0.68, 2)
    y_mit = round(ancho / 2.0, 2)

    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": [
                Vano(x_sala * 0.30, 2.40, "PO", etiqueta="CELOSIA ADMISION AIRE"),
                Vano(x_sala * 0.72, 2.40, "PO", etiqueta="PORTON ACUSTICO"),
                Vano((x_sala + largo) / 2, 1.20, "P2", "izq", "out", "SALA ELECTRICA"),
            ],
            "N": [Vano(x_sala * (i + 0.5) / n_gen, 1.80, "V") for i in range(n_gen)]
            + [Vano((x_sala + largo) / 2, 1.40, "V")],
        },
        achurar=True,
    )
    tabique(
        lz,
        x_sala,
        esp,
        x_sala,
        ancho - esp,
        [Vano(y_mit * 0.5, 1.10, "P", "izq", "+")],
        esp=0.18,
        capa="PA14-MUROS",
        achurar=True,
    )
    tabique(
        lz,
        x_sala,
        y_mit,
        largo - esp,
        y_mit,
        [Vano((x_sala + largo) / 2, 1.00, "P", "izq", "+")],
    )

    # Sala Acústica de Generación: Grupos Electrógenos Caterpillar sobre bancadas antivibratorias
    w_disp = x_sala - esp - 2.20
    paso_g = w_disp / n_gen
    wg = min(1.85, paso_g - 0.75)
    lg = min(4.60, ancho - 2.80)
    for i in range(n_gen):
        xg = esp + 0.45 + i * paso_g + (paso_g - (wg + 0.60)) / 2
        grupo_electrogeno(
            lz,
            xg,
            (ancho - (lg + 0.60)) / 2,
            wg,
            lg,
            f"GEN-{i + 1} ({kva_unit:.0f} kVA)",
        )

    # Tanques diarios de combustible (Day Tanks) dentro de cubeto en franja junto al muro divisorio
    lz.rect(x_sala - 1.55, esp + 0.35, 1.25, ancho - 2 * esp - 0.70, "PA14-OBRAS-ARTE")
    for i in range(n_gen):
        lz.circ(
            x_sala - 0.92,
            esp + 1.10 + i * ((ancho - 2.20) / n_gen),
            0.42,
            "PA14-APARATOS",
        )
    lz.txt(x_sala - 0.92, ancho - 0.60, "DAY TANKS", h=0.11, w_max=1.3)

    # Trinchera de cables de fuerza hacia Sala de Sincronismo y Transferencia Automática (ATS)
    lz.rect(esp + 0.60, esp + 0.35, x_sala + 1.60, 0.55, "PA14-OBRAS-ARTE")
    lz.achurado(esp + 0.60, esp + 0.35, x_sala + 1.60, 0.55, 0.35, "PA14-OBRAS-ARTE")

    w_el = largo - esp - x_sala
    # Cuarto Sur-Este: Tableros de Sincronismo, I/O, Transferencia ATS y Banco de Condensadores
    lz.rect(x_sala + 0.35, y_mit - 0.75, w_el - 0.70, 0.55, "PA14-APARATOS")
    for i in range(4):
        lz.lin(
            x_sala + 0.35 + i * ((w_el - 0.70) / 4),
            y_mit - 0.75,
            x_sala + 0.35 + i * ((w_el - 0.70) / 4),
            y_mit - 0.20,
            "PA14-APARATOS",
        )
    lz.txt(
        x_sala + w_el / 2,
        y_mit * 0.48,
        "TABLEROS SINCRONISMO Y ATS",
        h=0.14,
        w_max=w_el - 0.4,
    )

    # Cuarto Norte-Este: Subestación Elevadora / Transformador Seco Encapsulado + Puesta a Tierra
    xt_c, yt_c = x_sala + w_el / 2, y_mit + (ancho - esp - y_mit) / 2
    lz.rect(xt_c - 1.10, yt_c - 0.80, 2.20, 1.60, "PA14-APARATOS")
    lz.achurado(xt_c - 1.10, yt_c - 0.80, 2.20, 1.60, 0.35, "PA14-APARATOS")
    lz.txt(
        xt_c, yt_c + 1.15, f"TRANSFORMADOR {pot_kva:.0f} kVA", h=0.13, w_max=w_el - 0.4
    )

    xs = [0.0, x_sala, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "H")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return f"T2 - CASA DE FUERZA INSONORIZADA {pot_kva:.0f} kVA (RNE EM.010 / CNE)"


# =============================================================== EDIF-21 y 30
def planta_estacion_combustible(
    lz: Lienzo, largo: float, ancho: float, eq: dict
) -> str:
    """EDIF-21 (25x16m, 2x10,000 gal) y EDIF-30 (20x10m, 1x10,000 gal): Dique 110% + Isla Despacho."""
    n_tq = int(eq.get("n_tanques", 2 if ancho >= 14 else 1))
    cap_gal = float(eq.get("capacidad_tanque_gal", 10000.0))
    cerco_malla(
        lz,
        largo,
        ancho,
        {
            "O": [Vano(2.80, 4.00, "PC", etiqueta="INGRESO CISTERNA / VOLQUETES")],
            "E": [Vano(2.80, 4.00, "PC", etiqueta="SALIDA VEHICULAR")],
        },
    )

    y_div = round(
        ancho * 0.46, 2
    )  # Mitad Sur: Pista + Isla; Mitad Norte: Cubeto Estanco 110%

    # 1. Cubeto Estanco de Concreto Armado (Capacidad >= 110% según D.S. 052-93-EM / NFPA 30)
    xc, yc = 1.20, y_div + 0.40
    wc, hc = largo - 5.20, ancho - yc - 0.80
    with lz.local(xc, yc, 0):
        cerramiento(lz, wc, hc, 0.25, "PA14-MUROS", achurar=True)
    # Tanques cilíndricos horizontales de acero sobre cunas de concreto
    lt = wc - 2.40
    dt = min(2.60, (hc - 1.20) / n_tq - 0.35)
    for i in range(n_tq):
        yt = yc + 0.55 + i * ((hc - 1.10) / n_tq) + ((hc - 1.10) / n_tq - dt) / 2
        xt = xc + 1.20
        lz.rect(xt, yt, lt, dt, "PA14-APARATOS")
        lz.lin(xt, yt + dt / 2, xt + lt, yt + dt / 2, "PA14-EJE")
        # Cunas de concreto de soporte y boca de hombre (manhole)
        for xs_c in (xt + lt * 0.20, xt + lt * 0.50, xt + lt * 0.80):
            lz.rect(xs_c - 0.18, yt - 0.12, 0.36, dt + 0.24, "PA14-ESTRUCTURA")
        lz.circ(xt + lt * 0.35, yt + dt / 2, 0.32, "PA14-APARATOS")
        lz.txt(
            xt + lt * 0.62,
            yt + dt / 2,
            f"TANQUE DIESEL #{i + 1} ({cap_gal:,.0f} GAL)",
            h=0.15,
            w_max=lt * 0.55,
        )
    # Escalera metálica pasa-muro de acceso al cubeto y válvula de drenaje pluvial bloqueada
    lz.rect(xc + wc - 0.60, yc + 0.50, 0.90, 0.55, "PA14-ESCALERAS")
    lz.txt(
        xc + wc / 2,
        yc + hc - 0.45,
        "CUBETO ESTANCO CONCRETO ARMADO (RETENCION >= 110% - D.S. 052-93-EM)",
        h=0.14,
        w_max=wc - 1.0,
    )

    # 2. Losa Vehicular Impermeable e Isla de Despacho con Techo Metálico (Canopy)
    lz.rect(1.20, 0.80, wc, y_div - 0.80, "PA14-OBRAS-ARTE")
    xi, yi = xc + wc * 0.28, y_div - 1.35
    wi, hi = wc * 0.44, 1.15
    lz.rect(xi, yi, wi, hi, "PA14-ESTRUCTURA")
    lz.rect(xi + wi / 2 - 0.70, yi + 0.20, 1.40, hi - 0.40, "PA14-APARATOS")
    # 4 Bolardos tubulares de acero rellenos de concreto en esquinas de isla
    for bx in (xi + 0.20, xi + wi - 0.20):
        for by in (yi + 0.20, yi + hi - 0.20):
            lz.circ(bx, by, 0.14, "PA14-ESTRUCTURA")
    lz.txt(
        xi + wi / 2,
        yi + hi / 2,
        "ISLA SURTIDOR ALTO CAUDAL + CANOPY",
        h=0.13,
        w_max=wi - 0.6,
    )

    # Silueta de camión/volquete abasteciendo en la pista
    wv, lv = min(2.40, y_div - 2.30), min(7.50, wc * 0.45)
    vehiculo(
        lz, xc + wc * 0.50 - lv / 2, 1.10 + wv, wv, lv, "UNIDAD EN DESPACHO", rot=270
    )
    lz.flecha(1.80, 1.60, 2.50, 0, "PA14-EJE")
    lz.flecha(xc + wc - 3.20, 1.60, 2.50, 0, "PA14-EJE")

    # 3. Separador de Hidrocarburos API + Kit Antiderrames y Extintores Rodantes PQS (Este)
    xs_api = largo - 3.55
    lz.rect(xs_api, 1.00, 2.50, 3.80, "PA14-MUROS")
    lz.lin(xs_api, 2.25, xs_api + 2.50, 2.25, "PA14-APARATOS")
    lz.lin(xs_api, 3.50, xs_api + 2.50, 3.50, "PA14-APARATOS")
    lz.txt(xs_api + 1.25, 2.90, "TRAMPA HIDROCARBUROS API", h=0.12, w_max=3.4, ang=90)

    lz.rect(xs_api, ancho - 3.60, 2.50, 2.40, "PA14-MOBILIARIO")
    lz.txt(xs_api + 1.25, ancho - 2.40, "KIT ANTIDERRAME / PQS 50kg", h=0.11, w_max=2.3)

    cotas_totales(lz, largo, ancho)
    return "T4 - ESTACION DE COMBUSTIBLE CON CUBETO 110% Y CANOPY (DS 052-93-EM)"


# =============================================================== EDIF-23 y 28
def planta_polvorin_sucamec(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-23 (15x10m) y EDIF-28 (10x10m): Polvorín SUCAMEC con Parapeto de Tierra y 2 Cámaras."""
    # Cerco exterior de seguridad y malla Faraday
    cerco_malla(
        lz,
        largo,
        ancho,
        {"S": [Vano(largo / 2, 2.80, "P2", "izq", "out", "PORTON SEGURIDAD SUCAMEC")]},
    )

    # Parapeto perimetral de tierra apisonada (talud con peines de pendiente en N, E, O y S con chicane)
    b_ext = 0.85
    b_int = 2.05
    lz.rect(b_ext, b_ext, largo - 2 * b_ext, ancho - 2 * b_ext, "PA14-OBRAS-ARTE")
    lz.rect(b_int, b_int, largo - 2 * b_int, ancho - 2 * b_int, "PA14-OBRAS-ARTE")
    paso_t = 0.90
    for k in range(int((largo - 2 * b_int) / paso_t) + 1):
        xt = b_int + k * paso_t
        lz.lin(xt, ancho - b_int, xt, ancho - b_ext, "PA14-OBRAS-ARTE")
        if abs(xt - largo / 2) > 1.80:
            lz.lin(xt, b_int, xt, b_ext, "PA14-OBRAS-ARTE")
    for k in range(int((ancho - 2 * b_int) / paso_t) + 1):
        yt = b_int + k * paso_t
        lz.lin(b_int, yt, b_ext, yt, "PA14-OBRAS-ARTE")
        lz.lin(largo - b_int, yt, largo - b_ext, yt, "PA14-OBRAS-ARTE")
    lz.txt(
        largo / 2,
        ancho - 1.45,
        "PARAPETO PERIMETRAL DE TIERRA APISONADA (H=3.50m, TALUD 1:1.5 - LEY 30299)",
        h=0.13,
        w_max=largo - 4.0,
    )

    # Búnker central de concreto armado (e = 0.30 m, achurado) con 2 compartimentos independientes
    xb, yb = 2.55, 2.55
    wb, hb = largo - 5.10, ancho - 5.10
    x_part = round(
        wb * 0.68, 2
    )  # 68% Cámara A (Explosivos) | 32% Cámara B (Detonadores/Accesorios)
    with lz.local(xb, yb, 0):
        cerramiento(
            lz,
            wb,
            hb,
            0.30,
            "PA14-MUROS",
            {
                "S": [
                    Vano(x_part * 0.50, 1.20, "P2", "izq", "out", "CAMARA A"),
                    Vano(
                        x_part + (wb - x_part) * 0.50,
                        1.00,
                        "P",
                        "izq",
                        "out",
                        "CAMARA B",
                    ),
                ]
            },
            achurar=True,
        )
        # Muro antifragmentación macizo de 0.30 m entre explosivos y accesorios
        tabique(
            lz,
            x_part,
            0.30,
            x_part,
            hb - 0.30,
            esp=0.30,
            capa="PA14-MUROS",
            achurar=True,
        )

        # Cámara A: Parihuelas de madera tratada sin metales (cajas de emulsión y dinamita)
        w_p = (x_part - 1.10) / 2
        for ix in range(2):
            for iy in range(2):
                estante(
                    lz,
                    0.50 + ix * (w_p + 0.25),
                    0.70 + iy * ((hb - 1.40) / 2),
                    w_p - 0.15,
                    (hb - 2.00) / 2,
                    3,
                )
        lz.txt(
            x_part / 2,
            hb / 2,
            "CAMARA A: EMULSION Y DINAMITA",
            h=0.14,
            w_max=x_part - 0.6,
        )

        # Cámara B: Estantería ignífuga para detonadores no eléctricos (Fanel) y cordón detonante
        w_cb = wb - x_part
        estante(lz, x_part + 0.35, hb - 1.05, w_cb - 0.70, 0.55, 2)
        estante(lz, x_part + 0.35, 0.85, w_cb - 0.70, 0.55, 2)
        lz.txt(
            x_part + w_cb / 2, hb / 2, "CAMARA B: DETONADORES", h=0.12, w_max=w_cb - 0.4
        )

    # Pararrayos dipolo corona (jaula Faraday) y barra de descarga de corriente estática
    lz.circ(0.45, ancho - 0.45, 0.28, "PA14-SIMBOLOS")
    lz.circ(largo - 0.45, ancho - 0.45, 0.28, "PA14-SIMBOLOS")
    lz.txt(1.80, ancho - 0.45, "PARARRAYOS FARADAY", h=0.11, w_max=2.2)

    cotas_totales(lz, largo, ancho)
    return "T5 - POLVORIN DE SUPERFICIE CON PARAPETO DE TIERRA (SUCAMEC LEY 30299)"
