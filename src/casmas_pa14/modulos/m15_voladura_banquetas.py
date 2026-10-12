"""15 · Voladura de Banquetas y Portales en Superficie (Epiroc PowerROC T25 — Modelo de C.J. Konya).

Desarrolla exclusivamente el diseño de perforación y voladura en superficie (a cielo abierto)
para los cortes escalonados de las banquetas y taludes de los portales del Túnel Casmas Huaraz PA14,
empleando la perforadora hidráulica sobre orugas (Rockdrill) Epiroc PowerROC T25 con broca de botones
de Ø 64 mm (2.5", rosca T38/T45), el Modelo Matemático de Bancos de C.J. Konya (1990), el diseño de
Taladros de Amortiguamiento (Buffer) y Precorte (Pre-splitting) a 70°, y el desglose operativo para
los 5 tramos de banquetas de `11_Portales.xlsx`.
Nota: La perforación y voladura subterránea en el frente del túnel con el Jumbo de 3 brazos
Sandvik DT1131 se calcula por separado en `m12_voladura.py` (`12_Voladura.xlsx`).
"""

import math
from typing import Any

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "voladura_banquetas"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
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

    # 1. Modelo Matemático de Bancos de C.J. Konya (1990)
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

    # 2. Voladura Controlada de Taludes: Buffer y Precorte (Guía de Ejercicios Konya)
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

    # 3. Desglose por cada Banqueta real de 11_Portales.xlsx
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


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 15_Voladura_Banquetas.xlsx exclusivo para Banquetas con PowerROC T25."""
    kt25 = resultados
    vol_p = p.get("voladura", {})
    vb_p = p.get("voladura_banquetas", {})

    # 1. Hoja Calculadora_Konya_T25 (Perforadora Epiroc PowerROC T25 - Broca 64 mm + Buffer/Precorte)
    filas_t25 = [
        (
            "Diámetro de broca seleccionada (Epiroc PowerROC T25)",
            "De_t25",
            kt25["de_mm"],
            "mm",
            'Broca de botones 2.5" T38/T45 (06_Maquinaria)',
        ),
        (
            "Diámetro de broca en pulgadas",
            "De_in",
            "={De_t25}/25.4",
            "pulg",
            "De_in = De_t25 / 25.4",
        ),
        (
            "Explosivo comercial seleccionado",
            "Tipo_e",
            kt25["explosivo_base"],
            "-",
            "Catálogo Comercial (Hoja BD_Explosivos)",
        ),
        (
            "Densidad del explosivo",
            "rho_e",
            "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 4, FALSE), 1.18)",
            "g/cm³",
            "Búsqueda dinámica en BD_Explosivos",
        ),
        (
            "Velocidad de detonación (VOD)",
            "VOD_e",
            "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 5, FALSE), 4500)",
            "m/s",
            "Búsqueda dinámica en BD_Explosivos",
        ),
        (
            "Presión de detonación del explosivo",
            "Pd_e",
            "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 7, FALSE), 86)",
            "kbar",
            "Búsqueda dinámica en BD_Explosivos",
        ),
        (
            "Macizo rocoso del portal",
            "Tipo_r",
            kt25["roca_base"],
            "-",
            "Catálogo Geomecánico (Hoja BD_Rocas)",
        ),
        (
            "Densidad de la roca",
            "rho_r",
            "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 2, FALSE), 2.76)",
            "g/cm³",
            "Búsqueda dinámica en BD_Rocas",
        ),
        (
            "Resistencia compresiva uniaxial (UCS)",
            "UCS_r",
            "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 3, FALSE), 250)",
            "MPa",
            "Búsqueda dinámica en BD_Rocas",
        ),
        (
            "Factor de esponjamiento de la roca",
            "Fe_r",
            "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 4, FALSE), 1.50)",
            "-",
            "Búsqueda dinámica en BD_Rocas",
        ),
        (
            "Resistencia a la tracción de la roca",
            "RT_r",
            kt25["rt_mpa"],
            "MPa",
            "Criterio mecánico en roca dura (Konya)",
        ),
        (
            "Altura de banco de diseño en banquetas",
            "H_b",
            kt25["h_m"],
            "m",
            "11_Portales (Banquetas H = 5.0 - 6.0 m)",
        ),
        (
            "Diámetro óptimo según altura de banco (8*H)",
            "D_opt",
            "=8*{H_b}",
            "mm",
            "Criterio Konya UNT: D_opt = 8 * H_b",
        ),
        (
            "Diámetro máximo admisible según banco (15*H)",
            "D_max",
            "=15*{H_b}",
            "mm",
            "Criterio Konya UNT: D_max = 15 * H_b",
        ),
        (
            "Factor de corrección por estratificación",
            "Kd_b",
            kt25["kd"],
            "-",
            "C.J. Konya (1.00 caso base)",
        ),
        (
            "Factor de corrección geológica",
            "Ks_b",
            kt25["ks"],
            "-",
            "C.J. Konya (1.00 caso base)",
        ),
        (
            "Factor de acoplamiento explosivo",
            "Ke_b",
            kt25["ke"],
            "-",
            "C.J. Konya (1.00 encartuchado atacado)",
        ),
        (
            "Relación de Taco (T / B)",
            "kt_b",
            kt25["kt"],
            "-",
            "Konya (0.70 estratificada a 1.00 masiva)",
        ),
        (
            "Relación de Sobreperforación (J / B_max)",
            "kj_b",
            kt25["kj"],
            "-",
            "Konya (J = 0.30 * B_max)",
        ),
        (
            "Relación de Espaciamiento (S / B)",
            "ks_rel",
            kt25["ks_rel"],
            "-",
            "Konya roca dura (1.15 a 1.40)",
        ),
        (
            "Error constante de emboquille",
            "e0",
            kt25["e0_m"],
            "m",
            "Konya: e = 0.05 + 0.03 * L",
        ),
        (
            "Desviación angular de perforación",
            "em",
            kt25["em_m_m"],
            "m/m",
            "Konya: 0.03 m por metro perforado",
        ),
        (
            "Burden máximo teórico (pies)",
            "B_max_ft",
            "=3.15*{De_in}*({rho_e}/{rho_r})^(1/3)",
            "pies",
            "B_max(ft) = 3.15 * De(in) * (rho_e / rho_r)^(1/3)",
        ),
        (
            "Burden máximo teórico (m)",
            "B_max",
            "={B_max_ft}*0.3048",
            "m",
            "B_max(m) = B_max(ft) * 0.3048",
        ),
        (
            "Sobreperforación (Pasadura)",
            "J_b",
            "={kj_b}*{B_max}",
            "m",
            "J = kj * B_max",
        ),
        (
            "Longitud total de perforación",
            "L_b",
            "={H_b}+{J_b}",
            "m",
            "L = H_b + J_b",
        ),
        (
            "Error total de perforación",
            "e_perf",
            "={e0}+{em}*{L_b}",
            "m",
            "e = 0.05 + 0.03 * L_b",
        ),
        (
            "Burden práctico ajustado",
            "B_p",
            "=({B_max}*{Kd_b}*{Ks_b}*{Ke_b})-{e_perf}",
            "m",
            "B_p = (B_max * Kd * Ks * Ke) - e",
        ),
        (
            "Longitud del Taco (Retacado)",
            "T_b",
            "={kt_b}*{B_p}",
            "m",
            "T_b = kt * B_p",
        ),
        (
            "Longitud de columna explosiva",
            "L_c",
            "=MAX(0, {L_b}-{T_b})",
            "m",
            "L_c = L_b - T_b",
        ),
        (
            "Espaciamiento práctico de diseño",
            "S_p",
            "={ks_rel}*{B_p}",
            "m",
            "S_p = ks_rel * B_p",
        ),
        (
            "Espaciamiento secuencial teórico Konya",
            "S_seq",
            "=IF({H_b}<4*{B_p}, ({H_b}+7*{B_p})/8, 1.4*{B_p})",
            "m",
            "Si H<4B: (H+7B)/8; si H>=4B: 1.4*B",
        ),
        (
            "Concentración lineal de carga",
            "q_l",
            "=(PI()*({De_t25}/1000)^2/4)*{rho_e}*1000",
            "kg/m",
            "q_l = (pi/4) * (De/1000)² * rho_e * 1000",
        ),
        (
            "Carga explosiva por taladro",
            "Q_tal",
            "={q_l}*{L_c}",
            "kg",
            "Q_tal = q_l * L_c",
        ),
        (
            "Volumen roto por taladro",
            "V_tal",
            "={B_p}*{S_p}*{H_b}",
            "m³",
            "V_tal = B_p * S_p * H_b",
        ),
        (
            "Tonelaje roto por taladro",
            "W_tal",
            "={V_tal}*{rho_r}",
            "t",
            "W_tal = V_tal * rho_r",
        ),
        (
            "Factor de potencia volumétrico",
            "q_v",
            "={Q_tal}/{V_tal}",
            "kg/m³",
            "q_v = Q_tal / V_tal",
        ),
        (
            "Factor de potencia másico",
            "q_m",
            "={Q_tal}/{W_tal}",
            "kg/t",
            "q_m = Q_tal / W_tal",
        ),
        (
            "Factor de potencia en gramos por tonelada",
            "FP_g",
            "={q_m}*1000",
            "g/t",
            "FP_g = q_m * 1000",
        ),
        (
            "Índice de rigidez del banco",
            "IR_b",
            "={H_b}/{B_p}",
            "-",
            "IR = H_b / B_p (>= 2.5 adecuado, >= 4.0 excelente)",
        ),
        # Voladura controlada de taludes: Buffer y Precorte
        (
            "Carga explosiva en taladro de Buffer (Amortiguado)",
            "W_buf",
            kt25["w_buffer_kg"],
            "kg",
            "Guía Konya: Carga controlada en fila Buffer",
        ),
        (
            "Relación Factor de Carga Buffer / Producción",
            "KBP",
            kt25["kbp_buffer"],
            "-",
            "Guía Konya (KBP = 1.00)",
        ),
        (
            "Burden de pozos de Buffer",
            "B_buf",
            "=SQRT(({W_buf}*1000)/({FP_g}*{KBP}*{H_b}*{rho_r}*({S_p}/{B_p})))",
            "m",
            "B_buf = [W*1000 / (FP*KBP*H*rho_r*SBR)]^(1/2)",
        ),
        (
            "Espaciamiento de pozos de Buffer",
            "E_buf",
            "={B_buf}*({S_p}/{B_p})",
            "m",
            "E_buf = B_buf * (S_p / B_p)",
        ),
        (
            "Presión en el barreno de Precorte",
            "Pb_pre",
            kt25["pb_precorte_mpa"],
            "MPa",
            "Carga desacoplada de contorno (Enaline / Exsacorte)",
        ),
        (
            "Ángulo de inclinación de Precorte",
            "Beta_pre",
            kt25["ang_precorte_deg"],
            "grados",
            "Inclinación del talud respecto a la vertical (70° horiz.)",
        ),
        (
            "Espaciamiento de taladros de Precorte",
            "E_pre",
            "=({De_in}*({Pb_pre}+{RT_r})/{RT_r})*0.0254",
            "m",
            "E_pre = [De(in) * (Pb + RT) / RT] * 0.0254 (Konya)",
        ),
        (
            "Longitud de taladros de Precorte",
            "L_pre",
            "={H_b}/COS(RADIANS({Beta_pre}))",
            "m",
            "L_pre = H_b / cos(Beta)",
        ),
        (
            "Volumen total real de las 5 banquetas del portal",
            "Vol_banco",
            "=Voladura_Por_Banqueta!C11",
            "m³",
            "Suma dinámica de las 5 banquetas (Hoja Voladura_Por_Banqueta)",
        ),
        (
            "Volumen esponjado total para acarreo",
            "Vol_esp",
            "={Vol_banco}*{Fe_r}",
            "m³",
            "Vol_esp = Vol_banco * Fe_r",
        ),
        (
            "Número de taladros en el banco de referencia",
            "N_tal_b",
            "=ROUNDUP({Vol_banco}/{V_tal}, 0)",
            "taladros",
            "N_tal = ROUNDUP(Vol_banco / V_tal, 0)",
        ),
        (
            "Consumo de explosivo en banco de referencia",
            "Q_tot_b",
            "={N_tal_b}*{Q_tal}",
            "kg",
            "Q_tot = N_tal * Q_tal",
        ),
        (
            "Metros de perforación (Epiroc PowerROC T25)",
            "M_perf_b",
            "={N_tal_b}*{L_b}",
            "m",
            "M_perf = N_tal * L_b",
        ),
    ]

    # 2. Hoja Voladura_Por_Banqueta (Desglose dinámico para las 5 banquetas de 11_Portales.xlsx)
    cols_banq = [
        "ID Banqueta (11_Portales)",
        "Altura Banco H (m)",
        "Volumen In-Situ (m³)",
        "Burden Práctico Bp (m)",
        "Espaciamiento Sp (m)",
        "Pasadura J (m)",
        "Longitud Taladro L (m)",
        "Volumen/Taladro V_tal (m³)",
        "N° Taladros PowerROC T25",
        "Metros Perforados (m)",
        "Horas PowerROC T25 (h)",
        "Carga/Taladro Q (kg)",
        "Consumo Explosivo (kg)",
    ]
    filas_banq = []
    fila_ini = 6
    fila_act = fila_ini
    ql_val = round(kt25["ql_kg_m"], 4)
    rend_val = kt25["rend_perf_m_h"]

    for b in kt25["banquetas_desglose"]:
        filas_banq.append(
            [
                b["id"],
                b["altura_m"],
                b["vol_insitu_m3"],
                b["b_prac_m"],
                b["s_prac_m"],
                b["j_m"],
                f"=B{fila_act}+F{fila_act}",
                f"=D{fila_act}*E{fila_act}*B{fila_act}",
                f"=ROUNDUP(C{fila_act}/H{fila_act}, 0)",
                f"=I{fila_act}*G{fila_act}",
                f"=J{fila_act}/{rend_val}",
                f"=MAX(0, G{fila_act}-(0.85*D{fila_act}))*{ql_val}",
                f"=I{fila_act}*L{fila_act}",
            ]
        )
        fila_act += 1

    if kt25["banquetas_desglose"]:
        fila_fin = fila_act - 1
        filas_banq.append(
            [
                "TOTAL BANQUETAS PORTAL",
                "",
                f"=SUM(C{fila_ini}:C{fila_fin})",
                "",
                "",
                "",
                "",
                "",
                f"=SUM(I{fila_ini}:I{fila_fin})",
                f"=SUM(J{fila_ini}:J{fila_fin})",
                f"=SUM(K{fila_ini}:K{fila_fin})",
                "",
                f"=SUM(M{fila_ini}:M{fila_fin})",
            ]
        )

    tabla_banquetas = Tabla(
        cols_banq,
        filas_banq,
        "Programación de Perforación y Voladura por Tramo de Banqueta (Epiroc PowerROC T25 — Ø 64 mm)",
    )

    # 3. Hoja Ficha_PowerROC_T25
    ft = vb_p.get("ficha_powerroc_t25", {})
    filas_ficha_t25 = [
        ["Equipo de Superficie", ft.get("equipo", "")],
        ["Marca y Modelo", ft.get("marca_modelo", "Epiroc PowerROC T25")],
        ["Aplicación en Obra PA14", ft.get("aplicacion", "")],
        ["Motor Diésel", ft.get("motor", "")],
        ["Potencia Nominal", ft.get("potencia_nominal", "")],
        ["Martillo de Perforación", ft.get("martillo", "")],
        ["Compresor de Barrido", ft.get("compresor", "")],
        ["Rango de Diámetro Recomendado", ft.get("rango_diametro", "")],
        ["Sistema de Aceros / Varillaje", ft.get("sistema_varillaje", "")],
        ["Longitud de Pasada Simple", ft.get("longitud_pasada", "")],
        ["Profundidad Máxima de Perforación", ft.get("profundidad_max", "")],
        ["Broca Base Especificada en Banquetas", ft.get("broca_base", "")],
        ["Velocidad Neta de Penetración", ft.get("velocidad_penetracion", "")],
        ["Vida Útil Estimada de la Broca", ft.get("vida_util_broca", "")],
        ["Consumo Diésel Estimado", ft.get("consumo_diesel", "")],
        ["Archivo PDF Oficial (Drive)", ft.get("archivo_ficha", "")],
        ["Enlace Directo a Ficha Técnica (Google Drive)", ft.get("link_ficha", "")],
    ]
    tabla_ficha_t25 = Tabla(
        ["Característica Técnica", "Especificación Oficial (Epiroc PowerROC T25)"],
        filas_ficha_t25,
        "Ficha Técnica de la Perforadora Hidráulica sobre Orugas Epiroc PowerROC T25",
    )

    # 4. Hoja BD_Explosivos (para que VLOOKUP funcione autónomamente)
    filas_exp = [
        [
            e["nombre"],
            e["fabricante"],
            e["tipo"],
            e["densidad_g_cm3"],
            e["vod_m_s"],
            e["resistencia_agua"],
            e["pd_kbar"],
            e["energia_kcal_kg"],
            e["rws_pct"],
        ]
        for e in vol_p.get("catalogo_explosivos", [])
    ]
    tabla_bd_exp = Tabla(
        [
            "Nombre de Explosivo",
            "Fabricante",
            "Tipo / Familia",
            "Densidad (g/cm³)",
            "VOD (m/s)",
            "Resistencia al Agua",
            "Presión Detonación Pd (kbar)",
            "Energía Específica (kcal/kg)",
            "Potencia Relativa RWS (%)",
        ],
        filas_exp,
        "Catálogo Comercial de Explosivos Industriales (EXSA, Enaex, Orica)",
    )

    # 5. Hoja BD_Rocas
    filas_rocas = [
        [
            r_item["nombre"],
            r_item["densidad_g_cm3"],
            r_item["ucs_mpa"],
            r_item["esponjamiento"],
            r_item["comportamiento"],
        ]
        for r_item in vol_p.get("rocas_geomecanica", [])
    ]
    tabla_rocas = Tabla(
        [
            "Macizo Rocoso",
            "Densidad (g/cm³)",
            "Resistencia Compresiva Uniaxial Rc (MPa)",
            "Factor de Esponjamiento (Fe)",
            "Comportamiento en Voladura",
        ],
        filas_rocas,
        "Base de Datos Geomecánica de Macizos Rocosos (Caso Base: Diorita PA14)",
    )

    # 6. Hoja BD_Brocas_Equipos
    filas_brocas = [
        [
            b["diametro_mm"],
            b["diametro_pulg"],
            b["tecnologia"],
            b["tipo_cortador"],
            b["sistema_rosca"],
            b["rango_roca"],
            b["modelos_referencia"],
            b["equipos_compatibles"],
            b["fabricantes"],
            b["compatible_t25"],
        ]
        for b in vol_p.get("brocas_equipos", [])
    ]
    tabla_brocas = Tabla(
        [
            "Diámetro (mm)",
            "Diámetro (pulg)",
            "Tecnología",
            "Tipo de Cortador",
            "Sistema de Rosca / Martillo",
            "Rango de Roca Recomendado",
            "Modelos de Referencia",
            "Equipos Compatibles",
            "Fabricantes",
            "Compatible con Epiroc PowerROC T25",
        ],
        filas_brocas,
        "Catálogo de Brocas de Perforación y Compatibilidad con Epiroc PowerROC T25",
    )

    # 7. Hoja Criterios_y_Fuentes
    filas_criterios = [
        [
            "Diámetro Óptimo y Máximo en Banco",
            "D_opt = 8 * H ; D_max = 15 * H",
            "Relación entre altura de banco H (m) y diámetro de broca D (mm) según Konya / UNT.",
        ],
        [
            "Burden Máximo Teórico (Konya 1983/1990)",
            "B_max (pies) = 3.15 * D_e(pulg) * (rho_e / rho_r)^(1/3)",
            "Función del diámetro de carga y la raíz cúbica de la relación de densidades.",
        ],
        [
            "Error de Perforación (e)",
            "e = 0.05 + 0.03 * L",
            "Suma del error de emboquille (0.05 m) y desviación angular (0.03 m/m).",
        ],
        [
            "Burden Práctico Ajustado (B_p)",
            "B_p = (B_max * Kd * Ks * Ke) - e",
            "Distancia efectiva desde el eje del barreno hasta la cara libre del banco.",
        ],
        [
            "Sobreperforación / Pasadura (J)",
            "J = 0.30 * B_max",
            "Perforación bajo la cota de banqueta para evitar lomos o repiés.",
        ],
        [
            "Taco / Retacado Inerte (T)",
            "T = kt * B_p (kt = 0.85)",
            "Confinamiento con detrito angular para evitar cráteres, airblast y flyrock.",
        ],
        [
            "Espaciamiento Práctico (S_p)",
            "S_p = 1.15 * B_p (roca dura)",
            "Distancia entre taladros de una misma fila en banqueo de portal.",
        ],
        [
            "Pozos de Buffer y Precorte de Taludes",
            "B_buf = [W*1000/(FP*KBP*H*rho_r*SBR)]^0.5 ; E_pre = D_in*(Pb+RT)/RT",
            "Control de sobrerrotura (backbreak) en los taludes finales de las banquetas.",
        ],
    ]
    tabla_criterios = Tabla(
        [
            "Parámetro de Diseño",
            "Fórmula (Modelo Matemático de Bancos de C.J. Konya)",
            "Justificación Técnica y Criterio de Control en Banquetas",
        ],
        filas_criterios,
        "1. Formulario Técnico del Modelo Matemático de Bancos de C.J. Konya",
    )
    filas_fuentes = [
        [f["categoria"], f["fuente"], f["justificacion"], f["enlace"]]
        for f in vol_p.get("fuentes_bibliograficas", [])
    ]
    tabla_fuentes = Tabla(
        [
            "Categoría",
            "Documento / Fuente Oficial",
            "Justificación en el Proyecto PA14",
            "Enlace Google Drive",
        ],
        filas_fuentes,
        "2. Fuentes Bibliográficas y Documentación Verificada en Google Drive (Unidad 2)",
    )

    return Libro(
        archivo="15_Voladura_Banquetas.xlsx",
        hojas=[
            Hoja(
                nombre="Calculadora_Konya_T25",
                titulo="Calculadora de Perforación y Voladura de Banquetas con Epiroc PowerROC T25 (Broca 64 mm)",
                tablas=[
                    tabla_parametros(
                        filas_t25,
                        "Diseño de Voladura de Banquetas en Superficie, Buffer y Precorte (Modelo C.J. Konya)",
                    )
                ],
            ),
            Hoja(
                nombre="Voladura_Por_Banqueta",
                titulo="Desglose de Perforación y Voladura para los 5 Tramos de Banquetas (11_Portales)",
                tablas=[tabla_banquetas],
            ),
            Hoja(
                nombre="Ficha_PowerROC_T25",
                titulo="Especificaciones Técnicas Oficiales — Perforadora sobre Orugas Epiroc PowerROC T25",
                tablas=[tabla_ficha_t25],
            ),
            Hoja(
                nombre="BD_Explosivos",
                titulo="Base de Datos de Explosivos Industriales y Agentes de Voladura",
                tablas=[tabla_bd_exp],
            ),
            Hoja(
                nombre="BD_Rocas",
                titulo="Base de Datos Geomecánica de Macizos Rocosos",
                tablas=[tabla_rocas],
            ),
            Hoja(
                nombre="BD_Brocas_Equipos",
                titulo="Catálogo Técnico de Brocas de Perforación y Equipos Compatibles",
                tablas=[tabla_brocas],
            ),
            Hoja(
                nombre="Criterios_y_Fuentes",
                titulo="Formulario Matemático de C.J. Konya y Fuentes Documentales (Unidad 2)",
                tablas=[tabla_criterios, tabla_fuentes],
            ),
        ],
    )


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 15_Voladura_Banquetas.md exclusiva para las banquetas en superficie."""
    t_resumen_t25 = Tabla(
        ["Parámetro", "Símbolo", "Valor", "Unidad", "Justificación Técnica (Konya)"],
        [
            [
                "Equipo de perforación en banquetas",
                "Equipo",
                "Epiroc PowerROC T25",
                "-",
                "Perforadora sobre orugas (173 HP, martillo RD 14UP)",
            ],
            [
                "Diámetro de broca de botones",
                "De_t25",
                f"{r['de_mm']:.1f}",
                "mm",
                'Broca 2.5" T38/T45 (48 <= 64 <= 90 mm)',
            ],
            [
                "Explosivo base seleccionado",
                "Tipo_e",
                r["explosivo_base"],
                "-",
                f"Densidad {r['rho_e']} g/cm³, VOD {r['vod_m_s']:.0f} m/s",
            ],
            [
                "Macizo rocoso del portal",
                "Tipo_r",
                r["roca_base"],
                "-",
                f"Densidad {r['rho_r']} g/cm³, UCS {r['ucs_mpa']:.0f} MPa",
            ],
            [
                "Burden máximo teórico",
                "B_max",
                f"{r['b_max_m']:.2f}",
                "m",
                "3.15 * De(in) * (rho_e/rho_r)^(1/3) * 0.3048",
            ],
            ["Error de perforación", "e", f"{r['e_m']:.2f}", "m", "0.05 + 0.03 * L"],
            [
                "Burden práctico ajustado",
                "B_p",
                f"{r['b_prac_m']:.2f}",
                "m",
                "B_max - e",
            ],
            [
                "Espaciamiento práctico",
                "S_p",
                f"{r['s_m']:.2f}",
                "m",
                "1.15 * B_p (roca dura)",
            ],
            [
                "Sobreperforación (Pasadura)",
                "J_b",
                f"{r['j_m']:.2f}",
                "m",
                "0.30 * B_max",
            ],
            ["Longitud de taco", "T_b", f"{r['t_m']:.2f}", "m", "0.85 * B_p"],
            [
                "Concentración lineal de carga",
                "q_l",
                f"{r['ql_kg_m']:.2f}",
                "kg/m",
                "(pi/4) * De² * rho_e",
            ],
            [
                "Carga explosiva por taladro (H=6m)",
                "Q_tal",
                f"{r['q_kg']:.2f}",
                "kg/tal",
                "q_l * L_c",
            ],
            [
                "Factor de potencia volumétrico",
                "q_v",
                f"{r['qv_kg_m3']:.2f}",
                "kg/m³",
                "Q_tal / V_tal",
            ],
            [
                "Factor de potencia másico",
                "FP_g",
                f"{r['fp_g_ton']:.1f}",
                "g/t",
                "(Q_tal / W_tal) * 1000",
            ],
            [
                "Malla de Buffer (B_buf x E_buf)",
                "Buffer",
                f"{r['b_buffer_m']:.2f} x {r['e_buffer_m']:.2f}",
                "m",
                "Fila amortiguada ante talud final",
            ],
            [
                "Espaciamiento de Precorte (70°)",
                "E_pre",
                f"{r['e_precorte_m']:.2f}",
                "m",
                "De(in) * (Pb + RT) / RT * 0.0254",
            ],
        ],
        "Parámetros de Perforación y Voladura de Banquetas en Superficie (Epiroc PowerROC T25)",
    )

    filas_b = [
        [
            b["id"],
            f"{b['altura_m']:.1f}",
            f"{b['vol_insitu_m3']:.2f}",
            f"{b['l_tal_m']:.2f}",
            b["n_taladros"],
            f"{b['metros_perf_m']:.1f}",
            f"{b['horas_t25_h']:.1f}",
            f"{b['kg_explosivo']:.1f}",
        ]
        for b in r["banquetas_desglose"]
    ]
    filas_b.append(
        [
            "**TOTAL BANQUETAS**",
            "-",
            f"**{r['tot_vol_banq_m3']:.2f}**",
            "-",
            f"**{r['tot_tal_banq']}**",
            f"**{r['tot_m_perf_banq_m']:.1f}**",
            f"**{r['tot_h_perf_banq_h']:.1f}**",
            f"**{r['tot_kg_exp_banq']:.1f}**",
        ]
    )
    t_banquetas = Tabla(
        [
            "Tramo de Banqueta (11_Portales)",
            "H (m)",
            "Volumen In-Situ (m³)",
            "L Taladro (m)",
            "N° Taladros",
            "Metros Perf. (m)",
            "Horas T25 (h)",
            "Explosivo (kg)",
        ],
        filas_b,
        "Resumen de Perforación y Voladura por Tramo de Banqueta del Portal",
    )

    return Memoria(
        archivo="15_Voladura_Banquetas.md",
        titulo="15 · Memoria de Cálculo: Perforación y Voladura de Banquetas de Portal en Superficie (Epiroc PowerROC T25 — Modelo C.J. Konya)",
        secciones=[
            (
                "1. Alcance y Diferenciación Operativa (Banquetas en Superficie vs. Túnel Subterráneo)",
                [
                    "El presente documento (`15_Voladura_Banquetas.md` y libro `15_Voladura_Banquetas.xlsx`) desarrolla "
                    "**exclusivamente la perforación y voladura en superficie (a cielo abierto con dos caras libres)** "
                    "para la excavación escalonada de las **Banquetas y Taludes de los Portales de Entrada y Salida**, "
                    "empleando la **Perforadora Hidráulica sobre Orugas (`Rockdrill`) Epiroc PowerROC T25** "
                    "($173\\text{ HP}$, martillo en cabeza `RD 14UP`, broca de botones $\\varnothing 64\\text{ mm} = 2.5''$ "
                    "con varillaje T38/T45).",
                    "> **Nota de separación técnica:** La perforación y voladura subterránea en el frente interior del "
                    "túnel (que emplea el **Jumbo Frontal Computarizado de 3 brazos Sandvik DT1131 / XE3C** con barra "
                    "de $3.66\\text{ m}$ y broca $\\varnothing 45\\text{ mm}$) se encuentra en el entregable separado "
                    "**`12_Voladura.xlsx`** y **`12_Voladura.md`**.",
                    t_resumen_t25,
                ],
            ),
            (
                "2. Programación de Perforación y Voladura para los 5 Tramos de Banquetas (`11_Portales`)",
                [
                    "Integrando los volúmenes geométricos in-situ de las 5 banquetas calculadas en `11_Portales.xlsx` "
                    "($3,795.21\\text{ m}^3$ en banco) con la malla práctica de C.J. Konya ($B_p = 1.58\\text{ m} \\times "
                    "S_p = 1.81\\text{ m}$), se obtiene el requerimiento total de taladros, metros perforados, horas "
                    "de operación de la **Epiroc PowerROC T25** y consumo de explosivo **Semexsa E-80**:",
                    t_banquetas,
                ],
            ),
        ],
    )
