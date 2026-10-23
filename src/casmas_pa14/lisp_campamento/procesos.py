"""Plantas civiles, sanitarias, energéticas, viales y de seguridad (EDIF-14..21, 23..28, 30..32, 36..38).

Representa fielmente cada tipología constructiva:
- T2: Casas de fuerza aporticadas (EDIF-20, 31).
- T3: Plataformas viales abiertas, playas de parqueo, patio de maquinaria y balanza (EDIF-24, 25, 26, 27).
- T4: Plantas sanitarias, residuos e hidrocarburos con cerco de malla olímpica (EDIF-14..19, 21, 30, 32).
- T5: Polvorines SUCAMEC con parapeto de tierra y casetas blindadas (EDIF-23, 28, 37, 38).
"""

from __future__ import annotations

import math

from .base import (
    Lienzo,
    Vano,
    cerco_malla,
    cerramiento,
    columnas,
    cotas_totales,
    ejes,
    escritorio,
    estante,
    grupo_electrogeno,
    inodoro,
    lavatorio,
    tabique,
    tanque_vertical,
    vehiculo,
)


# ===================================================================== EDIF-14
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


# =============================================================== EDIF-20 y 31
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


# ===================================================================== EDIF-24
def planta_edif_24(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-24 (10x6m): Plataforma de Balanza Camionera 80 t + Caseta de Control y Torniquete."""
    bal_t = float(eq.get("balanza_t", 80.0))

    # Bordillo perimetral de plataforma vial (T3: sin muros de edificio alrededor del lote)
    lz.rect(0.0, 0.0, largo, ancho, "PA14-OBRAS-ARTE")
    lz.rect(-0.25, -0.25, largo + 0.50, ancho + 0.50, "PA14-OBRAS-ARTE")

    # 1. Mitad Sur (Y = 0.25 .. 3.35 m): Plataforma de Balanza Camionera Electrónica 80 t
    xb, yb, wb, hb = 0.90, 0.30, largo - 1.80, 3.00
    lz.rect(xb, yb, wb, hb, "PA14-ESTRUCTURA")
    lz.rect(xb + 0.15, yb + 0.15, wb - 0.30, hb - 0.30, "PA14-APARATOS")
    # Rampas de aproximación Oeste y Este + 6 celdas de carga (load cells)
    lz.rect(0.0, yb, xb, hb, "PA14-OBRAS-ARTE")
    lz.rect(xb + wb, yb, xb, hb, "PA14-OBRAS-ARTE")
    for xc_i in (xb + 0.35, xb + wb / 2, xb + wb - 0.35):
        lz.circ(xc_i, yb + 0.30, 0.16, "PA14-SIMBOLOS")
        lz.circ(xc_i, yb + hb - 0.30, 0.16, "PA14-SIMBOLOS")
    # Barrera articulada (tranquera) en extremo Este y silueta de camión en pesaje
    lz.rect(largo - 0.55, yb + hb - 0.25, 0.35, 0.35, "PA14-ESTRUCTURA")
    lz.lin(largo - 0.40, yb + hb - 0.10, largo - 0.40, yb + 0.20, "PA14-PUERTAS")
    vehiculo(
        lz,
        xb + 0.60,
        yb + 0.35,
        2.30,
        wb - 1.20,
        f"BALANZA ELECTRONICA {bal_t:.0f} TN",
        rot=270,
    )
    lz.flecha(0.15, yb + hb / 2, 0.70, 0, "PA14-EJE")

    # 2. Mitad Norte (Y = 3.55 .. 5.75 m): Caseta de Control y Pesaje + Torniquete Peatonal
    xg, yg, wg, hg = 0.60, 3.55, 6.20, 2.20
    with lz.local(xg, yg, 0):
        cerramiento(
            lz,
            wg,
            hg,
            0.15,
            "PA14-MUROS",
            {
                "S": [Vano(wg * 0.38, 2.20, "V", etiqueta="VISOR PESAJE")],
                "E": [Vano(hg / 2, 0.85, "P", "izq", "in")],
                "N": [Vano(wg * 0.35, 1.40, "V")],
            },
            achurar=True,
        )
        # Baño de guardia en esquina NO de la caseta
        x_sh = wg - 1.65
        tabique(
            lz, x_sh, 0.15, x_sh, hg - 0.15, [Vano(hg * 0.35, 0.65, "P", "izq", "+")]
        )
        inodoro(lz, wg - 0.60, hg - 0.80, 180)
        lavatorio(lz, x_sh + 0.10, hg - 0.58, 90)
        escritorio(lz, 0.55, 0.25, 1.50, 0.60, 0)
        lz.txt(
            x_sh / 2, hg - 0.45, "CASETA VIGILANCIA Y PESAJE", h=0.14, w_max=x_sh - 0.3
        )

    # Pasillo peatonal con torniquete bidireccional y arco detector (Este-Norte)
    xt, yt, wt, ht = 7.20, 3.55, 2.40, 2.20
    lz.rect(xt, yt, wt, ht, "PA14-OBRAS-ARTE")
    lz.circ(xt + wt / 2, yt + ht / 2, 0.42, "PA14-APARATOS")
    lz.lin(
        xt + wt / 2 - 0.42,
        yt + ht / 2,
        xt + wt / 2 + 0.42,
        yt + ht / 2,
        "PA14-APARATOS",
    )
    lz.lin(
        xt + wt / 2,
        yt + ht / 2 - 0.42,
        xt + wt / 2,
        yt + ht / 2 + 0.42,
        "PA14-APARATOS",
    )
    lz.txt(xt + wt / 2, yt + ht - 0.30, "TORNIQUETE PEATONAL", h=0.11, w_max=wt - 0.2)

    cotas_totales(lz, largo, ancho)
    return "T3 - ESTACION DE PESAJE CAMIONERO 80 TN Y GARITA DE CONTROL (RNE G.050)"


# ===================================================================== EDIF-25
def planta_edif_25(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-25 (40x20m): Playa Abierta de Vehículos Livianos (20 camionetas 4x4) y 4 Buses."""
    n_liv = int(eq.get("cajones_livianos", 20))
    n_bus = int(eq.get("bahias_buses", 4))

    # Bordillo perimetral y cuneta pluvial achurada con aberturas viales en Oeste y Este
    lz.rect(-0.45, -0.45, largo + 0.90, ancho + 0.90, "PA14-OBRAS-ARTE")
    lz.achurado(-0.45, -0.45, largo + 0.90, 0.45, 0.45, "PA14-OBRAS-ARTE")
    lz.achurado(-0.45, ancho, largo + 0.90, 0.45, 0.45, "PA14-OBRAS-ARTE")
    lz.rect(0.0, 0.0, largo, ancho, "PA14-CONTORNO")

    x_zona_bus = 26.50  # Oeste (0..26.5m): 20 cajones camionetas | Este (26.5..40m): 4 bahías buses

    # Eje vial central con flechas de circulación y radio de giro
    lz.lin(0.0, ancho / 2, largo, ancho / 2, "PA14-EJE")
    lz.flecha(2.0, ancho / 2 - 1.5, 4.0, 0, "PA14-EJE")
    lz.flecha(18.0, ancho / 2 + 1.5, 4.0, 180, "PA14-EJE")
    lz.txt(
        x_zona_bus / 2,
        ancho / 2,
        "CALLE DE CIRCULACION VEHICULAR DOBLE SENTIDO (A=8.00 m - RNE A.010 CAP. X)",
        h=0.20,
        w_max=x_zona_bus - 2.0,
    )

    # 20 Cajones de Camionetas 4x4 (10 al Sur + 10 al Norte, de 2.50 x 5.00 m cada uno)
    caj_por_fila = n_liv // 2
    w_caj = 2.50
    l_caj = 5.00
    x0_caj = 0.80
    for i in range(caj_por_fila):
        xc = x0_caj + i * w_caj
        # Fila Sur (y = 0.60 .. 5.60 m) con tope de llanta (wheel stop)
        lz.rect(xc, 0.60, w_caj, l_caj, "PA14-OBRAS-ARTE")
        lz.rect(xc + 0.35, 0.95, w_caj - 0.70, 0.18, "PA14-ESTRUCTURA")
        if i % 2 == 0:
            vehiculo(lz, xc + 0.30, 1.25, 1.90, 4.20, f"4x4 C-{i + 1:02d}", rot=0)
        else:
            lz.txt(
                xc + w_caj / 2,
                3.10,
                f"C-{i + 1:02d}\n2.5x5m",
                h=0.14,
                w_max=w_caj - 0.3,
            )

        # Fila Norte (y = 14.40 .. 19.40 m) con tope de llanta
        idx_n = caj_por_fila + i + 1
        lz.rect(xc, ancho - 0.60 - l_caj, w_caj, l_caj, "PA14-OBRAS-ARTE")
        lz.rect(xc + 0.35, ancho - 1.13, w_caj - 0.70, 0.18, "PA14-ESTRUCTURA")
        if i % 2 == 1:
            vehiculo(
                lz,
                xc + 0.30,
                ancho - 0.60 - l_caj + 0.15,
                1.90,
                4.20,
                f"4x4 C-{idx_n:02d}",
                rot=180,
            )
        else:
            lz.txt(
                xc + w_caj / 2,
                ancho - 3.10,
                f"C-{idx_n:02d}\n2.5x5m",
                h=0.14,
                w_max=w_caj - 0.3,
            )

    # 4 Bahías de Buses de Personal (3.50 x 12.00 m) en el sector Este
    w_b, l_b = 12.00, 3.50
    xb_0 = largo - w_b - 0.80
    for k in range(n_bus):
        yb = 0.90 + k * 4.65
        lz.rect(xb_0, yb, w_b, l_b, "PA14-OBRAS-ARTE")
        vehiculo(
            lz,
            xb_0 + 0.50,
            yb + 0.45 + 2.60,
            2.60,
            11.00,
            f"BUS PERSONAL B-0{k + 1} (3.5x12m)",
            rot=270,
        )

    # Vereda peatonal segura hacia el campamento (borde Sur)
    lz.txt(
        largo / 2,
        -0.95,
        "CUNETA PLUVIAL PERIMETRAL Y SARDINEL DE CONCRETO (SIN MUROS DE EDIFICIO)",
        h=0.16,
        w_max=largo,
    )
    cotas_totales(lz, largo, ancho, sep=3.0)
    return "T3 - PLAYA ABIERTA DE ESTACIONAMIENTO LIVIANOS Y BUSES (RNE A.010)"


# ===================================================================== EDIF-26
def planta_edif_26(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-26 (50x30m): Patio Abierto de Maquinaria Pesada, Radio Giro 15 m y Losa de Lavado."""
    n_volq = int(eq.get("bahias_volquetes", 6))
    n_eq = int(eq.get("bahias_equipos", 4))

    # Plataforma estabilizada con cuneta perimetral achurada (sin muros cerrados)
    lz.rect(-0.60, -0.60, largo + 1.20, ancho + 1.20, "PA14-OBRAS-ARTE")
    lz.achurado(-0.60, -0.60, largo + 1.20, 0.60, 0.50, "PA14-OBRAS-ARTE")
    lz.achurado(-0.60, ancho, largo + 1.20, 0.60, 0.50, "PA14-OBRAS-ARTE")
    lz.rect(0.0, 0.0, largo, ancho, "PA14-CONTORNO")

    x_wash = (
        largo - 11.50
    )  # Sector Este: Losa de lavado a presión (Wash Pad) + Desarenador

    # Círculo de radio de giro mínimo R = 7.50 m (D = 15.0 m) en patio central
    lz.lin(0.0, ancho / 2, x_wash, ancho / 2, "PA14-EJE")
    lz.circ(x_wash * 0.50, ancho / 2, 5.00, "PA14-EJE")
    lz.flecha(2.50, ancho / 2 - 2.20, 5.00, 0, "PA14-EJE")
    lz.flecha(x_wash - 3.50, ancho / 2 + 2.20, 5.00, 180, "PA14-EJE")
    lz.txt(
        x_wash * 0.50,
        ancho / 2,
        "PATIO DE MANIOBRAS AFIRMADO E=0.30m (GIRO LIBRE D=15.0 m - MTC EG-2013 SEC. 104)",
        h=0.22,
        w_max=x_wash - 4.0,
    )

    # Franja Sur: 6 Bahías para Volquetes Mineros 20 m³ (4.50 x 9.00 m)
    paso_v = (x_wash - 1.60) / n_volq
    wv_b = min(4.60, paso_v - 0.40)
    for i in range(n_volq):
        xb = 0.80 + i * paso_v + (paso_v - wv_b) / 2
        lz.rect(xb, 0.80, wv_b, 8.80, "PA14-OBRAS-ARTE")
        vehiculo(
            lz,
            xb + (wv_b - 2.60) / 2,
            1.30,
            2.60,
            7.80,
            f"VOLQUETE 20m3 V-0{i + 1}",
            rot=0,
        )

    # Franja Norte: 4 Bahías Anchas para Equipos de Tunelería (Jumbo, Scooptram, Mixer, Scaler)
    equipos_tunel = [
        "JUMBO 2 BRAZOS",
        "SCOOPTRAM LHD 6 YD3",
        "MIXER BAJO PERFIL",
        "SCALER / TELEHANDLER",
    ]
    paso_e = (x_wash - 1.60) / n_eq
    we_b = min(6.20, paso_e - 0.60)
    for i in range(n_eq):
        xb = 0.80 + i * paso_e + (paso_e - we_b) / 2
        lz.rect(xb, ancho - 9.60, we_b, 8.80, "PA14-OBRAS-ARTE")
        vehiculo(
            lz,
            xb + (we_b - 2.70) / 2,
            ancho - 9.10,
            2.70,
            7.80,
            equipos_tunel[i % len(equipos_tunel)],
            rot=180,
        )

    # Sector Este: Losa de Lavado de Maquinaria (Wash Pad) + Canaleta Desarenadora + Trampa API
    xw, yw, ww, hw = x_wash + 0.60, 1.20, 10.00, ancho - 7.20
    lz.rect(xw, yw, ww, hw, "PA14-MUROS")
    lz.achurado(xw + 0.30, yw + 0.30, ww - 0.60, hw - 0.60, 0.80, "PA14-OBRAS-ARTE")
    lz.txt(
        xw + ww / 2,
        yw + hw / 2,
        "LOSA DE LAVADO A PRESION (WASH PAD)",
        h=0.20,
        w_max=ww - 0.8,
    )

    # Desarenador y Trampa de Grasas e Hidrocarburos al Norte-Este
    lz.rect(xw, ancho - 5.20, ww, 4.00, "PA14-MUROS")
    lz.lin(xw + ww / 2, ancho - 5.20, xw + ww / 2, ancho - 1.20, "PA14-APARATOS")
    lz.txt(xw + ww * 0.25, ancho - 3.20, "DESARENADOR", h=0.15, w_max=ww * 0.45)
    lz.txt(
        xw + ww * 0.75, ancho - 3.20, "TRAMPA HIDROCARBUROS", h=0.15, w_max=ww * 0.45
    )

    cotas_totales(lz, largo, ancho, sep=3.2)
    return "T3 - PATIO ABIERTO DE MAQUINARIA PESADA Y WASH PAD (MTC EG-2013)"


# ===================================================================== EDIF-27
def planta_edif_27(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-27 (20x20m): Playa de Estacionamiento y Parqueo Auxiliar Satélite (Portal B)."""
    n_liv = int(eq.get("cajones_livianos", 8))

    lz.rect(-0.40, -0.40, largo + 0.80, ancho + 0.80, "PA14-OBRAS-ARTE")
    lz.achurado(-0.40, -0.40, largo + 0.80, 0.40, 0.45, "PA14-OBRAS-ARTE")
    lz.rect(0.0, 0.0, largo, ancho, "PA14-CONTORNO")

    # Calle central de maniobra (Y = 6.00 .. 12.60 m)
    lz.lin(0.0, 9.30, largo, 9.30, "PA14-EJE")
    lz.flecha(1.50, 8.20, 3.20, 0, "PA14-EJE")
    lz.flecha(largo - 1.50, 10.40, 3.20, 180, "PA14-EJE")
    lz.txt(
        largo / 2,
        9.30,
        "VIA DE CIRCULACION Y MANIOBRA PORTAL B (A=6.60 m)",
        h=0.18,
        w_max=largo - 2.0,
    )

    # Franja Sur: 8 Cajones de Camionetas 4x4 de Supervisión (2.35 x 5.00 m)
    w_c = (largo - 1.20) / n_liv
    for i in range(n_liv):
        xc = 0.60 + i * w_c
        lz.rect(xc, 0.60, w_c, 5.00, "PA14-OBRAS-ARTE")
        lz.rect(xc + 0.25, 0.90, w_c - 0.50, 0.16, "PA14-ESTRUCTURA")
        if i % 2 == 0:
            vehiculo(
                lz, xc + (w_c - 1.80) / 2, 1.20, 1.80, 4.10, f"4x4 S-{i + 1:02d}", rot=0
            )
        else:
            lz.txt(xc + w_c / 2, 3.10, f"S-{i + 1:02d}", h=0.14, w_max=w_c - 0.2)

    # Franja Norte: 2 Bahías de Minibuses de Guardia + 3 Bahías de Equipo Pesado Auxiliar
    bahias_n = [
        ("MINIBUS GUARDIA 1", 3.40),
        ("MINIBUS GUARDIA 2", 3.40),
        ("VOLQUETE AUX.", 3.80),
        ("CARGADOR LHD", 3.80),
        ("TELEHANDLER", 3.60),
    ]
    x_cur = 0.60
    for nom_b, wb in bahias_n:
        lz.rect(x_cur, ancho - 7.00, wb, 6.40, "PA14-OBRAS-ARTE")
        vehiculo(lz, x_cur + (wb - 2.20) / 2, ancho - 6.60, 2.20, 5.60, nom_b, rot=180)
        x_cur += wb + 0.20

    cotas_totales(lz, largo, ancho)
    return "T3 - PLAYA ABIERTA DE ESTACIONAMIENTO Y PARQUEO AUXILIAR (RNE A.010)"


# ===================================================================== EDIF-36
def planta_edif_36(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-36 (6x5m): Garita de Control de Acceso y Lampistería Satélite (40 lámparas)."""
    esp = 0.15
    n_lamp = int(eq.get("lamparas", 40))
    lz.rect(-0.65, -0.65, largo + 1.30, ancho + 1.30, "PA14-OBRAS-ARTE")

    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": [
                Vano(1.80, 1.80, "V", etiqueta="VENTANAL CONTROL"),
                Vano(largo - 1.15, 0.90, "P", "izq", "in", "INGRESO"),
            ],
            "E": [Vano(ancho * 0.55, 1.50, "VE", etiqueta="ENTREGA LAMPARAS")],
            "N": [Vano(largo * 0.60, 1.40, "V")],
        },
        achurar=True,
    )

    # Baño integrado en esquina NO (1.65 x 1.75 m)
    w_sh, h_sh = 1.65, 1.75
    y_sh = ancho - esp - h_sh
    tabique(lz, esp + w_sh, y_sh, esp + w_sh, ancho - esp)
    tabique(
        lz,
        esp,
        y_sh,
        esp + w_sh,
        y_sh,
        [Vano(esp + w_sh * 0.55, 0.65, "P", "izq", "-")],
    )
    inodoro(lz, esp + 0.15, ancho - esp - 0.70, 180)
    lavatorio(lz, esp + w_sh - 0.58, ancho - esp - 0.50, 180)
    lz.txt(esp + w_sh / 2, y_sh + 0.45, "SS.HH.", h=0.10, w_max=w_sh - 0.2)

    # Rack cargador de 40 lámparas mineras y autorrescatadores al Norte-Este
    x_rk = esp + w_sh + 0.25
    estante(lz, x_rk, ancho - esp - 0.65, largo - esp - x_rk - 0.20, 0.55, 4)
    estante(lz, largo - esp - 0.65, 1.20, 0.50, 2.20, 3)
    lz.txt(
        (x_rk + largo - esp) / 2,
        ancho - esp - 1.05,
        f"RACK {n_lamp} LAMPARAS Y AUTORRESCATADORES",
        h=0.11,
        w_max=(largo - esp - x_rk) - 0.2,
    )

    # Escritorio de vigilancia y control de acceso frente al ventanal Sur
    escritorio(lz, esp + 0.45, esp + 0.25, 1.50, 0.60, 0)
    lz.txt(
        largo * 0.45, ancho * 0.42, "CONTROL ACCESO PORTAL B", h=0.13, w_max=largo - 1.6
    )

    xs, ys = [0.0, largo], [0.0, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - GARITA DE CONTROL Y LAMPISTERIA SATELITE (DS 024 ART. 97)"


# =============================================================== EDIF-37 y 38
def planta_caseta_polvorin(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-37 y EDIF-38 (4x3m = 12 m²): Caseta Blindada de Custodia Armada 24/7 de Polvorín."""
    esp = 0.20  # Muro blindado de concreto armado
    lz.rect(-0.55, -0.55, largo + 1.10, ancho + 1.10, "PA14-OBRAS-ARTE")

    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": [
                Vano(1.15, 0.85, "P", "izq", "in", "PUERTA BLINDADA"),
                Vano(2.85, 1.00, "V", etiqueta="TRONERA SUR"),
            ],
            "N": [Vano(2.75, 1.20, "V")],
            "E": [Vano(ancho / 2, 1.10, "V")],
            "O": [Vano(0.90, 0.70, "V")],
        },
        achurar=True,
    )

    # Baño compacto de guardia en esquina NO (1.30 x 1.25 m)
    w_sh, h_sh = 1.30, 1.25
    y_sh = ancho - esp - h_sh
    tabique(lz, esp + w_sh, y_sh, esp + w_sh, ancho - esp)
    tabique(
        lz,
        esp,
        y_sh,
        esp + w_sh,
        y_sh,
        [Vano(esp + w_sh * 0.55, 0.60, "P", "izq", "-")],
    )
    inodoro(lz, esp + 0.12, ancho - esp - 0.68, 180)
    lavatorio(lz, esp + w_sh - 0.55, ancho - esp - 0.46, 180)
    lz.txt(esp + w_sh / 2, y_sh + 0.32, "SS.HH.", h=0.09, w_max=w_sh - 0.2)

    # Consola de monitoreo CCTV / Radio VHF en esquina NE
    escritorio(lz, esp + w_sh + 0.30, ancho - esp - 1.20, 1.35, 0.55, 180)
    lz.txt(
        esp + w_sh + 0.98, ancho - esp - 1.55, "CONSOLA CCTV / RADIO", h=0.10, w_max=1.8
    )

    # Armero metálico SUCAMEC en esquina SE
    estante(lz, largo - esp - 0.85, esp + 0.12, 0.75, 0.45, 2)
    lz.txt(largo - esp - 0.48, esp + 0.75, "ARMERO", h=0.09, w_max=0.9)

    cotas_totales(lz, largo, ancho)
    return "T5 - CASETA BLINDADA DE CUSTODIA ARMADA 24/7 (SUCAMEC LEY 30299)"
