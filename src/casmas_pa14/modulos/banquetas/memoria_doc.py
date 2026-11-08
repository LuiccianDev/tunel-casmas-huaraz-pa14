"""Generador de la memoria descriptiva 15_Voladura_Banquetas.md."""

from __future__ import annotations

from typing import Any

from ...modelo import Memoria, Tabla


def construir_memoria_banquetas(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 15_Voladura_Banquetas.md exclusiva para las banquetas en superficie."""
    t_resumen_t25 = Tabla(
        ["Parámetro", "Símbolo", "Valor", "Unidad", "Justificación Técnica (Konya)"],
        [
            ["Equipo de perforación en banquetas", "Equipo", "Epiroc PowerROC T25", "-", "Perforadora sobre orugas (173 HP, martillo RD 14UP)"],
            ["Diámetro de broca de botones", "De_t25", f"{r['de_mm']:.1f}", "mm", 'Broca 2.5" T38/T45 (48 <= 64 <= 90 mm)'],
            ["Explosivo base seleccionado", "Tipo_e", r["explosivo_base"], "-", f"Densidad {r['rho_e']} g/cm³, VOD {r['vod_m_s']:.0f} m/s"],
            ["Macizo rocoso del portal", "Tipo_r", r["roca_base"], "-", f"Densidad {r['rho_r']} g/cm³, UCS {r['ucs_mpa']:.0f} MPa"],
            ["Burden máximo teórico", "B_max", f"{r['b_max_m']:.2f}", "m", "3.15 * De(in) * (rho_e/rho_r)^(1/3) * 0.3048"],
            ["Error de perforación", "e", f"{r['e_m']:.2f}", "m", "0.05 + 0.03 * L"],
            ["Burden práctico ajustado", "B_p", f"{r['b_prac_m']:.2f}", "m", "B_max - e"],
            ["Espaciamiento práctico", "S_p", f"{r['s_m']:.2f}", "m", "1.15 * B_p (roca dura)"],
            ["Sobreperforación (Pasadura)", "J_b", f"{r['j_m']:.2f}", "m", "0.30 * B_max"],
            ["Longitud de taco", "T_b", f"{r['t_m']:.2f}", "m", "0.85 * B_p"],
            ["Concentración lineal de carga", "q_l", f"{r['ql_kg_m']:.2f}", "kg/m", "(pi/4) * De² * rho_e"],
            ["Carga explosiva por taladro (H=6m)", "Q_tal", f"{r['q_kg']:.2f}", "kg/tal", "q_l * L_c"],
            ["Factor de potencia volumétrico", "q_v", f"{r['qv_kg_m3']:.2f}", "kg/m³", "Q_tal / V_tal"],
            ["Factor de potencia másico", "FP_g", f"{r['fp_g_ton']:.1f}", "g/t", "(Q_tal / W_tal) * 1000"],
            ["Malla de Buffer (B_buf x E_buf)", "Buffer", f"{r['b_buffer_m']:.2f} x {r['e_buffer_m']:.2f}", "m", "Fila amortiguada ante talud final"],
            ["Espaciamiento de Precorte (70°)", "E_pre", f"{r['e_precorte_m']:.2f}", "m", "De(in) * (Pb + RT) / RT * 0.0254"],
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
