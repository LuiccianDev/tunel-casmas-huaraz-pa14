"""Plantas arquitectónicas de servicios, comedores, oficinas, tópico y recreación (EDIF-04..09, 13, 35)."""

from __future__ import annotations

from .base import (
    Lienzo,
    Vano,
    cama,
    cerramiento,
    columnas,
    cotas_totales,
    ejes,
    escritorio,
    estante,
    inodoro,
    lavatorio,
    mesa_sillas,
    tabique,
    urinario,
    vehiculo,
)
from .plantas_residencia import _vereda_perimetral


def planta_comedor(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-04 y EDIF-05: Comedor, Línea de Autoservicio, Cocina Industrial y Cámaras de Frío."""
    esp = 0.15
    x_coc = round(largo * 0.60, 2)
    x_alm = round(largo * 0.82, 2)
    y_mit = round(ancho * 0.50, 2)

    _vereda_perimetral(lz, largo, ancho)
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "O": [Vano(ancho / 2, 1.60, "P2", "izq", "in", "ACCESO COMENSALES")],
            "S": [
                Vano(x_coc * 0.30, 1.60, "V"),
                Vano(x_coc * 0.70, 1.60, "V"),
                Vano((x_coc + x_alm) / 2, 1.20, "V"),
            ],
            "N": [
                Vano(x_coc * 0.30, 1.60, "V"),
                Vano(x_coc * 0.70, 1.60, "V"),
                Vano((x_coc + x_alm) / 2, 1.20, "V"),
            ],
            "E": [Vano(ancho * 0.25, 1.40, "P2", "izq", "out", "CARGA INSUMOS")],
        },
        achurar=True,
    )

    # Lavamanos de ingreso (NTS 142-MINSA)
    for k in range(3):
        lavatorio(lz, esp + 0.35 + k * 0.65, esp + 0.05, 0)
    lz.txt(esp + 1.15, esp + 0.75, "LAVAMANOS", h=0.12, w_max=2.0)

    # Mesas de comedor con sillas individuales
    cols_m = 3 if x_coc >= 9.0 else 2
    filas_m = 3 if ancho >= 11.0 else 2
    w_mesa, d_mesa = (1.60, 0.80) if largo >= 14.0 else (1.30, 0.75)
    paso_x = (x_coc - 2.40) / cols_m
    paso_y = (ancho - 2.20) / filas_m
    for ix in range(cols_m):
        for iy in range(filas_m):
            xm = 1.00 + ix * paso_x + (paso_x - w_mesa) / 2
            ym = 1.10 + iy * paso_y + (paso_y - d_mesa) / 2
            mesa_sillas(lz, xm, ym, w_mesa, d_mesa, por_lado=3 if w_mesa >= 1.5 else 2)
    lz.txt(
        x_coc * 0.45,
        ancho - 0.55,
        "SALON COMEDOR CALEFACCIONADO (RNE A.070)",
        h=0.18,
        w_max=x_coc - 1.5,
    )

    # Línea de autoservicio (Baño María + barra deslizable) y tabique a cocina
    lz.rect(x_coc - 1.15, 1.20, 0.75, ancho - 2.40, "PA14-APARATOS")
    lz.rect(x_coc - 1.40, 1.20, 0.25, ancho - 2.40, "PA14-MOBILIARIO")
    lz.txt(
        x_coc - 0.78,
        ancho / 2,
        "LINEA AUTOSERVICIO / BUFFET",
        h=0.14,
        w_max=ancho - 2.8,
        ang=90,
    )
    tabique(
        lz,
        x_coc,
        esp,
        x_coc,
        ancho - esp,
        [
            Vano(0.85, 0.90, "P", "izq", "+"),
            Vano(ancho / 2, max(2.0, ancho - 3.6), "VE"),
        ],
        esp=0.12,
        capa="PA14-MUROS",
    )

    # Cocina caliente: isla central con campana extractora, marmitas y lavadero 3 pozas
    w_coc = x_alm - x_coc
    x_isla = x_coc + w_coc * 0.22
    w_isla = w_coc * 0.56
    h_isla = ancho * 0.42
    lz.rect(x_isla, (ancho - h_isla) / 2, w_isla, h_isla, "PA14-APARATOS")
    lz.lin(
        x_isla,
        (ancho - h_isla) / 2,
        x_isla + w_isla,
        (ancho + h_isla) / 2,
        "PA14-APARATOS",
    )
    lz.lin(
        x_isla,
        (ancho + h_isla) / 2,
        x_isla + w_isla,
        (ancho - h_isla) / 2,
        "PA14-APARATOS",
    )
    for k in range(2):
        lz.circ(
            x_isla + w_isla * (0.30 + 0.40 * k),
            ancho / 2,
            min(0.28, w_isla * 0.16),
            "PA14-APARATOS",
        )
    lz.txt(
        x_isla + w_isla / 2,
        ancho - 0.60,
        "COCINA INDUSTRIAL + CAMPANA",
        h=0.14,
        w_max=w_coc - 0.3,
    )
    # Lavadero de 3 pozas inox al Sur
    lz.rect(x_coc + 0.30, esp + 0.08, min(1.80, w_coc - 0.60), 0.60, "PA14-APARATOS")
    lz.txt(x_coc + w_coc / 2, esp + 0.95, "LAVADERO 3 POZAS", h=0.11, w_max=w_coc - 0.4)

    # Franja Este (18%): Cámaras frigoríficas (-18C / +4C) al Norte y Despensa Seca al Sur
    tabique(
        lz,
        x_alm,
        esp,
        x_alm,
        ancho - esp,
        [
            Vano(y_mit * 0.50, 0.85, "P", "izq", "+"),
            Vano(y_mit + (ancho - y_mit) * 0.50, 0.90, "P", "izq", "+"),
        ],
    )
    tabique(lz, x_alm, y_mit, largo - esp, y_mit, esp=0.15)
    w_fr = largo - esp - x_alm
    # Doble línea de aislamiento térmico en cámara frigorífica
    lz.rect(
        x_alm + 0.12,
        y_mit + 0.12,
        w_fr - 0.24,
        ancho - esp - y_mit - 0.24,
        "PA14-APARATOS",
    )
    estante(lz, x_alm + 0.22, y_mit + 0.25, w_fr - 0.44, 0.45, 2)
    lz.txt(
        x_alm + w_fr / 2,
        y_mit + (ancho - y_mit) * 0.55,
        "CAMARA FRIO -18C/+4C",
        h=0.13,
        w_max=w_fr - 0.3,
    )
    estante(lz, x_alm + 0.20, esp + 0.20, w_fr - 0.40, 0.45, 3)
    lz.txt(x_alm + w_fr / 2, y_mit * 0.55, "DESPENSA SECA", h=0.13, w_max=w_fr - 0.3)

    xs = [0.0, x_coc, x_alm, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - COMEDOR Y COCINA INDUSTRIAL (NTS 142-MINSA / RNE A.070)"


# =============================================================== EDIF-06 y 07
def _amoblar_crujia_sur_oficinas(
    lz: Lienzo, tramos: list[tuple[float, float, str]], esp: float, y_sur: float
) -> None:
    """Dibuja los tabiques y el mobiliario de cada ambiente en la crujía Sur de oficinas."""
    h_sur = y_sur - esp
    for idx, (xa, w_of, nom_of) in enumerate(tramos):
        if idx > 0:
            tabique(lz, xa, esp, xa, y_sur)
        if "DIRECTORIO" in nom_of or "REUNIONES" in nom_of:
            wm = min(4.20, w_of - 1.60)
            dm = min(1.50, h_sur - 1.60)
            mesa_sillas(
                lz,
                xa + (w_of - wm) / 2,
                esp + (h_sur - dm) / 2,
                wm,
                dm,
                por_lado=5,
                cabeceras=True,
            )
        elif "AUDITORIO" in nom_of:
            lz.rect(xa + w_of - 0.85, esp + 0.30, 0.60, h_sur - 0.60, "PA14-MOBILIARIO")
            for c_i in range(3):
                for r_i in range(3):
                    lz.rect(
                        xa + 0.55 + c_i * 1.35,
                        esp + 0.45 + r_i * ((h_sur - 1.1) / 3),
                        0.90,
                        0.45,
                        "PA14-MOBILIARIO",
                    )
        else:
            escritorio(lz, xa + (w_of - 1.50) / 2, esp + 0.35, 1.50, 0.70, 0)
            estante(lz, xa + w_of - 0.55, esp + 0.30, 0.40, min(1.80, h_sur - 0.80), 3)
        lz.txt(xa + w_of / 2, y_sur - 0.45, nom_of, h=0.14, w_max=w_of - 0.3)


def planta_oficinas(lz: Lienzo, largo: float, ancho: float, es_central: bool) -> str:
    """EDIF-06 (Central 40x15m con Auditorio) y EDIF-07 (Satélite 30x10m)."""
    esp = 0.15
    pas = 1.80
    y_sur = round(ancho * 0.42, 2)
    y_nor = y_sur + pas

    oficinas_sur = (
        [
            ("RECEPCION Y CONTROL", 0.14),
            ("GERENCIA PROYECTO", 0.16),
            ("RESIDENCIA OBRA", 0.16),
            ("JEFATURA SSOMA", 0.14),
            ("SALA DIRECTORIO (14 PAX)", 0.22),
            ("AUDITORIO INDUCCION", 0.18),
        ]
        if es_central
        else [
            ("RECEPCION", 0.16),
            ("ING. RESIDENTE FRENTE 2", 0.22),
            ("SUPERVISION MTC/CLIENTE", 0.22),
            ("CONTROL DOCUMENTARIO", 0.16),
            ("SALA DE REUNIONES", 0.24),
        ]
    )

    w_disp = largo - 2 * esp
    vanos_s: list[Vano] = []
    vp_s: list[Vano] = []
    xs = [0.0]
    x_cur = esp
    tramos: list[tuple[float, float, str]] = []
    for idx, (nom_of, frac) in enumerate(oficinas_sur):
        w_of = w_disp * frac
        tramos.append((x_cur, w_of, nom_of))
        xs.append(round(x_cur, 3))
        if idx == 0:
            vanos_s.append(
                Vano(x_cur + w_of / 2, 1.60, "P2", "izq", "in", "INGRESO PRINCIPAL")
            )
            vp_s.append(Vano(x_cur + w_of / 2, 1.20, "A"))
        else:
            vanos_s.append(Vano(x_cur + w_of / 2, min(1.80, w_of * 0.55), "V"))
            vp_s.append(Vano(x_cur + 0.70, 0.85, "P", "izq", "-"))
        x_cur += w_of
    xs.append(largo)

    # Crujía Norte: Pool de Ingeniería (60%), Sala TI/Plotters (18%), Baterías SSHH Damas/Varones (22%)
    x_ti = esp + w_disp * 0.60
    x_sh = esp + w_disp * 0.78
    x_sh_m = (x_sh + largo - esp) / 2
    vanos_n = [
        Vano(esp + w_disp * 0.15, 2.00, "V"),
        Vano(esp + w_disp * 0.35, 2.00, "V"),
        Vano(esp + w_disp * 0.50, 2.00, "V"),
        Vano((x_ti + x_sh) / 2, 1.40, "V"),
        Vano((x_sh + x_sh_m) / 2, 0.90, "V"),
        Vano((x_sh_m + largo - esp) / 2, 0.90, "V"),
    ]
    vp_n = [
        Vano(esp + w_disp * 0.18, 1.40, "P2", "izq", "+"),
        Vano(esp + w_disp * 0.45, 0.90, "P", "izq", "+"),
        Vano((x_ti + x_sh) / 2, 0.90, "P", "izq", "+"),
        Vano(x_sh + 0.65, 0.80, "P", "izq", "+"),
        Vano(x_sh_m + 0.65, 0.80, "P", "izq", "+"),
    ]

    _vereda_perimetral(lz, largo, ancho)
    cerramiento(
        lz,
        largo,
        ancho,
        esp,
        "PA14-MUROS",
        {
            "S": vanos_s,
            "N": vanos_n,
            "O": [Vano((y_sur + y_nor) / 2, 1.40, "P2", "izq", "out", "SALIDA EVAC.")],
            "E": [Vano((y_sur + y_nor) / 2, 1.40, "P2", "izq", "out", "SALIDA EVAC.")],
        },
        achurar=True,
    )
    tabique(lz, esp, y_sur, largo - esp, y_sur, vp_s, esp=0.12, capa="PA14-MUROS")
    tabique(lz, esp, y_nor, largo - esp, y_nor, vp_n, esp=0.12, capa="PA14-MUROS")
    lz.txt(
        largo / 2,
        (y_sur + y_nor) / 2,
        f"PASADIZO ADMINISTRATIVO Y CIRCULACION (A={pas:.2f} m - RNE A.080)",
        h=0.18,
        w_max=largo - 6.0,
    )

    _amoblar_crujia_sur_oficinas(lz, tramos, esp, y_sur)

    # Amoblar Crujía Norte
    h_nor = ancho - esp - y_nor
    tabique(lz, x_ti, y_nor, x_ti, ancho - esp)
    tabique(lz, x_sh, y_nor, x_sh, ancho - esp)
    tabique(lz, x_sh_m, y_nor, x_sh_m, ancho - esp)

    w_pool = x_ti - esp
    n_islas = 6 if es_central else 4
    paso_i = (w_pool - 1.20) / n_islas
    for i in range(n_islas):
        xi = esp + 0.60 + i * paso_i
        escritorio(lz, xi, ancho - esp - 1.45, 1.35, 0.65, 180)
        if h_nor >= 4.20:
            escritorio(lz, xi, y_nor + 0.35, 1.35, 0.65, 0)
    lz.txt(
        esp + w_pool / 2,
        y_nor + h_nor / 2,
        "POOL DE INGENIERIA, CAD, TOPOGRAFIA Y CONTROL DE PROYECTOS",
        h=0.17,
        w_max=w_pool - 1.0,
    )

    # Sala TI y Plotters
    estante(lz, x_ti + 0.25, ancho - esp - 0.70, (x_sh - x_ti) - 0.50, 0.55, 4)
    estante(lz, x_ti + 0.25, y_nor + 0.25, 1.40, 0.65, 2)
    lz.txt(
        (x_ti + x_sh) / 2,
        y_nor + h_nor / 2,
        "SERVIDORES TI / PLOTTERS / ARCHIVO",
        h=0.14,
        w_max=(x_sh - x_ti) - 0.3,
    )

    # Baterías SSHH Damas y Varones
    for x_b, w_b, etq, con_urin in (
        (x_sh, x_sh_m - x_sh, "SS.HH. DAMAS", False),
        (x_sh_m, largo - esp - x_sh_m, "SS.HH. VARONES", True),
    ):
        for k in range(2):
            inodoro(lz, x_b + 0.25 + k * 0.95, ancho - esp - 0.70, 180)
            lavatorio(lz, x_b + 0.25 + k * 0.85, y_nor + 0.08, 0)
        if con_urin and w_b >= 2.2:
            urinario(lz, x_b + w_b - 0.48, y_nor + h_nor * 0.45, 270)
        lz.txt(x_b + w_b / 2, y_nor + h_nor * 0.52, etq, h=0.13, w_max=w_b - 0.3)

    ys = [0.0, y_sur, y_nor, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - EDIFICIO DE OFICINAS E INGENIERIA (RNE A.080)"


# =============================================================== EDIF-08 y 09
def planta_topico_medico(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-08 (15x8m) y EDIF-09 (8x7m): Tópico Médico 24/7 + Bahía de Ambulancia Tipo II."""
    esp = 0.15
    x_amb = round(largo * 0.64, 2)
    x_tri = round(x_amb * 0.48, 2)
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
                Vano(x_tri / 2, 1.30, "P2", "izq", "in", "ACCESO PACIENTES"),
                Vano((x_tri + x_amb) / 2, 1.20, "V"),
                Vano(
                    (x_amb + largo) / 2,
                    max(2.80, (largo - x_amb) * 0.72),
                    "PO",
                    etiqueta="SALIDA AMBULANCIA",
                ),
            ],
            "N": [Vano(x_tri / 2, 1.20, "V"), Vano((x_tri + x_amb) / 2, 1.20, "V")],
            "O": [Vano(y_mit * 0.5, 1.10, "V"), Vano(y_mit * 1.5, 1.10, "V")],
        },
        achurar=True,
    )
    # Rampa vehicular frente a bahía de ambulancia
    lz.rect(x_amb + 0.30, -1.05, (largo - x_amb) - 0.60, 1.05, "PA14-OBRAS-ARTE")

    tabique(
        lz,
        x_amb,
        esp,
        x_amb,
        ancho - esp,
        [Vano(y_mit * 0.5, 1.10, "P", "izq", "-")],
        esp=0.15,
        capa="PA14-MUROS",
    )
    tabique(
        lz,
        x_tri,
        esp,
        x_tri,
        ancho - esp,
        [
            Vano(y_mit * 0.5, 0.90, "P", "izq", "+"),
            Vano(y_mit * 1.5, 0.90, "P", "izq", "+"),
        ],
    )
    tabique(
        lz,
        esp,
        y_mit,
        x_amb,
        y_mit,
        [
            Vano(x_tri * 0.5, 0.85, "P", "izq", "+"),
            Vano((x_tri + x_amb) / 2, 0.90, "P", "izq", "+"),
        ],
    )

    # Cuadrante SO: Triaje, recepción y consultorio
    escritorio(lz, esp + 0.35, esp + 0.25, min(1.30, x_tri - 0.80), 0.60, 0)
    lz.txt(x_tri / 2, y_mit - 0.55, "TRIAJE Y CONSULTORIO", h=0.13, w_max=x_tri - 0.4)

    # Cuadrante NO: Farmacia, central O2 medicinal y SSHH accesible
    estante(lz, esp + 0.20, ancho - esp - 0.55, min(1.80, x_tri - 0.60), 0.42, 3)
    for k in range(3):
        lz.circ(esp + 0.35 + k * 0.32, y_mit + 0.40, 0.12, "PA14-APARATOS")
    inodoro(lz, x_tri - 0.55, ancho - esp - 0.70, 180)
    lavatorio(lz, x_tri - 0.58, y_mit + 0.15, 270)
    lz.txt(
        x_tri / 2,
        y_mit + (ancho - y_mit) * 0.52,
        "FARMACIA / O2 / SSHH",
        h=0.12,
        w_max=x_tri - 0.4,
    )

    # Cuadrante SE: Sala Trauma-Shock (camilla clínica + desfibrilador)
    w_ts = x_amb - x_tri
    cama(lz, x_tri + (w_ts - 1.85) / 2, esp + 0.35, rot=90, w=0.80, l_c=1.85)
    lz.txt(x_tri + w_ts / 2, y_mit - 0.55, "TRAUMA SHOCK", h=0.13, w_max=w_ts - 0.3)

    # Cuadrante NE: Observación e Hipobaria (camas clínicas)
    cama(lz, x_tri + 0.25, ancho - esp - 1.15, rot=90, w=0.80, l_c=1.85)
    if w_ts >= 3.80:
        cama(lz, x_tri + 2.35, ancho - esp - 1.15, rot=90, w=0.80, l_c=1.85)
    lz.txt(x_tri + w_ts / 2, y_mit + 0.55, "OBSERVACION 24/7", h=0.13, w_max=w_ts - 0.3)

    # Bahía Este: Ambulancia 4x4 Tipo II estacionada lista para salida (rot=180 mira al Sur)
    w_bah = largo - esp - x_amb
    w_v = min(2.10, w_bah - 0.50)
    l_v = min(5.00, ancho - 1.40)
    vehiculo(
        lz,
        x_amb + (w_bah - w_v) / 2,
        (ancho - l_v) / 2,
        w_v,
        l_v,
        "AMBULANCIA 4x4 TIPO II",
        rot=180,
    )
    lz.txt(
        x_amb + w_bah / 2, ancho - 0.50, "BAHIA AMBULANCIA", h=0.13, w_max=w_bah - 0.2
    )

    xs = [0.0, x_tri, x_amb, largo]
    ys = [0.0, y_mit, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - TOPICO MEDICO 24/7 Y BAHIA DE AMBULANCIA (DS 024 ART. 157)"
