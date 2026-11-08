"""Motor de cálculo de voladura de banquetas en superficie con Epiroc PowerROC T25 (Modelo Konya)."""

from __future__ import annotations

import math
from typing import Any


def calcular_voladura_banquetas(
    p: dict[str, Any], ctx: dict[str, Any]
) -> dict[str, Any]:
    """Calcula el modelo de bancos de C.J. Konya con Epiroc PowerROC T25 para las banquetas."""
    kt25 = p.get("voladura_banquetas", {})
    portales_ctx = ctx.get("portales", {})
    banquetas_lista = portales_ctx.get(
        "banquetas", p.get("portales", {}).get("banquetas", [])
    )

    de_t25_mm = float(kt25.get("diametro_broca_mm", 64.0))
    de_t25_in = de_t25_mm / 25.4
    exp_t25 = str(kt25.get("explosivo_base", "semexsa E-80"))
    rho_e_t25 = float(kt25.get("densidad_explosivo_g_cm3", 1.18))
    vod_t25 = float(kt25.get("vod_explosivo_m_s", 4500.0))
    pd_t25 = float(kt25.get("presion_detonacion_kbar", 86.0))
    roca_t25 = str(kt25.get("roca_base", "Diorita PA14 (Caso Base)"))
    rho_r_t25 = float(kt25.get("densidad_roca_g_cm3", 2.76))
    ucs_t25 = float(kt25.get("ucs_roca_mpa", 250.0))
    rt_t25 = float(kt25.get("resistencia_traccion_mpa", 18.0))
    fe_t25 = float(kt25.get("factor_esponjamiento", 1.50))
    h_t25 = float(kt25.get("altura_banco_m", 6.0))
    kd_t25 = float(kt25.get("factor_kd", 1.00))
    ks_t25 = float(kt25.get("factor_ks", 1.00))
    ke_t25 = float(kt25.get("factor_ke", 1.00))
    kt_t25 = float(kt25.get("factor_taco_kt", 0.85))
    kj_t25 = float(kt25.get("factor_sobreperforacion_kj", 0.30))
    ks_rel_t25 = float(kt25.get("factor_espaciamiento_ks_rel", 1.15))
    e0_t25 = float(kt25.get("error_perf_constante_m", 0.05))
    em_t25 = float(kt25.get("error_perf_pendiente_m_m", 0.03))
    vol_banco_req = float(kt25.get("volumen_banco_requerido_m3", 2500.0))
    largo_frente_m = float(kt25.get("largo_frente_banco_m", 50.0))
    ancho_frente_m = float(kt25.get("ancho_frente_banco_m", 20.0))
    rend_perf_m_h = float(kt25.get("rendimiento_perforadora_m_h", 25.0))
    w_buffer_kg = float(kt25.get("carga_pozo_buffer_kg", 12.0))
    kbp_buffer = float(kt25.get("relacion_fc_buffer_prod", 1.00))
    pb_precorte_mpa = float(kt25.get("presion_barreno_precorte_mpa", 75.0))
    ang_precorte_deg = float(kt25.get("angulo_inclinacion_precorte_deg", 20.0))

    diam_opt_mm = 8.0 * h_t25
    diam_max_mm = 15.0 * h_t25
    b_max_ft = 3.15 * de_t25_in * ((rho_e_t25 / rho_r_t25) ** (1.0 / 3.0))
    b_max_m = b_max_ft * 0.3048
    j_t25_m = kj_t25 * b_max_m
    l_t25_m = h_t25 + j_t25_m
    err_t25_m = e0_t25 + em_t25 * l_t25_m
    b_prac_t25_m = (b_max_m * kd_t25 * ks_t25 * ke_t25) - err_t25_m
    t_t25_m = kt_t25 * b_prac_t25_m
    lc_t25_m = max(0.0, l_t25_m - t_t25_m)
    s_t25_m = ks_rel_t25 * b_prac_t25_m
    s_seq_konya_m = (
        (h_t25 + 7.0 * b_prac_t25_m) / 8.0
        if h_t25 < 4.0 * b_prac_t25_m
        else 1.40 * b_prac_t25_m
    )
    ql_t25_kg_m = (math.pi * ((de_t25_mm / 1000.0) ** 2) / 4.0) * rho_e_t25 * 1000.0
    q_t25_kg = ql_t25_kg_m * lc_t25_m
    v_t25_m3 = b_prac_t25_m * s_t25_m * h_t25
    w_t25_ton = v_t25_m3 * rho_r_t25
    qv_t25_kg_m3 = q_t25_kg / v_t25_m3 if v_t25_m3 > 0 else 0.0
    qm_t25_kg_ton = q_t25_kg / w_t25_ton if w_t25_ton > 0 else 0.0
    fp_t25_g_ton = qm_t25_kg_ton * 1000.0
    ir_t25 = h_t25 / b_prac_t25_m if b_prac_t25_m > 0 else 0.0

    sbr_ratio = s_t25_m / b_prac_t25_m if b_prac_t25_m > 0 else 1.15
    b_buffer_m = (
        math.sqrt(
            (w_buffer_kg * 1000.0)
            / (fp_t25_g_ton * kbp_buffer * h_t25 * rho_r_t25 * sbr_ratio)
        )
        if fp_t25_g_ton > 0
        else 1.20
    )
    e_buffer_m = b_buffer_m * sbr_ratio
    e_precorte_in = de_t25_in * ((pb_precorte_mpa + rt_t25) / rt_t25)
    e_precorte_m = e_precorte_in * 0.0254
    l_precorte_m = h_t25 / math.cos(math.radians(ang_precorte_deg))

    n_taladros_banco = math.ceil(vol_banco_req / v_t25_m3) if v_t25_m3 > 0 else 0
    exp_total_banco_kg = n_taladros_banco * q_t25_kg
    metros_perf_banco_m = n_taladros_banco * l_t25_m

    desglose_banquetas = []
    tot_vol_banq = 0.0
    tot_tal_banq = 0
    tot_m_perf_banq = 0.0
    tot_h_perf_banq = 0.0
    tot_kg_exp_banq = 0.0

    for b in banquetas_lista:
        b_id = str(b.get("id", "Banqueta"))
        h_b = float(b.get("altura", b.get("altura_banco_m", 5.0)))
        vol_b = float(b.get("vol_insitu", 500.0))
        l_tal_b = h_b + j_t25_m
        v_tal_b = b_prac_t25_m * s_t25_m * h_b
        n_tal_tramo = math.ceil(vol_b / v_tal_b) if v_tal_b > 0 else 0
        m_perf_tramo = n_tal_tramo * l_tal_b
        h_perf_tramo = m_perf_tramo / rend_perf_m_h if rend_perf_m_h > 0 else 0.0
        lc_tramo = max(0.0, l_tal_b - t_t25_m)
        q_tal_tramo = lc_tramo * ql_t25_kg_m
        kg_exp_tramo = n_tal_tramo * q_tal_tramo

        tot_vol_banq += vol_b
        tot_tal_banq += n_tal_tramo
        tot_m_perf_banq += m_perf_tramo
        tot_h_perf_banq += h_perf_tramo
        tot_kg_exp_banq += kg_exp_tramo

        desglose_banquetas.append(
            {
                "id": b_id,
                "altura_m": round(h_b, 2),
                "vol_insitu_m3": round(vol_b, 2),
                "b_prac_m": round(b_prac_t25_m, 3),
                "s_prac_m": round(s_t25_m, 3),
                "j_m": round(j_t25_m, 3),
                "l_tal_m": round(l_tal_b, 2),
                "v_tal_m3": round(v_tal_b, 2),
                "n_taladros": n_tal_tramo,
                "metros_perf_m": round(m_perf_tramo, 2),
                "horas_t25_h": round(h_perf_tramo, 2),
                "q_tal_kg": round(q_tal_tramo, 2),
                "kg_explosivo": round(kg_exp_tramo, 2),
            }
        )

    return {
        "de_mm": de_t25_mm,
        "de_in": de_t25_in,
        "explosivo_base": exp_t25,
        "rho_e": rho_e_t25,
        "vod_m_s": vod_t25,
        "pd_kbar": pd_t25,
        "roca_base": roca_t25,
        "rho_r": rho_r_t25,
        "ucs_mpa": ucs_t25,
        "rt_mpa": rt_t25,
        "fe": fe_t25,
        "h_m": h_t25,
        "kd": kd_t25,
        "ks": ks_t25,
        "ke": ke_t25,
        "kt": kt_t25,
        "kj": kj_t25,
        "ks_rel": ks_rel_t25,
        "e0_m": e0_t25,
        "em_m_m": em_t25,
        "vol_banco_m3": vol_banco_req,
        "largo_frente_m": largo_frente_m,
        "ancho_frente_m": ancho_frente_m,
        "rend_perf_m_h": rend_perf_m_h,
        "w_buffer_kg": w_buffer_kg,
        "kbp_buffer": kbp_buffer,
        "pb_precorte_mpa": pb_precorte_mpa,
        "ang_precorte_deg": ang_precorte_deg,
        "diam_opt_mm": diam_opt_mm,
        "diam_max_mm": diam_max_mm,
        "b_max_ft": b_max_ft,
        "b_max_m": b_max_m,
        "j_m": j_t25_m,
        "l_m": l_t25_m,
        "e_m": err_t25_m,
        "b_prac_m": b_prac_t25_m,
        "t_m": t_t25_m,
        "lc_m": lc_t25_m,
        "s_m": s_t25_m,
        "s_seq_konya_m": s_seq_konya_m,
        "ql_kg_m": ql_t25_kg_m,
        "q_kg": q_t25_kg,
        "v_m3": v_t25_m3,
        "w_ton": w_t25_ton,
        "qv_kg_m3": qv_t25_kg_m3,
        "qm_kg_ton": qm_t25_kg_ton,
        "fp_g_ton": fp_t25_g_ton,
        "ir": ir_t25,
        "b_buffer_m": b_buffer_m,
        "e_buffer_m": e_buffer_m,
        "e_precorte_m": e_precorte_m,
        "l_precorte_m": l_precorte_m,
        "n_taladros_banco": n_taladros_banco,
        "exp_total_banco_kg": exp_total_banco_kg,
        "metros_perf_banco_m": metros_perf_banco_m,
        "banquetas_desglose": desglose_banquetas,
        "tot_vol_banq_m3": round(tot_vol_banq, 2),
        "tot_tal_banq": tot_tal_banq,
        "tot_m_perf_banq_m": round(tot_m_perf_banq, 2),
        "tot_h_perf_banq_h": round(tot_h_perf_banq, 2),
        "tot_kg_exp_banq": round(tot_kg_exp_banq, 2),
    }
