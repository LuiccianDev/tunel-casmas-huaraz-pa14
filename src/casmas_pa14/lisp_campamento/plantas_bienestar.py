"""Plantas arquitectónicas de bienestar, recreación SUM, lavandería y change-house (EDIF-12, 13, 22, 34, 35)."""

from __future__ import annotations

from .base import (
    Lienzo,
    Vano,
    cerramiento,
    columnas,
    cotas_totales,
    ducha,
    ejes,
    escritorio,
    estante,
    inodoro,
    lavatorio,
    lockers,
    mesa_sillas,
    tabique,
)
from .plantas_residencia import _vereda_perimetral


def planta_recreacion_sum(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-13 (25x16m) y EDIF-35 (15x8m): SUM/Cine, Salón de Juegos, Gimnasio y Cafetería/SSHH."""
    esp = 0.15
    x_mit = round(largo * 0.52, 2)
    y_mit = round(ancho * 0.50, 2)

    _vereda_perimetral(lz, largo, ancho)
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": [
                Vano(x_mit * 0.5, 1.60, "P2", "izq", "in", "INGRESO SUM"),
                Vano(x_mit + (largo - x_mit) * 0.5, 1.60, "V"),
            ],
            "N": [
                Vano(x_mit * 0.35, 1.60, "V"),
                Vano(x_mit * 0.75, 1.60, "V"),
                Vano(x_mit + (largo - x_mit) * 0.4, 1.40, "V"),
            ],
            "O": [Vano(y_mit * 0.5, 1.40, "V"), Vano(y_mit * 1.5, 1.40, "V")],
            "E": [Vano(y_mit * 0.5, 1.40, "P2", "izq", "out", "SALIDA GIMNASIO")],
        },
        achurar=True,
    )
    tabique(
        lz,
        x_mit,
        esp,
        x_mit,
        ancho - esp,
        [
            Vano(y_mit * 0.5, 1.20, "P2", "izq", "+"),
            Vano(y_mit * 1.5, 1.10, "P", "izq", "+"),
        ],
    )
    tabique(
        lz,
        esp,
        y_mit,
        largo - esp,
        y_mit,
        [
            Vano(x_mit * 0.5, 1.20, "P2", "izq", "+"),
            Vano(x_mit + (largo - x_mit) * 0.4, 0.90, "P", "izq", "+"),
        ],
    )

    # Cuadrante SO: Sala de Cine / TV Satelital / SUM con filas de butacas y pantalla
    lz.rect(esp + 0.15, esp + 0.60, 0.25, y_mit - esp - 1.20, "PA14-APARATOS")
    cols_b = 4 if largo >= 20 else 3
    filas_b = 4 if ancho >= 12 else 2
    for ix in range(cols_b):
        for iy in range(filas_b):
            xb = esp + 1.20 + ix * ((x_mit - 1.80) / cols_b)
            yb = esp + 0.55 + iy * ((y_mit - esp - 1.20) / filas_b)
            lz.rect(xb, yb, 0.55, 0.55, "PA14-MOBILIARIO")
    lz.txt(
        x_mit / 2,
        y_mit - 0.45,
        "AUDITORIO SUM / TV SATELITAL Y CINE",
        h=0.16,
        w_max=x_mit - 0.8,
    )

    # Cuadrante NO: Salón de Juegos (Mesa de Billar + Mesa de Ping-Pong)
    h_no = ancho - esp - y_mit
    w_bil, d_bil = min(2.40, x_mit * 0.36), min(1.30, h_no * 0.45)
    lz.rect(esp + 0.80, y_mit + (h_no - d_bil) / 2, w_bil, d_bil, "PA14-MOBILIARIO")
    lz.rect(
        esp + 0.92,
        y_mit + (h_no - d_bil) / 2 + 0.12,
        w_bil - 0.24,
        d_bil - 0.24,
        "PA14-MOBILIARIO",
    )
    lz.txt(
        esp + 0.80 + w_bil / 2, y_mit + h_no / 2, "BILLAR", h=0.13, w_max=w_bil - 0.3
    )

    x_pp = esp + 1.30 + w_bil
    w_pp, d_pp = min(2.50, x_mit - x_pp - 0.60), min(1.40, h_no * 0.48)
    lz.rect(x_pp, y_mit + (h_no - d_pp) / 2, w_pp, d_pp, "PA14-MOBILIARIO")
    lz.lin(
        x_pp + w_pp / 2,
        y_mit + (h_no - d_pp) / 2,
        x_pp + w_pp / 2,
        y_mit + (h_no + d_pp) / 2,
        "PA14-MOBILIARIO",
    )
    lz.txt(x_pp + w_pp / 2, y_mit + h_no / 2, "PING-PONG", h=0.13, w_max=w_pp - 0.3)
    lz.txt(
        x_mit / 2,
        ancho - esp - 0.45,
        "SALON DE JUEGOS Y ESPARCIMIENTO",
        h=0.16,
        w_max=x_mit - 0.8,
    )

    # Cuadrante SE: Gimnasio Equipado (Caminadoras, Bicicletas y Banco de Pesas)
    w_se = largo - esp - x_mit
    n_cam = 4 if largo >= 20 else 3
    for i in range(n_cam):
        xc = x_mit + 0.50 + i * ((w_se - 1.00) / n_cam)
        lz.rect(xc, esp + 0.40, 0.75, min(1.70, (y_mit - esp) * 0.45), "PA14-APARATOS")
        lz.rect(xc + 0.10, esp + 0.50, 0.55, 0.30, "PA14-APARATOS")
        lz.circ(xc + 0.38, y_mit - 0.85, 0.30, "PA14-APARATOS")
    lz.txt(
        x_mit + w_se / 2,
        y_mit - 0.35,
        "GIMNASIO Y MAQUINAS CARDIOVASCULARES",
        h=0.16,
        w_max=w_se - 0.6,
    )

    # Cuadrante NE: Cafetería / Lectura + Núcleo SSHH
    x_sh = x_mit + w_se * 0.60
    tabique(
        lz,
        x_sh,
        y_mit,
        x_sh,
        ancho - esp,
        [Vano(y_mit + h_no * 0.35, 0.80, "P", "izq", "+")],
    )
    lz.rect(
        x_mit + 0.40, ancho - esp - 0.65, (x_sh - x_mit) - 0.80, 0.50, "PA14-MOBILIARIO"
    )
    mesa_sillas(
        lz, x_mit + 0.70, y_mit + h_no * 0.28, min(1.60, (x_sh - x_mit) - 1.40), 0.75, 2
    )
    lz.txt(
        (x_mit + x_sh) / 2,
        y_mit + h_no - 0.95,
        "CAFETERIA Y LECTURA",
        h=0.14,
        w_max=(x_sh - x_mit) - 0.4,
    )

    for k in range(2):
        inodoro(lz, x_sh + 0.25 + k * 0.95, ancho - esp - 0.70, 180)
        lavatorio(lz, x_sh + 0.25 + k * 0.95, y_mit + 0.12, 0)
    lz.txt(
        (x_sh + largo - esp) / 2,
        y_mit + h_no / 2,
        "SS.HH.",
        h=0.14,
        w_max=(largo - esp - x_sh) - 0.3,
    )

    xs = [0.0, x_mit, x_sh, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - MODULO RECREATIVO, SUM, CINE Y GIMNASIO (DS 024)"


# =============================================================== EDIF-12 y 34
def planta_lavanderia(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-12 (10x8m) y EDIF-34 (7x6m): Lavandería Industrial (flujo Sucia -> Lavado -> Limpia)."""
    esp = 0.15
    x1 = round(largo * 0.30, 2)
    x2 = round(largo * 0.68, 2)
    y_mit = round(ancho / 2.0, 2)

    _vereda_perimetral(lz, largo, ancho)
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "O": [Vano(y_mit, 1.10, "P", "izq", "in", "INGRESO ROPA SUCIA")],
            "E": [Vano(y_mit, 1.10, "P", "izq", "out", "ENTREGA ROPA LIMPIA")],
            "S": [
                Vano((x1 + x2) / 2, 1.30, "V"),
                Vano((x2 + largo) / 2, 1.30, "VE", etiqueta="VENTANILLA"),
            ],
            "N": [
                Vano(x1 / 2, 1.10, "V"),
                Vano((x1 + x2) / 2, 1.40, "V"),
                Vano((x2 + largo) / 2, 1.10, "V"),
            ],
        },
        achurar=True,
    )
    tabique(lz, x1, esp, x1, ancho - esp, [Vano(y_mit, 1.00, "P", "izq", "+")])
    tabique(lz, x2, esp, x2, ancho - esp, [Vano(y_mit, 1.00, "P", "izq", "+")])

    # Zona 1 (Oeste): Recepción y clasificación de ropa térmica sucia + pozas de remojo
    for k in range(2):
        lz.rect(
            esp + 0.25,
            ancho - esp - 0.85 - k * 0.90,
            min(1.30, x1 - esp - 0.50),
            0.70,
            "PA14-APARATOS",
        )
    estante(lz, esp + 0.25, esp + 0.25, min(1.40, x1 - esp - 0.50), 0.55, 2)
    lz.txt(x1 / 2, y_mit, "CLASIFICACION ROPA SUCIA", h=0.13, w_max=x1 - 0.3)

    # Zona 2 (Centro): Batería de Lavadoras Centrífugas (Norte) y Secadoras Industriales (Sur)
    w_c = x2 - x1
    n_maq = 3 if largo >= 9.0 else 2
    paso_m = (w_c - 0.40) / n_maq
    wm = min(0.85, paso_m - 0.15)
    for i in range(n_maq):
        xm = x1 + 0.20 + i * paso_m + (paso_m - wm) / 2
        # Lavadora al Norte
        lz.rect(xm, ancho - esp - wm - 0.15, wm, wm, "PA14-APARATOS")
        lz.circ(xm + wm / 2, ancho - esp - wm / 2 - 0.15, wm * 0.34, "PA14-APARATOS")
        # Secadora al Sur
        lz.rect(xm, esp + 0.15, wm, wm, "PA14-APARATOS")
        lz.circ(xm + wm / 2, esp + 0.15 + wm / 2, wm * 0.34, "PA14-APARATOS")
    lz.txt((x1 + x2) / 2, y_mit + 0.35, "LAVADORAS IND.", h=0.13, w_max=w_c - 0.3)
    lz.txt((x1 + x2) / 2, y_mit - 0.35, "SECADORAS IND.", h=0.13, w_max=w_c - 0.3)

    # Zona 3 (Este): Planchado, doblado y estanterías de ropa limpia
    w_e = largo - esp - x2
    lz.rect(x2 + 0.30, y_mit - 0.35, min(1.50, w_e - 0.60), 0.70, "PA14-MOBILIARIO")
    estante(lz, x2 + 0.25, ancho - esp - 0.65, w_e - 0.50, 0.48, 3)
    lz.txt(x2 + w_e / 2, ancho - esp - 1.25, "ROPERIA LIMPIA", h=0.13, w_max=w_e - 0.3)
    lz.txt(x2 + w_e / 2, esp + 0.85, "PLANCHADO", h=0.12, w_max=w_e - 0.3)

    xs = [0.0, x1, x2, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - LAVANDERIA INDUSTRIAL Y ROPERIA TERMICA (RNE G.050)"


# ===================================================================== EDIF-22
def planta_change_house(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-22 (36x13m): Casa de Cambio (Zona Sucia -> Duchas -> Zona Limpia -> Lampistería)."""
    esp = 0.15
    n_lamp = int(eq.get("lamparas", 100))
    x1 = round(largo * 0.28, 2)  # Fin Zona Sucia (10.08 m)
    x2 = round(largo * 0.52, 2)  # Fin Núcleo Húmedo Duchas/SSHH (18.72 m)
    x3 = round(largo * 0.78, 2)  # Fin Zona Limpia (28.08 m)
    y_pas = 2.00

    _vereda_perimetral(lz, largo, ancho)
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "O": [
                Vano(
                    ancho / 2,
                    1.80,
                    "P2",
                    "izq",
                    "in",
                    "INGRESO GUARDIA DE MINA (SUCIO)",
                )
            ],
            "E": [
                Vano(
                    ancho / 2,
                    1.80,
                    "P2",
                    "izq",
                    "out",
                    "SALIDA HACIA PORTAL A (LIMPIO)",
                )
            ],
            "S": [
                Vano(x1 / 2, 1.80, "V"),
                Vano((x1 + x2) / 2, 1.40, "V"),
                Vano((x2 + x3) / 2, 1.80, "V"),
                Vano((x3 + largo) / 2, 2.20, "VE", etiqueta="VENTANILLA LAMPARAS"),
            ],
            "N": [
                Vano(x1 / 2, 1.80, "V"),
                Vano((x1 + x2) / 2, 1.40, "V"),
                Vano((x2 + x3) / 2, 1.80, "V"),
                Vano((x3 + largo) / 2, 1.60, "V"),
            ],
        },
        achurar=True,
    )
    for xd in (x1, x2, x3):
        tabique(
            lz,
            xd,
            esp,
            xd,
            ancho - esp,
            [Vano(ancho / 2, 1.50, "P2", "izq", "+")],
            esp=0.12,
            capa="PA14-MUROS",
        )
    lz.flecha(1.20, ancho / 2, largo - 2.40, 0, "PA14-EJE")

    # 1. Zona Sucia (Oeste): Lavabotas a presión + bancas y lockers de ropa de mina
    lz.rect(esp + 0.35, esp + 0.25, x1 - esp - 0.80, 0.70, "PA14-APARATOS")
    lz.txt(
        x1 / 2, esp + 1.25, "LAVABOTAS Y DESINFECCION DE EPPS", h=0.14, w_max=x1 - 0.8
    )
    for yb in (esp + 2.10, ancho - esp - 2.80):
        lockers(lz, esp + 0.60, yb, int((x1 - 1.60) // 0.45), rot=0, w=0.45, d=0.50)
        lz.rect(esp + 0.60, yb + 0.75, x1 - 1.60, 0.40, "PA14-MOBILIARIO")
    lz.txt(
        x1 / 2,
        ancho - esp - 0.65,
        "1. VESTUARIO ROPA DE MINA (ZONA SUCIA)",
        h=0.17,
        w_max=x1 - 0.6,
    )

    # 2. Núcleo Húmedo Central: 8 duchas calientes al Norte + 6 inodoros, urinarios y lavamanos al Sur
    w_sh = x2 - x1
    n_duch = 7
    paso_d = (w_sh - 0.60) / n_duch
    for i in range(n_duch):
        ducha(lz, x1 + 0.30 + i * paso_d, ancho - esp - 1.05, min(0.95, paso_d - 0.08))
        ducha(lz, x1 + 0.30 + i * paso_d, ancho / 2 + 1.10, min(0.95, paso_d - 0.08))
    for i in range(5):
        inodoro(lz, x1 + 0.45 + i * ((w_sh - 1.00) / 5), esp + 0.10, 0)
        lavatorio(lz, x1 + 0.45 + i * ((w_sh - 1.00) / 5), ancho / 2 - 1.45, 180)
    lz.txt(
        (x1 + x2) / 2,
        ancho / 2 + 0.45,
        "2. BATERIA DE DUCHAS TERMICAS E HIGIENE",
        h=0.16,
        w_max=w_sh - 0.5,
    )

    # 3. Zona Limpia: Lockers dobles de ropa civil y bancas calefaccionadas
    w_lim = x3 - x2
    for yb in (esp + 0.55, esp + 2.35, ancho - esp - 2.95, ancho - esp - 1.15):
        lockers(lz, x2 + 0.55, yb, int((w_lim - 1.10) // 0.45), rot=0, w=0.45, d=0.50)
    lz.txt(
        (x2 + x3) / 2,
        ancho / 2 - 0.45,
        "3. VESTUARIO ROPA CIVIL (ZONA LIMPIA)",
        h=0.17,
        w_max=w_lim - 0.6,
    )

    # 4. Lampistería y Control de Autorrescatadores (D.S. 024-2016-EM Art. 97)
    w_lmp = largo - esp - x3
    for yr in (ancho - esp - 1.10, ancho - esp - 2.45, ancho - esp - 3.80):
        estante(lz, x3 + 0.55, yr, w_lmp - 1.10, 0.65, 6)
    escritorio(lz, x3 + 0.70, esp + 0.85, w_lmp - 1.40, 0.70, 180)
    lz.txt(
        x3 + w_lmp / 2,
        ancho / 2 + y_pas * 0.2,
        f"4. LAMPISTERIA ({n_lamp} LAMPARAS + AUTORRESCATADORES)",
        h=0.15,
        w_max=w_lmp - 0.4,
    )

    xs = [0.0, x1, x2, x3, largo]
    ys = [0.0, ancho / 2, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - CHANGE-HOUSE Y LAMPISTERIA MINERA (DS 024 ART. 97)"
