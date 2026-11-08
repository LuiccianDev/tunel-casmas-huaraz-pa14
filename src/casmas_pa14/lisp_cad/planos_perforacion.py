"""Generadores AutoLISP de malla de perforación y cortes de explanación de portales."""

from __future__ import annotations

import math

from .nucleo import (
    Dibujo,
    _circulo,
    _cota,
    _linea,
    _n,
    _rect,
    _texto,
    _texto_cen,
)


def _taladros_cune(x_cune: float, y_cune: float, r_tal: float) -> list[str]:
    """Genera las entidades del cuñe cilíndrico de 4 secciones y el alivio central."""
    cuerpo: list[str] = [
        _circulo(x_cune, y_cune, 0.18, "PA14-ALIVIO"),
        _texto_cen(x_cune, y_cune - 0.40, 0.20, "ALIVIO D=102mm", "PA14-TEXTO"),
    ]
    for d_sq in (0.25, 0.90):
        for dx, dy in [(-d_sq, -d_sq), (-d_sq, d_sq), (d_sq, -d_sq), (d_sq, d_sq)]:
            cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
        cuerpo.append(
            _rect(x_cune - d_sq, y_cune - d_sq, 2 * d_sq, 2 * d_sq, "PA14-SIMBOLOS")
        )

    d2 = 0.50
    for dx, dy in [(0, -d2), (0, d2), (-d2, 0), (d2, 0)]:
        cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
    cuerpo.extend(
        [
            _linea(x_cune, y_cune - d2, x_cune + d2, y_cune, "PA14-SIMBOLOS"),
            _linea(x_cune + d2, y_cune, x_cune, y_cune + d2, "PA14-SIMBOLOS"),
            _linea(x_cune, y_cune + d2, x_cune - d2, y_cune, "PA14-SIMBOLOS"),
            _linea(x_cune - d2, y_cune, x_cune, y_cune - d2, "PA14-SIMBOLOS"),
        ]
    )

    d4 = 1.45
    pts_d4 = [
        (-d4, -d4),
        (-d4, 0),
        (-d4, d4),
        (0, -d4),
        (0, d4),
        (d4, -d4),
        (d4, 0),
        (d4, d4),
    ]
    for dx, dy in pts_d4:
        cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
    cuerpo.append(_rect(x_cune - d4, y_cune - d4, 2 * d4, 2 * d4, "PA14-SIMBOLOS"))
    return cuerpo


def _taladros_malla(
    b: float, hw: float, radio: float, xc: float, yc: float
) -> list[str]:
    """Genera las entidades de taladros (cuñe de 4 secciones, periferia, arrastre y ayuda)."""
    x_cune, y_cune = xc, hw + 0.60
    r_tal = 0.08
    cuerpo = _taladros_cune(x_cune, y_cune, r_tal)

    y_p = 0.40
    while y_p <= hw:
        cuerpo.append(_circulo(0.20, y_p, r_tal, "PA14-TALADROS"))
        cuerpo.append(_circulo(b - 0.20, y_p, r_tal, "PA14-TALADROS"))
        y_p += 0.60

    r_perif, n_corona = radio - 0.20, 33
    for i in range(1, n_corona):
        ang_rad = math.pi * i / n_corona
        cuerpo.append(
            _circulo(
                xc - r_perif * math.cos(ang_rad),
                yc + r_perif * math.sin(ang_rad),
                r_tal,
                "PA14-TALADROS",
            )
        )

    n_zapateras = 17
    dx_zap = (b - 0.80) / (n_zapateras - 1)
    for i in range(n_zapateras):
        cuerpo.append(_circulo(0.40 + i * dx_zap, 0.20, r_tal, "PA14-TALADROS"))

    for x_ay in [1.20, 2.30, 3.40, 4.50, 8.80, 9.90, 11.00, 12.10]:
        cuerpo.append(_circulo(x_ay, 1.10, r_tal, "PA14-TALADROS"))
        cuerpo.append(_circulo(x_ay, 2.10, r_tal, "PA14-TALADROS"))
    for x_ay in [1.00, 2.20, 3.50, 4.80, 8.50, 9.80, 11.10, 12.30]:
        cuerpo.append(_circulo(x_ay, 3.50, r_tal, "PA14-TALADROS"))

    for r_int, n_int in [(radio - 1.50, 19), (radio - 2.80, 13)]:
        for i in range(1, n_int):
            ang_rad = math.pi * i / n_int
            xt = xc - r_int * math.cos(ang_rad)
            yt = yc + r_int * math.sin(ang_rad)
            if abs(xt - x_cune) > 1.3 or abs(yt - y_cune) > 1.3:
                cuerpo.append(_circulo(xt, yt, r_tal, "PA14-TALADROS"))
    return cuerpo


