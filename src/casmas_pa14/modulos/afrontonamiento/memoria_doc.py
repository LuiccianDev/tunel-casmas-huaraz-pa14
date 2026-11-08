"""Generador de la memoria descriptiva 14_Afrontonamiento.md."""

from __future__ import annotations

from typing import Any

from ...modelo import Memoria, Tabla


def construir_memoria_afrontonamiento(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 14_Afrontonamiento.md del afrontonamiento y sellado del portal."""
    t_resumen_fronton = Tabla(
        ["Componente / Parámetro", "Valor Calculado", "Unidad", "Criterio Técnico / Fuente"],
        [
            ["Valoración Geomecánica RMR Básico / Corregido", f"{r['rmr_basico']} / {r['rmr_corregido']}", "pts", "Bieniawski (1989) — Clase III (Roca Regular)"],
            ["Altura de carga de roca aflojada (Hp Terzaghi)", r["hp_terzaghi_m"], "m", "Condición 4: Hp = 0.35 * (B + Ht)"],
            ["Altura total del frontón (Ht + Hp)", r["h_fronton_m"], "m", f"Ht = {r['alto_h']} m + Hp = {r['hp_terzaghi_m']:.2f} m"],
            ["Presión vertical de diseño sobre clave", r["presion_vert_kpa"], "kPa", f"gamma = {r['gamma_kn_m3']} kN/m³ * Hp"],
            ["Ancho total de maniobra en portal (CAT 966H)", r["ancho_fronton_m"], "m", f"2 * (R_giro {r['r_giro']} + L_eq {r['l_eq']} + D_seg {r['d_seg']})"],
            ["Área bruta del frontón", r["area_bruta_fronton_m2"], "m²", "Ancho frontón * Altura frontón"],
            ["Área de la sección herradura del túnel descontada", r["area_tunel_m2"], "m²", "03_Seccion (13.30 x 9.58 m)"],
            ["ÁREA NETA A SELLAR / AFRONTONAR EN EL PORTAL", r["area_neta_fronton_m2"], "m²", "Área bruta - Área sección del túnel"],
            ["Paños de malla electrosoldada (6.0 x 2.4 m, traslape 0.30 m)", r["n_panos_malla"], "paños", f"Área útil {r['area_util_pano_m2']:.2f} m²/paño ({r['t_total_malla_h']:.2f} h)"],
            ["Pernos RockBolt (L=3.0 m, d=22 mm, malla 1.5x1.5 m)", r["n_pernos_fronton"], "pernos", f"Ciclo Bolter Robótico: {r['t_total_empernado_h']:.2f} h"],
            ["Cartuchos de resina epóxica (28x305 mm, 320 g)", r["total_cartuchos"], "cartuchos", f"{r['cartuchos_x_tal']} cart/perno ({r['total_cajas_resina']} cajas, {r['masa_resina_kg']:.1f} kg)"],
            ["Volumen real de Shotcrete (e=0.12 m + 10% rebote)", r["vol_shot_real_m3"], "m³", f"Cemento: {r['bolsas_cemento']} bolsas, Fibra: {r['fibra_total_kg']:.1f} kg ({r['t_total_shotcrete_h']:.2f} h)"],
        ],
        "Síntesis de Ingeniería del Afrontonamiento y Sellado del Portal",
    )

    return Memoria(
        archivo="14_Afrontonamiento.md",
        titulo="14 · Memoria de Cálculo: Afrontonamiento y Sellado del Portal de Emboquille",
        secciones=[
            (
                "1. Fundamento y Geometría del Afrontonamiento del Portal",
                [
                    "El **afrontonamiento y sellado del portal** prepara y estabiliza el talud frontal exterior "
                    "de emboquille antes de iniciar el avance subterráneo del túnel. Su dimensionamiento integra "
                    "la **Teoría de Cargas de Roca de Karl Terzaghi (1946)** para un macizo Clase III "
                    "($\\text{RMR} = 42$, Condición 4: *roca medianamente fracturada en bloques algo abiertos*, "
                    "$H_p = 0.35(B + H_t)$) con la envolvente cinemática de giro del cargador frontal "
                    "**Caterpillar 966H** ([Ficha Técnica en Drive](https://drive.google.com/file/d/1MmeCiUDpEDKpKdOn1hrj8rbDK1uqPrcL/view)), "
                    "descontando el área de la sección herradura del túnel ($108.43\\text{ m}^2$) para obtener el "
                    "**Área Neta del Frontón a Sellar ($493.08\\text{ m}^2$)**.",
                    t_resumen_fronton,
                ],
            ),
        ],
    )
