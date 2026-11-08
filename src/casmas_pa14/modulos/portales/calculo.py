"""Cálculo volumétrico, Q-slope, sobreancho DG-2018 y drenaje Manning para 11 · Portales."""

from __future__ import annotations

import math
from typing import Any

from .progresivas import calcular_control_progresivas


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    portales = p["portales"]
    banquetas = portales["banquetas"]
    factor_esponjamiento = float(portales["factor_esponjamiento"])
    resultados = []
    volumen_total_insitu = 0.0
    volumen_total_esponjado = 0.0

    for b in banquetas:
        h = float(b["altura_banco_m"])
        largo = float(b["largo_banco_m"])
        alpha = float(b["angulo_talud_deg"])
        beta = float(b["angulo_perfil_deg"])
        w = float(
            b["ancho_plataforma_m"] if "ancho_plataforma_m" in b else b["lado_mayor_m"]
        )

        base_talud = (
            h / math.tan(math.radians(alpha)) if (alpha != 90 and alpha > 0) else 0.0
        )
        area_talud = 0.5 * h * base_talud
        area_rect = w * h
        area_excavacion = max(0.0, area_rect - area_talud)

        vol_insitu = area_excavacion * largo
        vol_esponjado = vol_insitu * factor_esponjamiento
        volumen_total_insitu += vol_insitu
        volumen_total_esponjado += vol_esponjado

        resultados.append(
            {
                "id": str(b["id"]),
                "largo": round(largo, 3),
                "altura": round(h, 3),
                "ancho": round(w, 3),
                "alpha": round(alpha, 1),
                "beta": round(beta, 1),
                "base_talud": round(base_talud, 4),
                "area_excavacion": round(area_excavacion, 4),
                "vol_insitu": round(vol_insitu, 2),
                "factor_esp": factor_esponjamiento,
                "vol_esponjado": round(vol_esponjado, 2),
            }
        )

    q_slope_res = None
    if "q_slope" in portales:
        qs = portales["q_slope"]
        rqd = float(qs.get("rqd", 50.0))
        jn = float(qs.get("jn", 9.0))
        jr = float(qs.get("jr", 1.5))
        ja = float(qs.get("ja", 3.0))
        jw = float(qs.get("jw", 0.75))
        srfa = float(qs.get("srfa", 2.5))
        qslope_calc = (rqd / jn) * (jr / ja) * (jw / srfa)
        angulo_calc = 20.0 * math.log10(qslope_calc) + 65.0
        q_slope_res = {
            "rqd": rqd,
            "jn": jn,
            "jr": jr,
            "ja": ja,
            "jw": jw,
            "srfa": srfa,
            "q_slope": round(qslope_calc, 4),
            "angulo_estable_deg": round(angulo_calc, 2),
        }

    dg2018_res = None
    if "dg2018_geometria" in portales:
        dg = portales["dg2018_geometria"]
        v = float(dg.get("velocidad_diseno_kph", 30.0))
        r = float(dg.get("radio_minimo_curvatura_m", 15.0))
        l_ejes = float(dg.get("distancia_ejes_vehiculo_m", 5.10))
        n = int(dg.get("numero_carriles", 1))
        s_calc = n * (r - math.sqrt(r**2 - l_ejes**2)) + v / (10.0 * math.sqrt(r))
        ancho_base = 3.60
        dg2018_res = {
            "clasificacion_via": str(dg.get("clasificacion_via", "Trocha de Acceso")),
            "velocidad_diseno_kph": v,
            "radio_minimo_curvatura_m": r,
            "distancia_ejes_vehiculo_m": l_ejes,
            "numero_carriles": n,
            "sobreancho_calculado_m": round(s_calc, 2),
            "ancho_calzada_base_m": ancho_base,
            "ancho_calzada_ampliada_m": round(ancho_base + s_calc, 2),
            "talud_corte_h_v": str(dg.get("talud_corte_h_v", "0.5:1")),
            "angulo_talud_corte_deg": float(dg.get("angulo_talud_corte_deg", 63.43)),
            "bombeo_calzada_pct": float(dg.get("bombeo_calzada_pct", -2.0)),
            "ancho_banqueta_resguardo_m": float(
                dg.get("ancho_banqueta_resguardo_m", 5.0)
            ),
            "altura_max_banco_m": float(dg.get("altura_max_banco_m", 6.0)),
            "pendiente_banqueta_pct": float(dg.get("pendiente_banqueta_pct", 2.0)),
            "diametro_giro_cat966h_m": float(
                dg.get("diametro_giro_cargador_cat966h_m", 14.73)
            ),
            "ancho_plataforma_emboquille_m": float(
                dg.get("ancho_plataforma_emboquille_m", 28.53)
            ),
        }

    c3d = portales.get("cortes_civil3d", {})

    drenaje_res = None
    if "drenaje_cunetas" in portales:
        dc = portales["drenaje_cunetas"]
        i_lluvia = float(dc.get("intensidad_precipitacion_mm_h", 65.0))
        c_escorr = float(dc.get("coeficiente_escorrentia", 0.85))
        n_manning = float(dc.get("rugosidad_manning_concreto", 0.015))
        v_min = float(dc.get("velocidad_minima_flujo_m_s", 0.60))
        v_max = float(dc.get("velocidad_maxima_flujo_m_s", 4.50))
        bl_min = float(dc.get("borde_libre_minimo_m", 0.10))

        cunetas_lista = []
        tipos_cunetas = [
            ("cuneta_acceso_tunel", "Cuneta Acceso Túnel B"),
            ("cuneta_banquetas", "Cuneta Banquetas de Portal"),
            ("cuneta_coronacion", "Zanja de Coronación de Ladera"),
        ]

        for clave_cuneta, etiqueta in tipos_cunetas:
            cfg = dc.get(clave_cuneta, {})
            if cfg:
                t_sup = float(cfg.get("ancho_superior_m", 1.00))
                h_prof = float(cfg.get("profundidad_total_m", 0.35))
                z1 = float(cfg.get("talud_lado_calzada_z1", 1.43))
                z2 = float(cfg.get("talud_lado_corte_z2", 1.43))
                s_pct = float(cfg.get("pendiente_longitudinal_pct", 2.50))
                s_m_m = s_pct / 100.0
                l_tramo = float(cfg.get("longitud_tramo_m", 200.00))
                w_trib = float(cfg.get("ancho_tributario_m", 16.00))

                area_trib_m2 = l_tramo * w_trib
                area_trib_ha = area_trib_m2 / 10000.0

                qp_m3_s = (c_escorr * i_lluvia * area_trib_ha) / 360.0
                qp_l_s = qp_m3_s * 1000.0

                z_sum = z1 + z2
                area_max_m2 = 0.5 * t_sup * h_prof
                p_max_m = h_prof * (math.sqrt(1.0 + z1**2) + math.sqrt(1.0 + z2**2))
                rh_max_m = area_max_m2 / p_max_m if p_max_m > 0 else 0.0

                q_max_m3_s = (
                    (1.0 / n_manning)
                    * area_max_m2
                    * (rh_max_m ** (2.0 / 3.0))
                    * math.sqrt(s_m_m)
                )
                q_max_l_s = q_max_m3_s * 1000.0

                kp = math.sqrt(1.0 + z1**2) + math.sqrt(1.0 + z2**2)
                ka = 0.5 * z_sum
                factor_geom = ka * ((ka / kp) ** (2.0 / 3.0))

                yn_m = ((qp_m3_s * n_manning) / (factor_geom * math.sqrt(s_m_m))) ** (
                    3.0 / 8.0
                )
                yn_cm = yn_m * 100.0

                bl_m = h_prof - yn_m
                bl_cm = bl_m * 100.0

                an_m2 = ka * (yn_m**2)
                vn_m_s = qp_m3_s / an_m2 if an_m2 > 0 else 0.0

                yh_m = yn_m / 2.0
                froude = vn_m_s / math.sqrt(9.81 * yh_m) if yh_m > 0 else 0.0
                fs_hidr = q_max_m3_s / qp_m3_s if qp_m3_s > 0 else 99.0

                cumple_bl = bl_m >= bl_min
                cumple_v_min = vn_m_s >= v_min
                cumple_v_max = vn_m_s <= v_max

                cunetas_lista.append(
                    {
                        "id": clave_cuneta,
                        "nombre": str(cfg.get("nombre", etiqueta)),
                        "ancho_superior_m": round(t_sup, 3),
                        "profundidad_total_m": round(h_prof, 3),
                        "talud_z1": round(z1, 2),
                        "talud_z2": round(z2, 2),
                        "pendiente_pct": round(s_pct, 2),
                        "longitud_m": round(l_tramo, 2),
                        "area_cuenca_ha": round(area_trib_ha, 4),
                        "caudal_diseno_l_s": round(qp_l_s, 2),
                        "capacidad_max_l_s": round(q_max_l_s, 2),
                        "tirante_normal_cm": round(yn_cm, 2),
                        "borde_libre_cm": round(bl_cm, 2),
                        "velocidad_flujo_m_s": round(vn_m_s, 2),
                        "froude": round(froude, 2),
                        "regimen": "Supercrítico" if froude > 1.0 else "Subcrítico",
                        "factor_seguridad_hidraulico": round(fs_hidr, 2),
                        "estado_normativo": (
                            "CONFORME (MTC)"
                            if (cumple_bl and cumple_v_min and cumple_v_max)
                            else "OBSERVADO"
                        ),
                    }
                )

        drenaje_res = {
            "periodo_retorno_anos": int(dc.get("periodo_retorno_anos", 25)),
            "intensidad_lluvia_mm_h": i_lluvia,
            "coeficiente_escorrentia": c_escorr,
            "rugosidad_manning": n_manning,
            "velocidad_min_m_s": v_min,
            "velocidad_max_m_s": v_max,
            "borde_libre_min_m": bl_min,
            "cunetas": cunetas_lista,
        }

    return {
        "banquetas": resultados,
        "factor_esponjamiento": factor_esponjamiento,
        "volumen_total_insitu_m3": round(volumen_total_insitu, 2),
        "volumen_total_esponjado_m3": round(volumen_total_esponjado, 2),
        "q_slope": q_slope_res,
        "dg2018_geometria": dg2018_res,
        "cortes_civil3d": c3d,
        "drenaje_cunetas": drenaje_res,
        "control_progresivas": calcular_control_progresivas(portales),
    }
