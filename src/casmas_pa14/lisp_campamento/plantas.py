"""Plantas arquitectónicas y estructurales detalladas (EDIF-01..13, 22, 29, 33, 34, 35).

Cada función construye la planta sobre un ``Lienzo`` usando muros con vanos reales,
tabiques, ejes estructurales, columnas y bloques de mobiliario/equipos a escala en metros.
"""

from __future__ import annotations

from .base import (
    Lienzo,
    Vano,
    cama,
    cerramiento,
    columnas,
    cotas_totales,
    ducha,
    ejes,
    escalera,
    escritorio,
    estante,
    inodoro,
    lavatorio,
    lockers,
    mesa_sillas,
    tabique,
    urinario,
    vehiculo,
)


def _vereda_perimetral(
    lz: Lienzo, largo: float, ancho: float, w_ver: float = 0.80
) -> None:
    """Vereda perimetral de concreto con cuneta pluvial exterior."""
    lz.rect(-w_ver, -w_ver, largo + 2 * w_ver, ancho + 2 * w_ver, "PA14-OBRAS-ARTE")
    lz.rect(
        -w_ver - 0.25,
        -w_ver - 0.25,
        largo + 2 * w_ver + 0.50,
        ancho + 2 * w_ver + 0.50,
        "PA14-OBRAS-ARTE",
    )


def _bano_privado(
    lz: Lienzo, x: float, y: float, w: float, h: float, sur: bool
) -> None:
    """Baño privado completo (ducha + inodoro + lavatorio) dentro de habitación."""
    vp = Vano(x + w / 2, 0.70, "P", "izq", "-" if sur else "+")
    if sur:
        tabique(lz, x, y, x, y + h)
        tabique(lz, x + w, y, x + w, y + h)
        tabique(lz, x, y, x + w, y, [vp])
        ducha(lz, x + 0.08, y + h - 0.88, 0.80)
        inodoro(lz, x + w - 0.48, y + h - 0.70, 180)
        lavatorio(lz, x + 0.08, y + 0.12, 90)
    else:
        tabique(lz, x, y, x, y + h)
        tabique(lz, x + w, y, x + w, y + h)
        tabique(lz, x, y + h, x + w, y + h, [vp])
        ducha(lz, x + 0.08, y + 0.08, 0.80)
        inodoro(lz, x + w - 0.48, y + 0.05, 0)
        lavatorio(lz, x + 0.08, y + h - 0.54, 90)
    lz.txt(x + w / 2, y + h / 2, "SS.HH.", h=0.10, w_max=w - 0.15)


