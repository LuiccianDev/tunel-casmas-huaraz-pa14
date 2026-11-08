"""Plataformas viales, playas de estacionamiento, garitas y casetas (EDIF-24..27, 36..38)."""

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
    inodoro,
    lavatorio,
    tabique,
    vehiculo,
)


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
