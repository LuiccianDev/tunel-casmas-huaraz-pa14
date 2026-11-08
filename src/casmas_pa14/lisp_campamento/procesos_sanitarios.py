"""Plantas sanitarias y ambientales con cerco perimétrico (EDIF-14..19, 32)."""

from __future__ import annotations

import math

from .base import (
    Lienzo,
    Vano,
    cerco_malla,
    cerramiento,
    cotas_totales,
    escritorio,
    tabique,
    tanque_vertical,
)


def planta_edif_14(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-14 (8x5m): Caseta de Pozo Profundo (5 L/s), tren hidráulico y cloración."""
    caudal = float(eq.get("caudal_lps", 5.0))
    diam_pulg = float(eq.get("diametro_pozo_pulg", 8.0))
    cerco_malla(
        lz,
        largo,
        ancho,
        {"S": [Vano(largo / 2, 1.80, "P2", "izq", "out", "PORTON CASETA POZO")]},
    )

    # Caseta técnica interior de concreto/mampostería (6.80 x 3.80 m)
    with lz.local(0.60, 0.60, 0):
        cerramiento(
            lz,
            largo - 1.20,
            ancho - 1.20,
            0.15,
            "PA14-MUROS",
            {
                "S": [Vano((largo - 1.20) / 2, 1.20, "P2", "izq", "out")],
                "N": [
                    Vano((largo - 1.20) * 0.35, 1.10, "V"),
                    Vano((largo - 1.20) * 0.72, 1.10, "V"),
                ],
            },
            achurar=True,
        )

    # Dado sanitario de concreto (1.50 x 1.50 m) y cabezal de pozo tubular Ø 8"
    xp, yp = 2.10, ancho / 2
    lz.rect(xp - 0.75, yp - 0.75, 1.50, 1.50, "PA14-OBRAS-ARTE")
    lz.circ(xp, yp, 0.32, "PA14-APARATOS")
    lz.circ(xp, yp, 0.16, "PA14-APARATOS")
    lz.txt(
        xp, yp - 1.00, f"POZO D={diam_pulg:.0f}in ({caudal:.1f} L/s)", h=0.12, w_max=2.2
    )

    # Tren de impulsión: tubería 3", válvula check, válvula compuerta y macromedidor
    lz.rect(xp + 0.32, yp - 0.08, 3.60, 0.16, "PA14-APARATOS")
    for xv, etq in (
        (xp + 1.10, "V.CHECK"),
        (xp + 2.05, "V.COMP"),
        (xp + 3.05, "MEDIDOR"),
    ):
        lz.circ(xv, yp, 0.22, "PA14-SIMBOLOS")
        lz.txt(xv, yp + 0.42, etq, h=0.10, w_max=0.85)

    # Tablero arrancador VFD (Norte) y Tanque Dosificador de Cloro (Sur)
    lz.rect(largo - 2.35, ancho - 1.45, 1.50, 0.55, "PA14-APARATOS")
    lz.txt(largo - 1.60, ancho - 1.70, "TABLERO VFD", h=0.11, w_max=1.5)
    lz.circ(largo - 1.55, 1.45, 0.42, "PA14-APARATOS")
    lz.txt(largo - 1.55, 1.45, "CLORO", h=0.10, w_max=0.75)

    cotas_totales(lz, largo, ancho)
    return "T4 - CASETA DE CAPTACION Y BOMBEO CON CERCO (RNE OS.010)"


# ===================================================================== EDIF-15
def planta_edif_15(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-15 (24x15m): Planta PTAP (floculador, sedimentador, filtros) + Reservorio 120 m³."""
    vol_res = float(eq.get("reservorio_m3", 120.0))
    h_agua = float(eq.get("altura_agua_m", 3.0))
    r_int = math.sqrt(vol_res / (math.pi * h_agua))  # 3.57 m
    r_ext = round(r_int + 0.25, 2)  # 3.82 m (D = 7.64 m)

    cerco_malla(
        lz, largo, ancho, {"S": [Vano(5.0, 3.60, "PC", etiqueta="PORTON ACCESO PTAP")]}
    )

    # Tren hidráulico de potabilización (mitad izquierda X = 1.2 .. 13.5 m)
    # 1. Floculador hidráulico de pantallas (baffles) al Norte-Oeste
    xf, yf, wf, hf = 1.20, ancho - 5.60, 5.20, 4.20
    lz.rect(xf, yf, wf, hf, "PA14-MUROS")
    lz.rect(xf + 0.20, yf + 0.20, wf - 0.40, hf - 0.40, "PA14-APARATOS")
    for i in range(1, 5):
        xb = xf + i * (wf / 5)
        y_ini = yf + 0.20 if i % 2 else yf + 0.90
        y_fin = yf + hf - 0.90 if i % 2 else yf + hf - 0.20
        lz.lin(xb, y_ini, xb, y_fin, "PA14-APARATOS")
    lz.txt(xf + wf / 2, yf - 0.35, "1. MEZCLA Y FLOCULADOR", h=0.14, w_max=wf)

    # 2. Sedimentador laminar de alta tasa (centro Norte)
    xs, ys_sed, ws, hs = 7.00, ancho - 5.60, 6.20, 4.20
    lz.rect(xs, ys_sed, ws, hs, "PA14-MUROS")
    lz.achurado(xs + 0.25, ys_sed + 0.25, ws - 0.50, hs - 0.50, 0.55, "PA14-APARATOS")
    lz.txt(xs + ws / 2, ys_sed - 0.35, "2. SEDIMENTADOR LAMINAR", h=0.14, w_max=ws)

    # 3. Batería de 2 Filtros Multimedia a Presión + Caseta de Cloración y Bombeo (Sur-Oeste)
    lz.rect(1.20, 1.40, 12.00, 5.40, "PA14-OBRAS-ARTE")
    for k in range(2):
        xf_k = 3.00 + k * 2.80
        lz.circ(xf_k, 4.10, 0.95, "PA14-APARATOS")
        lz.circ(xf_k, 4.10, 0.20, "PA14-APARATOS")
        lz.txt(xf_k, 4.10, f"FILTRO F-{k + 1}", h=0.12, w_max=1.6)
    # Caseta de cloración y bombas hidroneumáticas
    with lz.local(7.60, 1.70, 0):
        cerramiento(
            lz,
            5.20,
            4.60,
            0.15,
            "PA14-MUROS",
            {"O": [Vano(2.30, 1.10, "P", "izq", "in")]},
            achurar=True,
        )
    for k in range(2):
        lz.circ(8.80 + k * 1.40, 3.20, 0.45, "PA14-APARATOS")
        lz.rect(8.60 + k * 1.40, 4.30, 0.85, 0.55, "PA14-APARATOS")
    lz.txt(10.20, 5.70, "3. CASETA CLORACION Y BOMBAS", h=0.13, w_max=5.0)

    # 4. Reservorio Circular de Concreto Armado (120 m³) en mitad derecha
    xr, yr = largo - r_ext - 1.60, ancho / 2 + 0.60
    tanque_vertical(
        lz,
        xr,
        yr,
        r_ext,
        f"RESERVORIO APOYADO V={vol_res:.0f} m3 (D={2 * r_ext:.2f}m)",
        e_muro=0.25,
    )
    # Cámara de válvulas del reservorio
    lz.rect(xr - 1.10, yr - r_ext - 1.50, 2.20, 1.30, "PA14-MUROS")
    lz.txt(xr, yr - r_ext - 0.85, "CAMARA VALVULAS", h=0.12, w_max=2.0)

    cotas_totales(lz, largo, ancho)
    return "T4 - PLANTA POTABILIZADORA PTAP Y RESERVORIO CON CERCO (RNE OS.020)"


# ===================================================================== EDIF-16
def planta_edif_16(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-16 (24x15m): Planta PTAR Biológica MBBR, Clarificador Circular, UV y Lecho de Lodos."""
    cerco_malla(
        lz,
        largo,
        ancho,
        {"S": [Vano(4.50, 3.60, "PC", etiqueta="PORTON MANTENIMIENTO PTAR")]},
    )

    # 1. Cámara de rejas, desarenador y tanque de ecualización (Oeste)
    lz.rect(1.10, ancho - 5.20, 4.20, 3.80, "PA14-MUROS")
    lz.lin(1.10, ancho - 3.30, 5.30, ancho - 3.30, "PA14-APARATOS")
    lz.txt(3.20, ancho - 2.35, "REJAS / DESARENADOR", h=0.12, w_max=3.8)
    lz.txt(3.20, ancho - 4.25, "ECUALIZACION", h=0.13, w_max=3.8)

    # 2. Dos Reactores Aeróbicos de Lecho Móvil MBBR en paralelo (Centro-Norte)
    xr, yr, wr, hr = 6.00, ancho - 6.60, 7.60, 5.20
    lz.rect(xr, yr, wr, hr, "PA14-MUROS")
    lz.lin(xr, yr + hr / 2, xr + wr, yr + hr / 2, "PA14-MUROS")
    lz.puntos(xr + 0.30, yr + 0.30, wr - 0.60, hr / 2 - 0.60, 0.55, "PA14-APARATOS")
    lz.puntos(
        xr + 0.30, yr + hr / 2 + 0.30, wr - 0.60, hr / 2 - 0.60, 0.55, "PA14-APARATOS"
    )
    lz.txt(
        xr + wr / 2,
        yr + hr * 0.75,
        "REACTOR MBBR 1 (BIOPORTADORES)",
        h=0.14,
        w_max=wr - 0.6,
    )
    lz.txt(
        xr + wr / 2,
        yr + hr * 0.25,
        "REACTOR MBBR 2 (AIREACION DIFUSA)",
        h=0.14,
        w_max=wr - 0.6,
    )

    # 3. Sedimentador Secundario Circular con puente barre-lodos (Este-Norte)
    xc, yc, rc = 17.60, ancho - 4.10, 2.75
    lz.circ(xc, yc, rc, "PA14-MUROS")
    lz.circ(xc, yc, rc - 0.22, "PA14-APARATOS")
    lz.circ(xc, yc, 0.45, "PA14-APARATOS")
    lz.rect(xc - rc + 0.10, yc - 0.25, 2 * rc - 0.20, 0.50, "PA14-ESTRUCTURA")
    lz.txt(xc, yc - rc - 0.40, "CLARIFICADOR SECUNDARIO (D=5.50m)", h=0.13, w_max=5.4)

    # 4. Caseta acústica de sopladores (Sur-Centro)
    with lz.local(6.00, 1.50, 0):
        cerramiento(
            lz,
            5.40,
            4.20,
            0.15,
            "PA14-MUROS",
            {"O": [Vano(2.10, 1.10, "P", "izq", "in")]},
            achurar=True,
        )
    for k in range(3):
        lz.rect(6.60 + k * 1.45, 2.60, 1.00, 1.40, "PA14-APARATOS")
    lz.txt(8.70, 5.20, "CASETA SOPLADORES (BLOWERS)", h=0.13, w_max=5.2)

    # 5. Laberinto de cloración / UV y Lecho de Secado de Lodos (Sur-Este)
    xd, yd, wd, hd = 12.20, 1.50, 4.80, 4.20
    lz.rect(xd, yd, wd, hd, "PA14-MUROS")
    for i in range(1, 4):
        xb = xd + i * (wd / 4)
        lz.lin(
            xb,
            yd + (0.20 if i % 2 else 0.85),
            xb,
            yd + hd - (0.85 if i % 2 else 0.20),
            "PA14-APARATOS",
        )
    lz.txt(xd + wd / 2, yd + hd + 0.35, "CONTACTO CLORO / UV", h=0.13, w_max=wd)

    xl, yl, wl, hl = 17.60, 1.50, 5.20, 4.20
    lz.rect(xl, yl, wl, hl, "PA14-MUROS")
    lz.lin(xl + wl / 2, yl, xl + wl / 2, yl + hl, "PA14-MUROS")
    lz.achurado(xl + 0.20, yl + 0.20, wl - 0.40, hl - 0.40, 0.50, "PA14-OBRAS-ARTE")
    lz.txt(xl + wl / 2, yl + hl + 0.35, "LECHO SECADO DE LODOS", h=0.13, w_max=wl)

    cotas_totales(lz, largo, ancho)
    return "T4 - PLANTA TRATAMIENTO AGUAS RESIDUALES PTAR MBBR (RNE OS.090)"


# ===================================================================== EDIF-17
def planta_edif_17(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-17 (5x4m): Trampas de Grasa Industriales en Paralelo con Pantallas Deflectoras."""
    cerco_malla(
        lz,
        largo,
        ancho,
        {"O": [Vano(ancho / 2, 1.40, "P", "izq", "out", "INSPECCION")]},
    )

    # Losa técnica y 2 cámaras desengrasadoras de concreto en paralelo (operación + limpieza)
    lz.rect(0.45, 0.35, largo - 0.90, ancho - 0.70, "PA14-OBRAS-ARTE")
    for k, nom_c in enumerate(("CAMARA 1 (OPERACION)", "CAMARA 2 (ALTERNA)")):
        yc = 0.55 + k * 1.55
        xc, wc, hc = 0.85, largo - 1.70, 1.35
        lz.rect(xc, yc, wc, hc, "PA14-MUROS")
        lz.rect(xc + 0.12, yc + 0.12, wc - 0.24, hc - 0.24, "PA14-APARATOS")
        # Pantallas deflectoras (baffles de retención de grasas flotantes)
        lz.lin(
            xc + wc * 0.30, yc + 0.12, xc + wc * 0.30, yc + hc - 0.12, "PA14-APARATOS"
        )
        lz.lin(
            xc + wc * 0.68, yc + 0.12, xc + wc * 0.68, yc + hc - 0.12, "PA14-APARATOS"
        )
        # Tapas circulares herméticas de registro
        lz.circ(xc + wc * 0.16, yc + hc / 2, 0.24, "PA14-SIMBOLOS")
        lz.circ(xc + wc * 0.50, yc + hc / 2, 0.28, "PA14-SIMBOLOS")
        lz.circ(xc + wc * 0.84, yc + hc / 2, 0.24, "PA14-SIMBOLOS")
        lz.txt(xc + wc * 0.50, yc + hc / 2, nom_c, h=0.10, w_max=wc - 0.4)

    # Cajas de registro de entrada (Cocina) y salida (hacia PTAR)
    lz.rect(0.20, ancho / 2 - 0.35, 0.55, 0.70, "PA14-APARATOS")
    lz.rect(largo - 0.75, ancho / 2 - 0.35, 0.55, 0.70, "PA14-APARATOS")
    lz.flecha(0.10, ancho / 2, 0.65, 0, "PA14-EJE")
    lz.flecha(largo - 0.70, ancho / 2, 0.65, 0, "PA14-EJE")

    cotas_totales(lz, largo, ancho)
    return "T4 - CAMARAS DESENGRASADORAS EN PARALELO PRE-PTAR (RNE IS.010)"


# ===================================================================== EDIF-32
def planta_edif_32(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-32 (18x10m): Planta Compacta Modular (2 Contenedores ISO 40' PTAP/PTAR + Tanque 40 m³)."""
    vol_res = float(eq.get("reservorio_m3", 40.0))
    h_agua = float(eq.get("altura_agua_m", 3.0))
    q_ptap = float(eq.get("caudal_ptap_lps", 2.0))
    q_ptar = float(eq.get("caudal_ptar_lps", 1.5))
    r_tanq = round(
        math.sqrt(vol_res / (math.pi * h_agua)) + 0.18, 2
    )  # ~2.24 m (D=4.48 m)

    cerco_malla(
        lz,
        largo,
        ancho,
        {"S": [Vano(4.20, 3.20, "PC", etiqueta="PORTON ACCESO SANEAMIENTO")]},
    )

    # 2 Módulos Contenerizados ISO 40 pies (11.20 x 2.44 m) sobre losas de concreto
    for idx, (yc, titulo, sub) in enumerate(
        [
            (
                ancho - 3.60,
                f"MODULO CONTENEDOR ISO 40' - PTAP COMPACTA ({q_ptap:.1f} L/s)",
                "FILTRACION MULTIMEDIA + ULTRAFILTRACION + CLORACION",
            ),
            (
                1.30,
                f"MODULO CONTENEDOR ISO 40' - PTAR MBBR COMPACTA ({q_ptar:.1f} L/s)",
                "BIORREACTOR AEROBICO MBBR + CLARIFICADOR + UV",
            ),
        ]
    ):
        xc, wc, hc = 1.00, 11.20, 2.44
        lz.rect(xc - 0.25, yc - 0.25, wc + 0.50, hc + 0.50, "PA14-OBRAS-ARTE")
        with lz.local(xc, yc, 0):
            cerramiento(
                lz,
                wc,
                hc,
                0.10,
                "PA14-MUROS",
                {"E": [Vano(hc / 2, 1.80, "P2", "izq", "out")]},
            )
        for k in range(3 if idx == 0 else 4):
            if idx == 0:
                lz.circ(xc + 1.80 + k * 2.20, yc + hc / 2, 0.65, "PA14-APARATOS")
            else:
                lz.rect(
                    xc + 0.80 + k * 2.40, yc + 0.30, 2.00, hc - 0.60, "PA14-APARATOS"
                )
        lz.txt(xc + wc / 2, yc + hc + 0.35, titulo, h=0.14, w_max=wc)
        lz.txt(xc + wc / 2, yc + hc / 2, sub, h=0.12, w_max=wc - 1.0)

    # Reservorio circular de Agua Potable de 40 m³ en el extremo Este
    xt, yt = largo - r_tanq - 1.15, ancho - r_tanq - 1.25
    tanque_vertical(lz, xt, yt, r_tanq, f"RESERVORIO {vol_res:.0f} m3", e_muro=0.18)

    # Caseta de presurización y tablero de control (Sur-Este)
    lz.rect(largo - 4.40, 1.10, 3.40, 2.40, "PA14-MUROS")
    lz.txt(largo - 2.70, 2.30, "BOMBAS Y TABLERO", h=0.12, w_max=3.1)

    cotas_totales(lz, largo, ancho)
    return "T4 - PLANTA SANEAMIENTO CONTENERIZADA PTAP/PTAR + TANQUE (RNE OS.020)"


# ===================================================================== EDIF-18
def planta_edif_18(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-18 (31x16m): Centro de Acopio Temporal CAT (7 celdas NTP 900.058 + Bodega Peligrosos)."""
    cerco_malla(
        lz,
        largo,
        ancho,
        {
            "S": [
                Vano(
                    largo * 0.35,
                    4.80,
                    "PC",
                    etiqueta="PORTON CAMION EPS-RS (RETIRO RESIDUOS)",
                )
            ]
        },
    )

    # 7 Celdas Modulares Techadas en la franja Norte según NTP 900.058-2019
    celdas = [
        ("1. MARRON", "ORGANICOS"),
        ("2. AMARILLO", "METALES"),
        ("3. AZUL", "PAPEL/CARTON"),
        ("4. BLANCO", "PLASTICOS"),
        ("5. VERDE", "VIDRIO"),
        ("6. NEGRO", "NO APROV."),
        ("7. ROJO", "PELIGROSOS"),
    ]
    x0, y0_c, w_tot, h_cel = 1.00, ancho - 6.80, largo - 2.00, 5.80
    w_c = w_tot / len(celdas)
    lz.rect(x0, y0_c, w_tot, h_cel, "PA14-MUROS")
    for i, (col_t, desc_t) in enumerate(celdas):
        xc = x0 + i * w_c
        if i > 0:
            tabique(lz, xc, y0_c, xc, y0_c + h_cel, esp=0.15, capa="PA14-MUROS")
        # Contenedores cilíndricos / cilindros 55 gal en cada celda
        for k in range(3):
            lz.circ(
                xc + 0.85 + k * ((w_c - 1.70) / 2),
                y0_c + h_cel - 1.25,
                0.38,
                "PA14-APARATOS",
            )
        lz.rect(xc + 0.45, y0_c + 1.40, w_c - 0.90, 1.80, "PA14-MOBILIARIO")
        lz.txt(xc + w_c / 2, y0_c + 0.90, col_t, h=0.15, w_max=w_c - 0.3)
        lz.txt(xc + w_c / 2, y0_c + 0.40, desc_t, h=0.13, w_max=w_c - 0.3)

    # Bodega Estanca de Residuos Peligrosos (Aceites Usados / Baterías) con Cubeto 110% (Sur-Este)
    xb, yb, wb, hb = largo - 10.50, 1.10, 9.50, 5.40
    with lz.local(xb, yb, 0):
        cerramiento(
            lz,
            wb,
            hb,
            0.18,
            "PA14-MUROS",
            {"O": [Vano(hb / 2, 1.80, "P2", "izq", "out", "BODEGA PELIGROSOS")]},
            achurar=True,
        )
    lz.rect(xb + 0.40, yb + 0.40, wb - 0.80, hb - 0.80, "PA14-OBRAS-ARTE")
    for ix in range(4):
        for iy in range(2):
            lz.circ(xb + 1.40 + ix * 1.85, yb + 1.35 + iy * 1.75, 0.38, "PA14-APARATOS")
    lz.txt(
        xb + wb / 2,
        yb + hb - 0.75,
        "CUBETO ESTANCO: ACEITES USADOS, BATERIAS Y TRAPOS CON HIDROCARBUROS",
        h=0.14,
        w_max=wb - 1.0,
    )

    # Caseta de Pesaje, Registro Ambiental y Ducha Lavaojos de Emergencia (Sur-Oeste)
    lz.rect(1.00, 1.10, 4.20, 3.20, "PA14-MUROS")
    escritorio(lz, 1.60, 1.50, 1.40, 0.65, 0)
    lz.txt(3.10, 3.65, "CONTROL Y REGISTRO CAT", h=0.13, w_max=3.8)
    lz.rect(5.80, 1.30, 2.20, 1.80, "PA14-APARATOS")
    lz.txt(6.90, 2.20, "BALANZA 2 TN", h=0.13, w_max=2.0)
    lz.txt(
        largo * 0.38,
        5.80,
        "PATIO PAVIMENTADO DE CARGA Y MANIOBRA CAMION EPS-RS",
        h=0.18,
        w_max=largo * 0.55,
    )

    cotas_totales(lz, largo, ancho)
    return "T4 - CENTRO DE ACOPIO TEMPORAL CAT NTP 900.058 (D.LEG. 1278)"


# ===================================================================== EDIF-19
def planta_edif_19(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-19 (15x10m): Trincheras de Compostaje Impermeabilizadas HDPE y Poza de Lixiviados."""
    n_tr = int(eq.get("n_trincheras", 3))
    cerco_malla(
        lz,
        largo,
        ancho,
        {"S": [Vano(3.20, 3.00, "PC", etiqueta="INGRESO CARRETILLAS / VOLTEO")]},
    )

    # 3 Trincheras longitudinales impermeabilizadas con geomembrana HDPE y espina de pescado
    x_tr_fin = largo - 4.40
    h_disp = ancho - 2.20
    h_tr = (h_disp - (n_tr - 1) * 0.65) / n_tr
    for i in range(n_tr):
        yt = 1.10 + i * (h_tr + 0.65)
        wt = x_tr_fin - 1.00
        lz.rect(1.00, yt, wt, h_tr, "PA14-MUROS")
        lz.rect(1.18, yt + 0.18, wt - 0.36, h_tr - 0.36, "PA14-OBRAS-ARTE")
        # Dren central de lixiviados en espina de pescado
        ym = yt + h_tr / 2
        lz.lin(1.30, ym, 1.00 + wt, ym, "PA14-APARATOS")
        for k in range(6):
            xk = 1.80 + k * ((wt - 1.60) / 6)
            lz.lin(xk - 0.35, yt + 0.30, xk, ym, "PA14-APARATOS")
            lz.lin(xk - 0.35, yt + h_tr - 0.30, xk, ym, "PA14-APARATOS")
        lz.txt(
            1.00 + wt / 2,
            ym,
            f"TRINCHERA COMPOSTAJE #{i + 1} (GEOMEMBRANA HDPE 1.5mm)",
            h=0.13,
            w_max=wt - 0.8,
        )

    # Poza estanca colectora de lixiviados (Sur-Este) y Cancha de Cribado/Humus (Norte-Este)
    xp = x_tr_fin + 0.55
    wp = largo - xp - 0.85
    lz.rect(xp, 1.10, wp, 3.60, "PA14-MUROS")
    lz.achurado(xp + 0.20, 1.30, wp - 0.40, 3.20, 0.40, "PA14-APARATOS")
    lz.txt(xp + wp / 2, 2.90, "POZA ESTANCA LIXIVIADOS", h=0.12, w_max=wp - 0.3)

    lz.rect(xp, 5.30, wp, ancho - 6.40, "PA14-OBRAS-ARTE")
    lz.puntos(xp + 0.30, 5.60, wp - 0.60, ancho - 7.00, 0.55, "PA14-RUMAS")
    lz.txt(
        xp + wp / 2,
        5.30 + (ancho - 6.40) / 2,
        "MADURACION Y HUMUS",
        h=0.12,
        w_max=wp - 0.3,
    )

    cotas_totales(lz, largo, ancho)
    return "T4 - PLANTA DE COMPOSTAJE Y MANEJO DE LODOS CON CERCO (D.LEG. 1278)"
