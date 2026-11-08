"""Plantas arquitectónicas de residencia y habitabilidad (EDIF-01, EDIF-02, EDIF-03)."""

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
    tabique,
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
