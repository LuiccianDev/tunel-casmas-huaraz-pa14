"""Generador de la memoria descriptiva 12_Voladura.md."""

from __future__ import annotations

from typing import Any

from ...modelo import Memoria, Tabla


def construir_memoria_voladura(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 12_Voladura.md exclusiva para la voladura subterránea del túnel."""
    ft = r["frente_tunel"]
    inp = r["inputs"]
    calc = r["calculados"]

    t_malla = Tabla(
        ["Parámetro del Frente Subterráneo", "Símbolo", "Valor", "Unidad", "Criterio / Fuente"],
        [
            ["Equipo de perforación subterránea", "Eq_tunel", ft["equipo_tunel"], "-", "3 brazos automatizados iDATA"],
            ["Área de excavación del frente", "A_tun", f"{ft['area_m2']:.2f}", "m²", "Sección herradura 13.30 x 9.58 m"],
            ["Longitud de barreno (12 pies)", "L_bar", f"{ft['lb_m']:.2f}", "m", "Barra estándar Jumbo Sandvik DT1131"],
            ["Avance efectivo por disparo (90%)", "Av_disp", f"{ft['avance_disparo_m']:.2f}", "m", "L_bar * 0.90"],
            ["Volumen in-situ por disparo", "V_disp", f"{ft['vol_disparo_m3']:.2f}", "m³", "A_tun * Av_disp"],
            ["Taladros vacíos de alivio (Ø 102 mm)", "N_aliv", ft["n_alivio_vacios"], "taladros", "Escariados sin carga en el cuele"],
            ["Taladros cargados en el frente (Ø 45 mm)", "N_carg", ft["taladros_cargados"], "taladros", "Cuele (16) + Ayudas (20) + Destroza (105) + Contorno (64) + Arrastres (26)"],
            ["Total de taladros perforados por disparo", "N_perf", ft["taladros_perforados"], "taladros", "N_carg + N_aliv"],
            ["Tiempo neto de perforación (3 brazos)", "T_perf_h", f"{ft['tiempo_perf_neto_h']:.2f}", "h/disparo", "M_perf / (Vp * 3 brazos * 60)"],
            ["Consumo de explosivo por disparo", "Q_disp_kg", f"{ft['kg_explosivo_disparo']:.2f}", "kg/disparo", "V_disp * 1.60 kg/m³"],
        ],
        "Resumen de Perforación y Voladura Subterránea del Frente del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
    )

    t_resumen_tunel = Tabla(
        ["Parámetro", "Símbolo", "Valor", "Unidad", "Criterio / Fórmula Konya"],
        [
            ["Diámetro de taladro de producción", "De", inp["de_mm"], "mm", "Jumbo 3 brazos Sandvik DT1131"],
            ["Densidad del explosivo", "Sge", inp["sge"], "g/cm³", "Emulsión encartuchada / ANFO Pesado"],
            ["Densidad de la roca", "Sgr", inp["sgr"], "g/cm³", "Litología ponderada PA14"],
            ["Burden teórico de Konya en destroza", "B", f"{calc['burden_m']:.2f}", "m", "0.012 * (2*Sge/Sgr + 1.5) * De"],
            ["Burden corregido (Kr, Kd, Ks)", "Bc", f"{calc['burden_corr_m']:.2f}", "m", "B * Kr * Kd * Ks"],
            ["Espaciamiento en destroza", "S", f"{calc['espaciamiento_m']:.2f}", "m", "1.4 * B"],
            ["Taco inerte", "T", f"{calc['taco_m']:.2f}", "m", "0.7 * B"],
            ["Carga total por taladro de destroza", "Qt", f"{calc['carga_total_kg']:.2f}", "kg/tal", "(Cf + Cc) * Qbk"],
            ["Factor de carga volumétrico en destroza", "FC", f"{calc['factor_carga_kg_m3']:.2f}", "kg/m³", "Qt / V"],
            ["Retardo barreno a barreno", "th", f"{calc['retardo_barrenos_ms']:.1f}", "ms", "Th * S"],
            ["Retardo entre secciones", "tR", f"{calc['retardo_filas_ms']:.1f}", "ms", "TR * B"],
        ],
        "Parámetros de Destroza Subterránea (Modelo Matemático de C.J. Konya)",
    )

    return Memoria(
        archivo="12_Voladura.md",
        titulo="12 · Memoria de Cálculo: Perforación y Voladura Subterránea del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
        secciones=[
            (
                "1. Alcance y Diferenciación Operativa (Túnel Subterráneo vs. Banquetas en Superficie)",
                [
                    "El presente documento (`12_Voladura.md` y libro `12_Voladura.xlsx`) desarrolla **exclusivamente la "
                    "perforación y voladura subterránea en el frente de ataque del Túnel Casmas Huaraz PA14** "
                    "($B = 13.30\\text{ m}, H = 9.58\\text{ m}, A = 108.43\\text{ m}^2$), donde se trabaja con **una sola "
                    "cara libre inicial** empleando el **Jumbo Frontal Computarizado de 3 brazos Sandvik DT1131 / XE3C** "
                    "($300\\text{ HP}$, barra de $12\\text{ pies} = 3.66\\text{ m}$, broca de producción $\\varnothing 45\\text{ mm}$ "
                    "y escariador de alivio $\\varnothing 102\\text{ mm}$).",
                    "> **Nota de separación técnica:** La perforación y voladura a cielo abierto para los cortes escalonados "
                    "de las **Banquetas y Taludes de Portal en Superficie** (que emplea la perforadora hidráulica sobre "
                    "orugas **Epiroc PowerROC T25** con broca $\\varnothing 64\\text{ mm}$ y el modelo de bancos de C.J. Konya) "
                    "se encuentra independizada en el entregable **`15_Voladura_Banquetas.xlsx`** y su memoria **`15_Voladura_Banquetas.md`**.",
                    t_malla,
                ],
            ),
            (
                "2. Modelo Matemático de C.J. Konya en la Zona de Destroza del Frente",
                [
                    "Una vez aperturada la cavidad inicial por el **cuele quemado cilíndrico de 4 secciones** y sus "
                    "ayudas, los taladros del núcleo de **destroza/producción** trabajan hacia la cara libre interna "
                    "generada, rigiéndose por las relaciones del modelo de C.J. Konya para $\\varnothing 45\\text{ mm}$:",
                    t_resumen_tunel,
                ],
            ),
        ],
    )
