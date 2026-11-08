"""Plantas industriales de talleres, almacenes, lavandería y change-house (EDIF-10..12, 22, 29, 33, 34)."""

from __future__ import annotations

from .base import (
    Lienzo,
    Vano,
    cerramiento,
    columnas,
    cotas_totales,
    ejes,
    escritorio,
    estante,
    tabique,
    vehiculo,
)


def planta_taller_mecanico(lz: Lienzo, largo: float, ancho: float, eq: dict) -> str:
    """EDIF-10 (25x15m, 3 bahías, tecle 15t) y EDIF-29 (20x10m, 2 bahías, tecle 5t)."""
    esp = 0.15
    n_bah = int(eq.get("n_bahias", 3 if largo >= 22 else 2))
    tecle_t = float(eq.get("tecle_t", 15.0 if largo >= 22 else 5.0))
    x_tall = round(largo * 0.74, 2)
    w_bah = (x_tall - esp) / n_bah
    y_mit = round(ancho / 2.0, 2)

    # Portones seccionales industriales en fachada Sur (uno por bahía)
    vanos_s: list[Vano] = []
    xs = [0.0]
    for i in range(n_bah):
        xb = esp + i * w_bah
        if i > 0:
            xs.append(round(xb, 3))
        w_port = min(4.20, w_bah * 0.72)
        vanos_s.append(
            Vano(xb + w_bah / 2, w_port, "PO", etiqueta=f"PORTON BAHIA {i + 1}")
        )
        # Rampa vehicular exterior de concreto por bahía
        lz.rect(xb + (w_bah - w_port) / 2, -1.20, w_port, 1.20, "PA14-OBRAS-ARTE")
    xs.extend([x_tall, largo])
    vanos_s.append(Vano((x_tall + largo) / 2, 1.20, "P", "izq", "in"))

    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": vanos_s,
            "N": [Vano(esp + (i + 0.5) * w_bah, 2.00, "V") for i in range(n_bah)]
            + [Vano((x_tall + largo) / 2, 1.50, "V")],
            "E": [Vano(y_mit * 0.5, 1.40, "V"), Vano(y_mit * 1.5, 1.40, "V")],
        },
        achurar=True,
    )
    tabique(
        lz,
        x_tall,
        esp,
        x_tall,
        ancho - esp,
        [
            Vano(y_mit * 0.5, 1.20, "P", "izq", "+"),
            Vano(y_mit * 1.5, 1.20, "P", "izq", "+"),
        ],
        esp=0.15,
        capa="PA14-MUROS",
    )
    tabique(lz, x_tall, y_mit, largo - esp, y_mit)

    # Rieles y viga testera de Puente Grúa / Tecle
    lz.lin(0.45, 0.75, x_tall - 0.35, 0.75, "PA14-ESTRUCTURA")
    lz.lin(0.45, ancho - 0.75, x_tall - 0.35, ancho - 0.75, "PA14-ESTRUCTURA")
    x_pg = x_tall * 0.46
    lz.rect(x_pg, 0.65, 1.10, ancho - 1.30, "PA14-ESTRUCTURA")
    lz.rect(x_pg + 0.15, ancho / 2 - 0.55, 0.80, 1.10, "PA14-APARATOS")
    lz.txt(
        x_pg + 0.55,
        ancho / 2,
        f"PUENTE GRUA / TECLE {tecle_t:.0f} TN",
        h=0.15,
        w_max=ancho - 2.5,
        ang=90,
    )

    # Bahías de mantenimiento con zanjas de inspección achuradas y maquinaria pesada
    nombres_eq = ["JUMBO 2 BRAZOS", "SCOOPTRAM 6 YD3", "VOLQUETE 20 M3"]
    for i in range(n_bah):
        xb = esp + i * w_bah
        if i > 0:
            lz.lin(xb, esp + 0.50, xb, ancho - esp - 0.50, "PA14-EJE")
        # Zanja de inspección mecánica con achurado y escalera de bajada
        w_z = min(1.30, w_bah * 0.24)
        l_z = ancho - 3.60
        xz, yz = xb + (w_bah - w_z) / 2, 1.80
        lz.rect(xz, yz, w_z, l_z, "PA14-OBRAS-ARTE")
        lz.achurado(xz, yz, w_z, l_z, 0.45, "PA14-OBRAS-ARTE")
        # Silueta de equipo pesado sobre la bahía
        w_v = min(2.50, w_bah * 0.52)
        l_v = min(8.20, ancho - 3.20)
        vehiculo(
            lz,
            xb + (w_bah - w_v) / 2,
            (ancho - l_v) / 2,
            w_v,
            l_v,
            nombres_eq[i % len(nombres_eq)],
            rot=0,
        )
        lz.txt(
            xb + w_bah / 2,
            ancho - 0.45,
            f"BAHIA {i + 1}: ZANJA INSPECCION",
            h=0.15,
            w_max=w_bah - 0.3,
        )

    # Nave lateral derecha: Maestranza/Soldadura/Prensado al Sur, Pañol/Compresores al Norte
    w_lat = largo - esp - x_tall
    estante(lz, x_tall + 0.30, esp + 0.25, w_lat - 0.60, 0.60, 3)
    estante(lz, largo - esp - 0.65, esp + 1.10, 0.50, y_mit - 1.60, 3)
    lz.txt(
        x_tall + w_lat / 2,
        y_mit * 0.52,
        "SOLDADURA Y PRENSADO MANGUERAS",
        h=0.14,
        w_max=w_lat - 0.4,
    )

    estante(lz, x_tall + 0.30, y_mit + 0.25, w_lat - 0.60, 0.55, 4)
    lz.circ(x_tall + 0.95, ancho - esp - 0.95, 0.45, "PA14-APARATOS")
    lz.circ(x_tall + 2.15, ancho - esp - 0.95, 0.45, "PA14-APARATOS")
    lz.txt(
        x_tall + 1.55, ancho - esp - 1.70, "COMPRESORES AIRE", h=0.12, w_max=w_lat - 0.4
    )
    lz.txt(
        x_tall + w_lat / 2,
        y_mit + (ancho - y_mit) * 0.38,
        "PANOL HERRAMIENTAS Y LUBRICANTES",
        h=0.14,
        w_max=w_lat - 0.4,
    )

    # Trampa exterior separadora de hidrocarburos API conectada por canaleta
    lz.rect(largo + 0.35, 0.80, 1.50, 2.80, "PA14-APARATOS")
    lz.lin(largo + 0.35, 1.70, largo + 1.85, 1.70, "PA14-APARATOS")
    lz.lin(largo + 0.35, 2.65, largo + 1.85, 2.65, "PA14-APARATOS")
    lz.txt(largo + 1.10, 2.20, "SEPARADOR API", h=0.12, w_max=2.4, ang=90)

    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "H", interiores=True)
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T2 - NAVE INDUSTRIAL APORTICADA DE ACERO (RNE A.060)"


