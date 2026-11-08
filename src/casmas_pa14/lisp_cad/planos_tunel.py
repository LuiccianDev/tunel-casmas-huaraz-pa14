"""Generadores AutoLISP de sección transversal, perfil geológico y plano de ubicación."""

from __future__ import annotations

from .nucleo import (
    Dibujo,
    _cota,
    _cota_angular,
    _hatch_cunetas,
    _linea,
    _n,
    _rect,
    _texto,
    _texto_cen,
)


def dibujo_seccion(sec: dict) -> Dibujo:
    """Sección típica con veredas, cunetas, calzada con bombeo y cotas normalizadas."""
    b, h, hw = sec["ancho_m"], sec["altura_m"], sec["hastial_m"]
    e = sec["espesor_rasante_m"]
    hr = sec.get("altura_rasante_m", h - e)
    v = sec["vereda_m"]
    berma = sec["berma_m"]
    carril = sec["ancho_carril_m"]
    separador = sec["separador_m"]
    wg, hg = sec["ancho_galibo_m"], sec["altura_galibo_m"]
    ac = sec.get("cuneta_ancho_m", 1.20)
    hc = sec.get("cuneta_prof_m", 0.40)
    bombeo = sec.get("bombeo_pct", 2.0) / 100.0

    x_eje = b / 2
    x_cuneta_izq = v + ac  # 1.95
    x_berma_izq = v + berma  # 2.55
    x_carril_izq = x_berma_izq + carril  # 6.15
    x_separador_der = x_carril_izq + separador  # 7.15
    x_carril_der = x_separador_der + carril  # 10.75
    x_cuneta_der = b - (v + ac)  # 11.35
    x_vereda_der = b - v  # 12.55

    # Bombeo sobre calzada desde cuneta hasta separador
    dy_bombeo = (x_carril_izq - x_cuneta_izq) * bombeo
    y_calzada_eje = e + dy_bombeo

    pts_contorno = f"'((0.0 0.0) ({_n(b)} 0.0) ({_n(b)} {_n(hw)}) (0.0 {_n(hw)}))"
    pts_cuneta_izq = (
        f"'(({_n(v)} {_n(e)}) ({_n(v)} {_n(e - hc)}) ({_n(x_cuneta_izq)} {_n(e)}))"
    )
    pts_cuneta_der = f"'(({_n(x_cuneta_der)} {_n(e)}) ({_n(x_vereda_der)} {_n(e - hc)}) ({_n(x_vereda_der)} {_n(e)}))"

    cuerpo = [
        # 1. Contorno de excavación
        f'(pa14:pline {pts_contorno} \'(0.0 0.0 1.0 0.0) T "PA14-CONTORNO")',
        # 2. Rasante de fondo y divisiones de subbase (y=0 a y=e)
        _linea(0, e, b, e, "PA14-CONTORNO"),
        _linea(v, 0, v, e, "PA14-CONTORNO"),
        _linea(x_berma_izq, 0, x_berma_izq, e, "PA14-CONTORNO"),
        _linea(x_carril_izq, 0, x_carril_izq, e, "PA14-CONTORNO"),
        _linea(x_separador_der, 0, x_separador_der, e, "PA14-CONTORNO"),
        _linea(x_carril_der, 0, x_carril_der, e, "PA14-CONTORNO"),
        _linea(x_vereda_der, 0, x_vereda_der, e, "PA14-CONTORNO"),
        # Galería / ducto en subbase derecha
        _rect(x_carril_der + 0.60, 0.0, 1.20, e, "PA14-CONTORNO"),
        # 3. Veredas y cunetas
        _linea(0, e, v, e, "PA14-OBRAS-ARTE"),
        f'(pa14:pline {pts_cuneta_izq} \'(0.0 0.0 0.0) T "PA14-OBRAS-ARTE")',
        _linea(
            x_cuneta_izq, e, x_carril_izq, y_calzada_eje, "PA14-CONTORNO"
        ),  # calzada izq
        _rect(
            x_carril_izq, y_calzada_eje, separador, 0.20, "PA14-CONTORNO"
        ),  # separador central
        _linea(
            x_separador_der, y_calzada_eje, x_cuneta_der, e, "PA14-CONTORNO"
        ),  # calzada der
        f'(pa14:pline {pts_cuneta_der} \'(0.0 0.0 0.0) T "PA14-OBRAS-ARTE")',
        *_hatch_cunetas(v, e, ac, hc, b),
        _linea(x_vereda_der, e, b, e, "PA14-OBRAS-ARTE"),
        # 4. Gálibo y ejes
        _rect(v, e, wg, hg, "PA14-GALIBO"),
        _linea(x_eje, -0.8, x_eje, h + 0.6, "PA14-EJE"),
        _linea(0, hw, b, hw, "PA14-EJE"),
        # 5. Cotas inferiores (parciales y total)
        _cota(0.0, 0.0, v, 0.0, v / 2, -1.15, f"{v:.2f} m"),
        _cota(
            v,
            0.0,
            x_berma_izq,
            0.0,
            (v + x_berma_izq) / 2,
            -0.65,
            f"{berma:.2f} m",
        ),
        _cota(
            x_berma_izq,
            0.0,
            x_carril_izq,
            0.0,
            (x_berma_izq + x_carril_izq) / 2,
            -0.65,
            f"{carril:.2f} m",
        ),
        _cota(
            x_carril_izq,
            0.0,
            x_separador_der,
            0.0,
            x_eje,
            -0.65,
            f"{separador:.2f} m",
        ),
        _cota(0.0, 0.0, b, 0.0, x_eje, -1.75, f"{b:.2f} m"),
        # 6. Cotas de detalle (cuneta, subrasante y bombeo)
        _cota(
            v,
            e,
            x_cuneta_izq,
            e,
            (v + x_cuneta_izq) / 2,
            e + 0.40,
            f"{ac:.2f} m",
        ),
        _cota(v, e - hc, v, e, v - 0.40, e - hc / 2, f"{hc:.2f} m"),
        _cota(x_eje, 0.0, x_eje, e, x_eje - 0.75, e / 2, f"{e:.2f} m"),
        _cota_angular(
            x_cuneta_der,
            e,
            x_separador_der,
            e,
            x_separador_der,
            y_calzada_eje,
            x_separador_der + 1.20,
            e + dy_bombeo * 0.70,
            f"{sec.get('bombeo_pct', 2.0):.0f}%%d",
        ),
        # 7. Cotas verticales (alturas y gálibo a la izquierda)
        _cota(v, e, v, e + hg, -0.65, e + hg / 2, f"{hg:.2f} m"),
        _cota(
            v,
            e + hg,
            v,
            h,
            -0.65,
            (e + hg + h) / 2,
            f"{h - (e + hg):.2f} m",
        ),
        _cota(0.0, e, 0.0, h, -1.25, (e + h) / 2, f"{hr:.2f} m"),
        _cota(0.0, 0.0, 0.0, h, -1.85, h / 2, f"{h:.2f} m"),
        # 8. Textos
        _texto(0.0, h + 0.80, 0.35, f"SECCION TIPICA - {h:.2f} m x {b:.2f} m"),
        _texto(
            0.0,
            -2.40,
            0.20,
            f"A = {sec['area_m2']:.2f} m2   R = {sec['radio_m']:.2f} m   "
            f"Galibo = {wg:.2f} x {hg:.2f} m",
        ),
    ]
    return Dibujo("PA14_SECCION", "Sección típica del túnel", cuerpo, b + 4)