# ===================================================================== EDIF-01
def planta_edif_01(lz: Lienzo, largo: float, ancho: float, det: dict) -> str:
    """EDIF-01: Pabellón de Dormitorios Staff e Ingeniería (doble crujía + hall central)."""
    esp = float(det.get("espesor_muro_ext_m", 0.15))
    pas = float(det.get("ancho_pasadizo_m", 2.00))
    w_hall = float(det.get("ancho_modulo_central_m", 4.50))
    w_mod = float(det.get("ancho_modulo_m", 3.50))
    y_sur = (ancho - pas) / 2.0
    y_nor = y_sur + pas
    x_hall = (largo - w_hall) / 2.0

    # Calcular divisiones de habitaciones en Ala Oeste y Ala Este
    alas = [(esp, x_hall), (x_hall + w_hall, largo - esp)]
    vanos_s: list[Vano] = [
        Vano(x_hall + w_hall / 2, 1.80, "P2", "izq", "in", "INGRESO PRINCIPAL")
    ]
    vanos_n: list[Vano] = [Vano(x_hall + w_hall / 2, 1.40, "V")]
    vanos_pas_s: list[Vano] = [Vano(x_hall + w_hall / 2, 1.60, "A")]
    vanos_pas_n: list[Vano] = [Vano(x_hall + w_hall / 2, 1.60, "A")]
    xs_ejes = [0.0, x_hall, x_hall + w_hall]

    tramos_hab: list[tuple[float, float]] = []
    for x0, x1 in alas:
        n_m = max(2, round((x1 - x0) / w_mod))
        wr = (x1 - x0) / n_m
        for i in range(n_m):
            xa = x0 + i * wr
            tramos_hab.append((xa, wr))
            xs_ejes.append(round(xa, 3))
            vanos_s.append(Vano(xa + wr * 0.55, 1.40, "V"))
            vanos_n.append(Vano(xa + wr * 0.55, 1.40, "V"))
            vanos_pas_s.append(Vano(xa + wr - 0.65, 0.85, "P", "der", "-"))
            vanos_pas_n.append(Vano(xa + wr - 0.65, 0.85, "P", "der", "+"))
    xs_ejes = sorted(set([0.0, *xs_ejes, largo]))

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
            "O": [Vano(ancho / 2, 1.60, "P2", "izq", "out", "SALIDA EVAC.")],
            "E": [Vano(ancho / 2, 1.60, "P2", "izq", "out", "SALIDA EVAC.")],
        },
        achurar=True,
    )
    # Esclusa térmica cortaviento en acceso Sur
    lz.rect(x_hall + 0.70, -1.30, w_hall - 1.40, 1.30, "PA14-MUROS")
    lz.txt(x_hall + w_hall / 2, -0.65, "ESCLUSA TERMICA", h=0.14, w_max=w_hall - 1.5)

    # Muros longitudinales del pasadizo central
    tabique(
        lz, esp, y_sur, largo - esp, y_sur, vanos_pas_s, esp=0.12, capa="PA14-MUROS"
    )
    tabique(
        lz, esp, y_nor, largo - esp, y_nor, vanos_pas_n, esp=0.12, capa="PA14-MUROS"
    )
    lz.txt(
        x_hall / 2,
        ancho / 2,
        f"PASADIZO CENTRAL CALEFACCIONADO (A={pas:.2f} m)",
        h=0.18,
        w_max=x_hall - 2.0,
    )
    lz.txt(
        (x_hall + w_hall + largo) / 2,
        ancho / 2,
        f"PASADIZO CENTRAL CALEFACCIONADO (A={pas:.2f} m)",
        h=0.18,
        w_max=x_hall - 2.0,
    )

    # Hall central y caja de escalera a 2do nivel
    tabique(lz, x_hall, esp, x_hall, y_sur, esp=0.12, capa="PA14-MUROS")
    tabique(
        lz, x_hall + w_hall, esp, x_hall + w_hall, y_sur, esp=0.12, capa="PA14-MUROS"
    )
    tabique(lz, x_hall, y_nor, x_hall, ancho - esp, esp=0.12, capa="PA14-MUROS")
    tabique(
        lz,
        x_hall + w_hall,
        y_nor,
        x_hall + w_hall,
        ancho - esp,
        esp=0.12,
        capa="PA14-MUROS",
    )
    escritorio(lz, x_hall + w_hall / 2 - 0.80, esp + 0.50, 1.60, 0.65, 0)
    lz.txt(
        x_hall + w_hall / 2,
        y_sur - 0.80,
        "RECEPCION / CONSERJERIA",
        h=0.15,
        w_max=w_hall - 0.5,
    )
    escalera(lz, x_hall + 0.45, y_nor + 0.25, w_hall - 0.90, ancho - esp - y_nor - 0.50)

    # Habitaciones individuales con baño privado, cama, ropero y escritorio
    num = 101
    for xa, wr in tramos_hab:
        if xa > esp + 0.05 and abs(xa - (x_hall + w_hall)) > 0.05:
            tabique(lz, xa, esp, xa, y_sur)
            tabique(lz, xa, y_nor, xa, ancho - esp)
        # Sur
        _bano_privado(lz, xa + 0.06, y_sur - 1.85, 1.55, 1.80, sur=True)
        cama(lz, xa + 0.20, esp + 0.25, rot=90, w=1.00, l_c=2.00)
        estante(lz, xa + wr - 0.62, y_sur - 2.35, 0.50, 1.20)
        escritorio(lz, xa + wr - 1.45, esp + 0.20, 1.15, 0.55, 0)
        lz.txt(xa + wr * 0.52, esp + 1.95, f"HAB-{num}", h=0.14, w_max=wr - 0.4)
        num += 1
        # Norte
        _bano_privado(lz, xa + 0.06, y_nor + 0.05, 1.55, 1.80, sur=False)
        cama(lz, xa + 0.20, ancho - esp - 1.25, rot=90, w=1.00, l_c=2.00)
        estante(lz, xa + wr - 0.62, y_nor + 1.15, 0.50, 1.20)
        escritorio(lz, xa + wr - 1.45, ancho - esp - 1.40, 1.15, 0.55, 180)
        lz.txt(xa + wr * 0.52, ancho - esp - 1.95, f"HAB-{num}", h=0.14, w_max=wr - 0.4)
        num += 1

    ys_ejes = [0.0, y_sur, y_nor, ancho]
    columnas(lz, xs_ejes, ys_ejes, "panel")
    ejes(lz, xs_ejes[::2] if len(xs_ejes) > 10 else xs_ejes, ys_ejes, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - EDIFICACION MODULAR TERMOACUSTICA (2 NIVELES)"


# ===================================================================== EDIF-02
def _pabellon_obrero_ala(
    lz: Lienzo, largo: float, y0: float, h_pab: float, sufijo: str
) -> list[float]:
    """Dibuja un pabellón obrero completo (doble crujía + pasillo central + baterías SSHH)."""
    esp = 0.15
    pas = 1.80
    h_hab = (h_pab - pas) / 2.0
    ya_s = y0 + h_hab
    ya_n = ya_s + pas
    w_sshh = 4.60
    x_ini = esp + w_sshh
    x_fin = largo - esp - w_sshh
    n_mod = max(4, round((x_fin - x_ini) / 3.80))
    w_mod = (x_fin - x_ini) / n_mod

    vanos_s = [
        Vano(esp + w_sshh / 2, 1.10, "V"),
        Vano(largo - esp - w_sshh / 2, 1.10, "V"),
    ]
    vanos_n = [
        Vano(esp + w_sshh / 2, 1.10, "V"),
        Vano(largo - esp - w_sshh / 2, 1.10, "V"),
    ]
    vp_s = [
        Vano(esp + w_sshh - 0.70, 0.85, "P", "der", "-"),
        Vano(largo - esp - w_sshh + 0.70, 0.85, "P", "izq", "-"),
    ]
    vp_n = [
        Vano(esp + w_sshh - 0.70, 0.85, "P", "der", "+"),
        Vano(largo - esp - w_sshh + 0.70, 0.85, "P", "izq", "+"),
    ]
    xs = [0.0, esp + w_sshh]
    for i in range(n_mod):
        xm = x_ini + i * w_mod
        xs.append(round(xm, 3))
        vanos_s.append(Vano(xm + w_mod / 2, 1.30, "V"))
        vanos_n.append(Vano(xm + w_mod / 2, 1.30, "V"))
        vp_s.append(Vano(xm + w_mod - 0.65, 0.85, "P", "der", "-"))
        vp_n.append(Vano(xm + w_mod - 0.65, 0.85, "P", "der", "+"))
    xs.extend([round(x_fin, 3), largo])

    with lz.local(0.0, y0, 0):
        cerramiento(
            lz,
            largo,
            h_pab,
            esp,
            "PA14-MUROS",
            {
                "S": vanos_s,
                "N": vanos_n,
                "O": [
                    Vano(h_pab / 2, 1.50, "P2", "izq", "out", f"ACCESO PAB. {sufijo}")
                ],
                "E": [Vano(h_pab / 2, 1.50, "P2", "izq", "out", "SALIDA EMERG.")],
            },
            achurar=True,
        )
    tabique(lz, esp, ya_s, largo - esp, ya_s, vp_s, esp=0.12, capa="PA14-MUROS")
    tabique(lz, esp, ya_n, largo - esp, ya_n, vp_n, esp=0.12, capa="PA14-MUROS")
    lz.txt(
        largo / 2,
        (ya_s + ya_n) / 2,
        f"PABELLON {sufijo} - PASADIZO TERMICO (A={pas:.2f} m - EVAC. RNE A.130)",
        h=0.17,
        w_max=largo - 12.0,
    )

    # Baterías SSHH en extremos Oeste y Este
    for xb, etq in ((esp, f"SS.HH. OESTE {sufijo}"), (x_fin, f"SS.HH. ESTE {sufijo}")):
        tabique(
            lz,
            xb + (w_sshh if xb < 1.0 else 0.0),
            y0 + esp,
            xb + (w_sshh if xb < 1.0 else 0.0),
            ya_s,
        )
        tabique(
            lz,
            xb + (w_sshh if xb < 1.0 else 0.0),
            ya_n,
            xb + (w_sshh if xb < 1.0 else 0.0),
            y0 + h_pab - esp,
        )
        for k in range(4):
            inodoro(lz, xb + 0.30 + k * 0.95, y0 + esp + 0.05, 0)
            lavatorio(lz, xb + 0.30 + k * 0.95, ya_s - 0.50, 180)
            ducha(lz, xb + 0.30 + k * 0.95, y0 + h_pab - esp - 0.90, 0.82)
            lavatorio(lz, xb + 0.30 + k * 0.95, ya_n + 0.08, 0)
        lz.txt(xb + w_sshh / 2, y0 + h_hab / 2, etq, h=0.13, w_max=w_sshh - 0.4)
        lz.txt(
            xb + w_sshh / 2,
            ya_n + h_hab / 2,
            f"DUCHAS {sufijo}",
            h=0.13,
            w_max=w_sshh - 0.4,
        )

    # Módulos cuádruples (2 literas dobles + 4 lockers)
    for i in range(n_mod):
        xm = x_ini + i * w_mod
        if i > 0:
            tabique(lz, xm, y0 + esp, xm, ya_s)
            tabique(lz, xm, ya_n, xm, y0 + h_pab - esp)
        # Sur (h_hab = 3.70 m -> camas caben con holgura exacta)
        cama(lz, xm + 0.18, y0 + esp + 0.18, rot=0, w=0.90, l_c=1.90, litera=True)
        cama(lz, xm + 1.25, y0 + esp + 0.18, rot=0, w=0.90, l_c=1.90, litera=True)
        lockers(lz, xm + w_mod - 0.58, y0 + esp + 0.20, 4, rot=90, w=0.42, d=0.45)
        lz.txt(
            xm + w_mod * 0.45,
            ya_s - 0.55,
            f"M-{sufijo}{i + 1:02d}S (4P)",
            h=0.12,
            w_max=w_mod - 1.0,
        )
        # Norte
        cama(
            lz,
            xm + 0.18,
            y0 + h_pab - esp - 2.08,
            rot=180,
            w=0.90,
            l_c=1.90,
            litera=True,
        )
        cama(
            lz,
            xm + 1.25,
            y0 + h_pab - esp - 2.08,
            rot=180,
            w=0.90,
            l_c=1.90,
            litera=True,
        )
        lockers(lz, xm + w_mod - 0.13, ya_n + 0.30, 4, rot=90, w=0.42, d=0.45)
        lz.txt(
            xm + w_mod * 0.45,
            ya_n + 0.55,
            f"M-{sufijo}{i + 1:02d}N (4P)",
            h=0.12,
            w_max=w_mod - 1.0,
        )

    return sorted(set(xs))


def planta_edif_02(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-02: Pabellón de Dormitorios Obreros A y B (2 pabellones paralelos + patio central)."""
    patio = 3.60
    h_pab = (
        ancho - patio
    ) / 2.0  # 9.20 m cada pabellón (proporción arquitectónica real)
    _vereda_perimetral(lz, largo, ancho)
    xs = _pabellon_obrero_ala(lz, largo, 0.0, h_pab, "A")
    _pabellon_obrero_ala(lz, largo, h_pab + patio, h_pab, "B")

    # Corredor/patio central techado y pasarelas de interconexión
    y_pat_s, y_pat_n = h_pab, h_pab + patio
    lz.rect(largo * 0.25, y_pat_s, 2.40, patio, "PA14-OBRAS-ARTE")
    lz.rect(largo * 0.75 - 2.40, y_pat_s, 2.40, patio, "PA14-OBRAS-ARTE")
    lz.lin(0.0, (y_pat_s + y_pat_n) / 2, largo, (y_pat_s + y_pat_n) / 2, "PA14-EJE")
    lz.txt(
        largo / 2,
        (y_pat_s + y_pat_n) / 2,
        f"PATIO / CORREDOR DE VENTILACION E INTERCONEXION ENTRE PABELLONES A Y B (A={patio:.2f} m)",
        h=0.19,
        w_max=largo - 8.0,
    )
    ys = [0.0, h_pab, h_pab + patio, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs[::2] if len(xs) > 10 else xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - DOBLE PABELLON MODULAR PARALELO (PABELLONES A Y B)"


# ===================================================================== EDIF-03
def planta_edif_03(lz: Lienzo, largo: float, ancho: float) -> str:
    """EDIF-03: Dormitorios Satélite Frente 2 (módulos térmicos con baño/ducha y lockers integrados)."""
    esp = 0.15
    pas = 2.40
    y_sur = (ancho - pas) / 2.0  # 6.80 m
    y_nor = y_sur + pas
    n_mod = max(6, round((largo - 2 * esp) / 4.10))
    w_mod = (largo - 2 * esp) / n_mod

    vanos_s, vanos_n, vp_s, vp_n, xs = [], [], [], [], [0.0]
    for i in range(n_mod):
        xm = esp + i * w_mod
        xs.append(round(xm, 3))
        vanos_s.append(Vano(xm + w_mod * 0.55, 1.40, "V"))
        vanos_n.append(Vano(xm + w_mod * 0.55, 1.40, "V"))
        vp_s.append(Vano(xm + w_mod - 0.65, 0.85, "P", "der", "-"))
        vp_n.append(Vano(xm + w_mod - 0.65, 0.85, "P", "der", "+"))
    xs.append(largo)

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
            "O": [Vano(ancho / 2, 1.60, "P2", "izq", "out", "ESCLUSA ACCESO")],
            "E": [Vano(ancho / 2, 1.60, "P2", "izq", "out", "SALIDA EMERG.")],
        },
        achurar=True,
    )
    tabique(lz, esp, y_sur, largo - esp, y_sur, vp_s, esp=0.12, capa="PA14-MUROS")
    tabique(lz, esp, y_nor, largo - esp, y_nor, vp_n, esp=0.12, capa="PA14-MUROS")
    lz.txt(
        largo / 2,
        ancho / 2,
        f"PASADIZO CENTRAL CALEFACCIONADO 3,850 msnm (A={pas:.2f} m - DUCHAS INTEGRADAS)",
        h=0.19,
        w_max=largo - 4.0,
    )

    for i in range(n_mod):
        xm = esp + i * w_mod
        if i > 0:
            tabique(lz, xm, esp, xm, y_sur)
            tabique(lz, xm, y_nor, xm, ancho - esp)
        # Módulo Sur: zona vestuario + SSHH con ducha caliente junto al pasillo + 2 literas al fondo
        _bano_privado(lz, xm + 0.06, y_sur - 1.95, 1.65, 1.90, sur=True)
        lockers(lz, xm + w_mod - 0.55, y_sur - 2.30, 4, rot=90, w=0.45, d=0.48)
        cama(lz, xm + 0.18, esp + 0.25, rot=0, w=0.95, l_c=1.95, litera=True)
        cama(lz, xm + 1.35, esp + 0.25, rot=0, w=0.95, l_c=1.95, litera=True)
        escritorio(lz, xm + w_mod - 1.35, esp + 0.25, 1.10, 0.55, 0)
        lz.txt(
            xm + w_mod * 0.48,
            esp + 2.85,
            f"MOD-{i + 1:02d}A (4 PAX)",
            h=0.13,
            w_max=w_mod - 0.6,
        )

        # Módulo Norte
        _bano_privado(lz, xm + 0.06, y_nor + 0.05, 1.65, 1.90, sur=False)
        lockers(lz, xm + w_mod - 0.07, y_nor + 0.50, 4, rot=90, w=0.45, d=0.48)
        cama(lz, xm + 0.18, ancho - esp - 2.20, rot=180, w=0.95, l_c=1.95, litera=True)
        cama(lz, xm + 1.35, ancho - esp - 2.20, rot=180, w=0.95, l_c=1.95, litera=True)
        escritorio(lz, xm + w_mod - 1.35, ancho - esp - 1.45, 1.10, 0.55, 180)
        lz.txt(
            xm + w_mod * 0.48,
            ancho - esp - 2.85,
            f"MOD-{i + 1:02d}B (4 PAX)",
            h=0.13,
            w_max=w_mod - 0.6,
        )

    ys = [0.0, y_sur, y_nor, ancho]
    columnas(lz, xs, ys, "panel")
    ejes(lz, xs, ys, largo, ancho)
    cotas_totales(lz, largo, ancho)
    return "T1 - PABELLON SATELITE DE ALTA MONTANA CON SSHH INTEGRADO"


# =============================================================== EDIF-04 y 05
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


# =============================================================== EDIF-13 y 35
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


# =============================================================== EDIF-10 y 29
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