# ===================================================================== EDIF-11
def planta_almacen_central(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-11 (15x10m): Almacén Central de Repuestos, Racks Selectivos y Cuarto NFPA 30."""
    esp = 0.15
    x_desp = round(largo * 0.24, 2)
    x_nfpa = round(largo * 0.74, 2)
    y_mit = round(ancho * 0.50, 2)

    # Plataforma de descarga en fachada Oeste
    lz.rect(-1.40, ancho * 0.22, 1.40, ancho * 0.56, "PA14-OBRAS-ARTE")
    lz.txt(-0.70, ancho / 2, "MUELLE CARGA", h=0.13, w_max=ancho * 0.5, ang=90)

    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "O": [Vano(ancho / 2, 2.80, "PO", etiqueta="PORTON MONTACARGAS")],
            "S": [
                Vano(x_desp / 2, 1.00, "P", "izq", "in", "PERSONAL"),
                Vano((x_desp + x_nfpa) / 2, 1.60, "V"),
                Vano((x_nfpa + largo) / 2, 1.20, "V"),
            ],
            "N": [
                Vano((x_desp + x_nfpa) / 2, 1.60, "V"),
                Vano((x_nfpa + largo) / 2, 1.20, "V"),
            ],
        },
        achurar=True,
    )
    tabique(
        lz,
        x_desp,
        esp,
        x_desp,
        ancho - esp,
        [Vano(y_mit, 2.20, "A"), Vano(esp + 1.20, 1.40, "VE")],
    )
    # Muro cortafuego hacia cuarto NFPA 30 de lubricantes e inflamables
    tabique(
        lz,
        x_nfpa,
        esp,
        x_nfpa,
        ancho - esp,
        [Vano(y_mit, 1.20, "P", "izq", "+")],
        esp=0.18,
        capa="PA14-MUROS",
        achurar=True,
    )

    # Zona Oeste: Recepción, Kardex y Mostrador de Despacho
    escritorio(lz, esp + 0.45, esp + 0.45, 1.40, 0.65, 0)
    estante(lz, esp + 0.30, ancho - esp - 0.70, x_desp - esp - 0.60, 0.50, 3)
    lz.txt(x_desp / 2, ancho - 1.40, "RECEPCION / KARDEX", h=0.14, w_max=x_desp - 0.4)

    # Zona Central: 4 filas de racks selectivos de carga pesada + pasillo central montacargas
    w_rack = (x_nfpa - x_desp) - 1.20
    for y_r in (esp + 0.35, esp + 1.85, ancho - esp - 2.65, ancho - esp - 1.15):
        estante(lz, x_desp + 0.60, y_r, w_rack, 0.80, 5)
    lz.txt(
        (x_desp + x_nfpa) / 2,
        y_mit,
        "PASILLO MONTACARGAS Y RACKS SELECTIVOS",
        h=0.16,
        w_max=w_rack,
    )

    # Zona Este: Bodega NFPA 30 con cubeto antiderrame y cilindros de 55 gal
    w_nf = largo - esp - x_nfpa
    lz.rect(
        x_nfpa + 0.25,
        esp + 0.25,
        w_nf - 0.50,
        ancho - 2 * esp - 0.50,
        "PA14-OBRAS-ARTE",
    )
    for ix in range(2):
        for iy in range(4):
            lz.circ(
                x_nfpa + 0.85 + ix * 1.10, esp + 0.90 + iy * 1.15, 0.32, "PA14-APARATOS"
            )
    estante(lz, largo - esp - 0.85, y_mit + 0.40, 0.55, ancho - esp - y_mit - 0.75, 3)
    lz.txt(x_nfpa + w_nf / 2, ancho - 0.70, "BODEGA NFPA 30", h=0.14, w_max=w_nf - 0.3)
    lz.txt(x_nfpa + w_nf / 2, 0.70, "CUBETO LUBRICANTES", h=0.12, w_max=w_nf - 0.3)

    xs = [0.0, x_desp, x_nfpa, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "H")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T2 - NAVE ALMACEN LOGISTICO Y BODEGA NFPA 30 (RNE A.060)"


# ===================================================================== EDIF-33
def planta_edif_33(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-33 (15x8m): Recinto Bifuncional (Área A 60% Bodega Crítica + Área B 40% CAT NTP 900.058)."""
    esp = 0.15
    x_div = round(largo * 0.58, 2)  # Muro cortafuego divisor
    y_mit = round(ancho / 2.0, 2)

    lz.rect(esp + 0.80, -1.00, 2.40, 1.00, "PA14-OBRAS-ARTE")
    lz.rect(x_div + 0.80, -1.00, 2.60, 1.00, "PA14-OBRAS-ARTE")
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": [
                Vano(esp + 2.00, 2.20, "PO", etiqueta="ACCESO BODEGA (AREA A)"),
                Vano(x_div + 2.10, 2.40, "PC", etiqueta="RETIRO EPS-RS (AREA B)"),
            ],
            "N": [
                Vano(x_div * 0.5, 1.60, "V"),
                Vano(x_div + (largo - x_div) * 0.5, 1.80, "V"),
            ],
        },
        achurar=True,
    )
    # Muro cortafuego macizo sin vano interior entre insumos y residuos
    tabique(
        lz, x_div, esp, x_div, ancho - esp, esp=0.20, capa="PA14-MUROS", achurar=True
    )

    # Área A (60% Izquierda): Racks de mangueras hidráulicas, sellos, brocas y mostrador
    escritorio(lz, x_div - 1.75, esp + 0.35, 1.35, 0.60, 0)
    estante(lz, esp + 0.35, ancho - esp - 0.85, x_div - esp - 0.70, 0.65, 5)
    estante(lz, esp + 0.35, y_mit - 0.30, x_div - esp - 2.30, 0.65, 4)
    for k in range(3):
        lz.circ(x_div - 0.65, y_mit + 0.40 + k * 0.75, 0.28, "PA14-APARATOS")
    lz.txt(
        x_div / 2,
        ancho - esp - 1.35,
        "AREA A: BODEGA DE INSUMOS CRITICOS Y REPUESTOS",
        h=0.15,
        w_max=x_div - 0.6,
    )

    # Área B (40% Derecha): 7 bahías de segregación NTP 900.058 + cubeto de peligrosos
    w_b = largo - esp - x_div
    colores_ntp = [
        "MARRON",
        "AMARILLO",
        "AZUL",
        "BLANCO",
        "VERDE",
        "NEGRO",
        "ROJO PELIG.",
    ]
    n_c = len(colores_ntp)
    w_cel = (w_b - 0.40) / n_c
    for i, col_nom in enumerate(colores_ntp):
        xc = x_div + 0.20 + i * w_cel
        lz.rect(xc + 0.04, ancho - esp - 2.30, w_cel - 0.08, 2.10, "PA14-TABIQUES")
        lz.circ(
            xc + w_cel / 2, ancho - esp - 1.25, min(0.28, w_cel * 0.32), "PA14-APARATOS"
        )
        lz.txt(xc + w_cel / 2, ancho - esp - 2.05, col_nom, h=0.09, w_max=w_cel - 0.06)
    # Balanza y cubeto estanco inferior
    lz.rect(x_div + 0.35, esp + 0.35, 1.30, 1.10, "PA14-APARATOS")
    lz.txt(x_div + 1.00, esp + 0.90, "BALANZA", h=0.11, w_max=1.2)
    lz.rect(largo - esp - 2.40, esp + 0.30, 2.10, 1.60, "PA14-OBRAS-ARTE")
    lz.txt(largo - esp - 1.35, esp + 1.10, "CUBETO ROJO", h=0.11, w_max=1.9)
    lz.txt(
        x_div + w_b / 2,
        y_mit - 0.35,
        "AREA B: ACOPIO RESIDUOS NTP 900.058",
        h=0.14,
        w_max=w_b - 0.4,
    )

    xs = [0.0, x_div, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "H")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T2 - NAVE BIFUNCIONAL CON MURO CORTAFUEGO (RNE A.060 / D.LEG. 1278)"