def dibujo_malla(sec: dict, vol: dict | None = None) -> Dibujo:
    """Malla de perforacion y voladura mecanizada (cuñe de 4 secciones, ayudas y periferia)."""
    b, h, hw = sec["ancho_m"], sec["altura_m"], sec["hastial_m"]
    radio = b / 2.0
    xc, yc = radio, hw

    cuerpo = []
    pts_contorno = f"'((0.0 0.0) ({_n(b)} 0.0) ({_n(b)} {_n(hw)}) (0.0 {_n(hw)}))"
    cuerpo.append(f'(pa14:pline {pts_contorno} \'(0.0 0.0 1.0 0.0) T "PA14-CONTORNO")')
    cuerpo.append(_linea(xc, -1.0, xc, h + 1.0, "PA14-EJE"))
    cuerpo.append(_linea(-1.0, hw, b + 1.0, hw, "PA14-EJE"))
    cuerpo.extend(_taladros_malla(b, hw, radio, xc, yc))
    cuerpo.append(_cota(0.0, 0.0, b, 0.0, xc, -1.80, f"B={b:.2f}m"))
    cuerpo.append(_cota(0.0, 0.0, 0.0, hw, -1.80, hw / 2, f"hw={hw:.2f}m"))
    cuerpo.append(_cota(0.0, 0.0, 0.0, h, -3.20, h / 2, f"H={h:.2f}m"))

    x_cuadro = b + 3.0
    y_cuadro = h
    w_cuadro = 8.8
    h_cuadro = 9.2
    cuerpo.append(
        _rect(x_cuadro, y_cuadro - h_cuadro, w_cuadro, h_cuadro, "PA14-CONTORNO")
    )
    cuerpo.append(
        _texto(
            x_cuadro + 0.5,
            y_cuadro - 0.8,
            0.32,
            "PARAMETROS DE MALLA DE PERFORACION",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _linea(
            x_cuadro,
            y_cuadro - 1.1,
            x_cuadro + w_cuadro,
            y_cuadro - 1.1,
            "PA14-CONTORNO",
        )
    )

    taladros_tot = sec["taladros"]
    avance_disparo = sec["avance_disparo_m"]
    area_exc = sec["area_m2"]
    burden_val = vol.get("inputs", {}).get("burden_m", 1.25) if vol else 1.25
    esp_val = vol.get("inputs", {}).get("espaciamiento_m", 1.75) if vol else 1.75

    lineas_datos = [
        f"Seccion tunel: Herradura ({b:.2f} x {h:.2f} m)",
        f"Area de excavacion: {area_exc:.2f} m2",
        f"Taladros de diseno: {taladros_tot} und",
        "Arranque: Cune quemado cilindrico (4 secc.)",
        "Alivio: 1 taladro D = 102 mm (4 pulg)",
        "Produccion: D = 45 mm (broca integral)",
        "Longitud barreno: 3.66 m (12 pies Sandvik)",
        f"Avance efectivo: {avance_disparo:.2f} m/disparo (90%)",
        f"Burden teorico Konya: B = {burden_val:.2f} m",
        f"Espaciamiento Konya: S = {esp_val:.2f} m",
        "Espaciamiento periferico: E = 0.60 m",
        "Taco inerte: T = 0.80 m (detritus compactado)",
        "Explosivo: Emulsion / ANFO (q=1.60 kg/m3)",
    ]

    for idx, linea_txt in enumerate(lineas_datos):
        cuerpo.append(
            _texto(
                x_cuadro + 0.5,
                y_cuadro - 1.7 - (idx * 0.52),
                0.22,
                linea_txt,
                "PA14-TEXTO",
            )
        )

    return Dibujo(
        "PA14_MALLA",
        "Malla de Perforacion y Disparo - Seccion Herradura (Drill & Blast)",
        cuerpo,
        b + w_cuadro + 8.0,
    )


def dibujo_cortes_accesos(portales: dict) -> Dibujo:
    """Sección transversal típica de corte en roca, banquetas y sobreancho DG-2018 (Civil 3D)."""
    dg = portales.get("dg2018_geometria", {})
    c3d = portales.get("cortes_civil3d", {})

    b_calzada = float(dg.get("ancho_calzada_base_m", 3.60))
    s_sobreancho = float(dg.get("sobreancho_calculado_m", 1.67))
    b_berma = 0.90
    w_cuneta = 1.00
    d_cuneta = 0.35
    h_banco = float(dg.get("altura_max_banco_m", 6.00))
    w_banqueta = float(dg.get("ancho_banqueta_resguardo_m", 5.00))
    talud_h = 0.5  # 0.5H:1V -> base = 3.00 m
    p_bombeo = 0.02  # -2.0%

    ox, oy = 13.0, 2.0
    x_eje, y_eje = ox, oy

    x_borde_izq = x_eje - (b_calzada / 2.0)
    y_borde_izq = y_eje - (b_calzada / 2.0) * p_bombeo
    x_berma_izq = x_borde_izq - b_berma
    y_berma_izq = y_borde_izq - b_berma * 0.04
    x_pie_relleno = x_berma_izq - 1.50
    y_pie_relleno = y_berma_izq - 1.00
    x_terreno_izq = x_pie_relleno - 3.50
    y_terreno_izq = y_pie_relleno - 1.20

    x_borde_der = x_eje + (b_calzada / 2.0)
    y_borde_der = y_eje - (b_calzada / 2.0) * p_bombeo
    x_sobreancho = x_borde_der + s_sobreancho
    y_sobreancho = y_borde_der - s_sobreancho * p_bombeo

    x_cuneta_fin = x_sobreancho + w_cuneta
    y_cuneta_fin = y_sobreancho
    x_cuneta_fondo = x_sobreancho + (w_cuneta / 2.0)
    y_cuneta_fondo = y_sobreancho - d_cuneta

    yn_cuneta = 0.124
    w_espejo_agua = (yn_cuneta / d_cuneta) * w_cuneta
    x_agua_izq = x_cuneta_fondo - (w_espejo_agua / 2.0)
    x_agua_der = x_cuneta_fondo + (w_espejo_agua / 2.0)
    y_agua = y_cuneta_fondo + yn_cuneta

    dx_banco = h_banco * talud_h
    x_banco1_pie, y_banco1_pie = x_cuneta_fin, y_cuneta_fin
    x_banco1_top, y_banco1_top = x_banco1_pie + dx_banco, y_banco1_pie + h_banco
    x_banq1_fin, y_banq1_fin = x_banco1_top + w_banqueta, y_banco1_top + (w_banqueta * 0.02)
    x_banco2_top, y_banco2_top = x_banq1_fin + dx_banco, y_banq1_fin + h_banco
    x_banq2_fin, y_banq2_fin = x_banco2_top + w_banqueta, y_banco2_top + (w_banqueta * 0.02)
    x_banco3_top, y_banco3_top = x_banq2_fin + dx_banco, y_banq2_fin + h_banco
    x_terreno_der, y_terreno_der = x_banco3_top + 5.50, y_banco3_top + 1.80

    cuerpo = [
        _linea(x_berma_izq, y_berma_izq, x_borde_izq, y_borde_izq, "PA14-CONTORNO"),
        _linea(x_borde_izq, y_borde_izq, x_eje, y_eje, "PA14-CONTORNO"),
        _linea(x_eje, y_eje, x_borde_der, y_borde_der, "PA14-CONTORNO"),
        _linea(x_borde_der, y_borde_der, x_sobreancho, y_sobreancho, "PA14-CONTORNO"),
        _linea(x_borde_der, y_borde_der - 0.20, x_borde_der, y_borde_der + 0.20, "PA14-SIMBOLOS"),
        _linea(x_sobreancho, y_sobreancho, x_cuneta_fondo, y_cuneta_fondo, "PA14-OBRAS-ARTE"),
        _linea(x_cuneta_fondo, y_cuneta_fondo, x_cuneta_fin, y_cuneta_fin, "PA14-OBRAS-ARTE"),
        _linea(x_sobreancho, y_sobreancho, x_cuneta_fin, y_cuneta_fin, "PA14-OBRAS-ARTE"),
        _linea(x_agua_izq, y_agua, x_agua_der, y_agua, "PA14-OBRAS-ARTE"),
        _linea(x_cuneta_fondo, y_cuneta_fondo, x_cuneta_fondo, y_agua, "PA14-SIMBOLOS"),
        _linea(x_banco1_pie, y_banco1_pie, x_banco1_top, y_banco1_top, "PA14-CONTORNO"),
        _linea(x_banco1_top, y_banco1_top, x_banq1_fin, y_banq1_fin, "PA14-CONTORNO"),
        _linea(x_banq1_fin, y_banq1_fin, x_banco2_top, y_banco2_top, "PA14-CONTORNO"),
        _linea(x_banco2_top, y_banco2_top, x_banq2_fin, y_banq2_fin, "PA14-CONTORNO"),
        _linea(x_banq2_fin, y_banq2_fin, x_banco3_top, y_banco3_top, "PA14-CONTORNO"),
        _linea(x_banco3_top, y_banco3_top, x_terreno_der, y_terreno_der, "PA14-CONTORNO"),
        _linea(x_berma_izq, y_berma_izq, x_pie_relleno, y_pie_relleno, "PA14-CONTORNO"),
        _linea(x_pie_relleno, y_pie_relleno, x_terreno_izq, y_terreno_izq, "PA14-CONTORNO"),
        _linea(x_eje, y_eje - 1.80, x_eje, y_eje + 6.00, "PA14-EJE"),
        _rect(x_eje + 0.30, y_borde_der, 2.55, 3.80, "PA14-GALIBO"),
        _cota(x_berma_izq, y_berma_izq, x_borde_izq, y_borde_izq, (x_berma_izq + x_borde_izq) / 2.0, y_eje - 1.00, f"Berma {b_berma:.2f} m"),
        _cota(x_borde_izq, y_borde_izq, x_borde_der, y_borde_der, x_eje, y_eje - 1.00, f"Calzada {b_calzada:.2f} m"),
        _cota(x_borde_der, y_borde_der, x_sobreancho, y_sobreancho, (x_borde_der + x_sobreancho) / 2.0, y_eje - 1.00, f"S = {s_sobreancho:.2f} m"),
        _cota(x_sobreancho, y_sobreancho, x_cuneta_fin, y_cuneta_fin, x_cuneta_fondo, y_eje - 1.00, f"Cuneta {w_cuneta:.2f} m"),
        _cota(x_banco1_pie, y_banco1_pie, x_banco1_top, y_banco1_pie, (x_banco1_pie + x_banco1_top) / 2.0, y_banco1_pie - 1.70, f"{dx_banco:.2f} m (0.5H)"),
        _cota(x_banco1_top, y_banco1_pie, x_banco1_top, y_banco1_top, x_banco1_top + 1.20, (y_banco1_pie + y_banco1_top) / 2.0, f"H = {h_banco:.2f} m"),
        _cota(x_banco1_top, y_banco1_top, x_banq1_fin, y_banco1_top, (x_banco1_top + x_banq1_fin) / 2.0, y_banco1_top - 1.00, f"Banqueta {w_banqueta:.2f} m"),
        _cota(x_banco2_top, y_banq1_fin, x_banco2_top, y_banco2_top, x_banco2_top + 1.20, (y_banq1_fin + y_banco2_top) / 2.0, f"H = {h_banco:.2f} m"),
        _cota(x_banco2_top, y_banco2_top, x_banq2_fin, y_banco2_top, (x_banco2_top + x_banq2_fin) / 2.0, y_banco2_top - 1.00, f"Banqueta {w_banqueta:.2f} m"),
        _texto(x_eje - 11.50, y_eje + 21.00, 0.50, "SECCION TRANSVERSAL TIPICA - CORTE Y BANQUETAS DE ACCESO", "PA14-TEXTO"),
        _texto(x_eje - 11.50, y_eje + 20.00, 0.30, "Autodesk Civil 3D Subassembly | Estandar DG-2018 MTC", "PA14-TEXTO"),
        _texto(x_eje + 0.50, y_borde_der + 2.00, 0.25, "Volvo FMX 8x4 (C3/C4)", "PA14-TEXTO"),
        _texto(x_banco1_top - 1.20, (y_banco1_pie + y_banco1_top) / 2.0, 0.25, "Talud 0.5H:1V (63.43 deg)", "PA14-TEXTO"),
        _texto((x_banco1_top + x_banq1_fin) / 2.0 - 1.50, y_banco1_top + 0.35, 0.22, "Banqueta Resguardo (+2.0% drenaje)", "PA14-TEXTO"),
        _texto(x_eje + 0.20, y_eje + 5.50, 0.25, "EJE VIAL (CL)", "PA14-EJE"),
    ]

    x_c, y_c, w_c, h_c = x_eje - 11.80, y_eje + 18.50, 10.50, 14.50
    cuerpo.append(_rect(x_c, y_c - h_c, w_c, h_c, "PA14-EDIFICACION"))
    cuerpo.append(_rect(x_c + 0.15, y_c - h_c + 0.15, w_c - 0.30, h_c - 0.30, "PA14-CONTORNO"))
    cuerpo.append(_texto(x_c + 0.50, y_c - 0.90, 0.30, "PARAMETROS DE DISENO VIAL DG-2018", "PA14-TEXTO"))
    cuerpo.append(_linea(x_c + 0.30, y_c - 1.25, x_c + w_c - 0.30, y_c - 1.25, "PA14-EJE"))

    vol_corte = float(c3d.get("volumen_total_corte_m3", 76105.14))
    vol_relleno = float(c3d.get("volumen_total_relleno_m3", 27.03))

    datos_cuadro = [
        "Norma: MTC DG-2018 (Orografia Tipo 4)",
        "Velocidad Directriz: V = 30 km/h",
        "Radio Minimo en Curva: R = 15.00 m",
        "Vehiculo: Camion Volvo FMX 8x4 (L=5.10m)",
        f"Sobreancho DG-2018: S = {s_sobreancho:.2f} m",
        f"Calzada Ampliada: B = {b_calzada + s_sobreancho:.2f} m",
        "Talud de Desmonte: 0.5H:1V (63.43 deg)",
        "Q-Slope Estable: 63.42 deg (Compatible)",
        f"Banqueta Resguardo: Wb = {w_banqueta:.2f} m @ Hb = {h_banco:.2f} m",
        "Longitud Alineamientos: L = 979.13 m",
        f"Volumen Total Corte: {vol_corte:,.2f} m3",
        f"Volumen Relleno: {vol_relleno:,.2f} m3",
        "--- HIDRAULICA DE DRENAJE (MANNING) ---",
        "Cuneta Triangular: T=1.00m, H=0.35m (e=7.5cm)",
        "Q_diseno (Tr=25a): 49.1 l/s | Q_max: 382 l/s",
        "Tirante yn: 12.4 cm | Borde Libre: 22.6 cm",
        "Velocidad: V=1.95 m/s (0.60 <= V <= 4.50)",
        "Froude: Fr=2.50 (Supercritico - Conforme)",
    ]

    for idx, d_txt in enumerate(datos_cuadro):
        cuerpo.append(_texto(x_c + 0.50, y_c - 1.85 - (idx * 0.75), 0.22, d_txt, "PA14-TEXTO"))

    return Dibujo(
        "PA14_CORTES_ACCESOS",
        "Seccion Transversal Tipica - Cortes de Explanacion y Banquetas (Civil 3D DG-2018)",
        cuerpo,
        x_terreno_der + 2.0,
    )