def dibujo_geologia(geo: dict) -> Dibujo:
    """Corte geologico longitudinal del tunel (L = 5,556 m)."""
    cuerpo = []
    tramos = geo.get("tramos", [])
    if not tramos:
        return Dibujo("PA14_GEOLOGIA", "Corte Geologico Longitudinal", [], 100.0)

    prog_ini = min(t["progresiva_inicio"] for t in tramos)
    prog_fin = max(t["progresiva_fin"] for t in tramos)
    longitud = prog_fin - prog_ini

    y_top = 220.0
    y_bot = -60.0
    y_tunel = 0.0
    h_exc = 9.58  # altura de excavacion

    # 1. Contorno general del macizo rocoso
    cuerpo.append(_rect(prog_ini, y_bot, longitud, y_top - y_bot, "PA14-CONTORNO"))

    # 2. Eje rasante y linea de clave del tunel
    cuerpo.append(_linea(prog_ini, y_tunel, prog_fin, y_tunel, "PA14-EJE"))
    cuerpo.append(
        _linea(prog_ini, y_tunel + h_exc, prog_fin, y_tunel + h_exc, "PA14-GALIBO")
    )
    cuerpo.append(
        _texto(
            prog_ini - 240.0,
            y_tunel + 2.0,
            12.0,
            "RASANTE DEL TUNEL",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _texto(
            prog_ini - 240.0,
            y_tunel + h_exc,
            10.0,
            "CLAVE (EXCAVACION)",
            "PA14-TEXTO",
        )
    )

    # 3. Encabezado del plano longitudinal
    cuerpo.append(
        _texto(
            prog_ini,
            y_top + 25.0,
            22.0,
            "PERFIL GEOLOGICO LONGITUDINAL - TUNEL TRASANDINO PA14 (L = 5,556.00 m)",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _texto(
            prog_ini,
            y_top + 8.0,
            12.0,
            "Escala Horizontal 1:1 (metros) | Contactos Litologicos, Buzamiento, RMR y Q-Slope",
            "PA14-TEXTO",
        )
    )

    # 4. Tramos litologicos y contactos geologicos
    for t in tramos:
        x_ini = t["progresiva_inicio"]
        x_fin = t["progresiva_fin"]
        l_tramo = x_fin - x_ini
        x_mid = (x_ini + x_fin) / 2.0
        tipo = t.get("tipo_roca", "")
        rmr = t.get("rmr", 0)
        q_slope = t.get("q_slope", 0.0)

        dx_buz = 45.0
        if x_ini > prog_ini:
            cuerpo.append(
                _linea(
                    x_ini - 10.0,
                    y_bot,
                    x_ini + dx_buz,
                    y_top,
                    "PA14-ESTRUCTURA",
                )
            )

        cuerpo.append(_linea(x_ini, y_bot, x_ini, y_bot - 15.0, "PA14-EJE"))
        cuerpo.append(
            _texto_cen(
                x_ini,
                y_bot - 30.0,
                10.0,
                f"KM {x_ini / 1000.0:.3f}",
                "PA14-TEXTO",
            )
        )

        cuerpo.append(_texto_cen(x_mid, y_top - 35.0, 14.0, tipo, "PA14-TEXTO"))
        cuerpo.append(
            _texto_cen(
                x_mid,
                y_top - 60.0,
                10.0,
                f"RMR = {rmr} | Q-Slope = {q_slope:.3f}",
                "PA14-TEXTO",
            )
        )

        cuerpo.append(
            _cota(
                x_ini,
                y_bot - 55.0,
                x_fin,
                y_bot - 55.0,
                x_mid,
                y_bot - 70.0,
                f"L={l_tramo:.1f}m",
            )
        )

    cuerpo.append(_linea(prog_fin, y_bot, prog_fin, y_bot - 15.0, "PA14-EJE"))
    cuerpo.append(
        _texto_cen(
            prog_fin,
            y_bot - 30.0,
            10.0,
            f"KM {prog_fin / 1000.0:.3f}",
            "PA14-TEXTO",
        )
    )

    return Dibujo(
        "PA14_GEOLOGIA",
        "Corte Geologico Longitudinal del Tunel (0+000 a 5+556)",
        cuerpo,
        longitud + 400.0,
    )


def dibujo_ubicacion(ub: dict) -> Dibujo:
    """Puntos del proyecto en coordenadas UTM reales (X = Este, Y = Norte)."""
    puntos = ub["puntos"]
    pe, ps = puntos["PE"], puntos["PS"]
    cuerpo = [_linea(pe["este"], pe["norte"], ps["este"], ps["norte"], "PA14-EJE")]
    for pt in puntos.values():
        x, y = pt["este"], pt["norte"]
        cuerpo += [
            _rect(x - 15.0, y - 15.0, 30.0, 30.0, "PA14-CONTORNO"),
            _texto(x + 25.0, y + 25.0, 30.0, pt["nombre"]),
            _texto(
                x + 25.0,
                y - 15.0,
                18.0,
                f"E {x:.2f}  N {y:.2f}  Z {pt['cota']:.0f} m",
            ),
        ]
    xs = [pt["este"] for pt in puntos.values()]
    return Dibujo(
        "PA14_UBICACION",
        "Plano de ubicacion - UTM WGS84 18L",
        cuerpo,
        max(xs) - min(xs) + 500.0,
    )
