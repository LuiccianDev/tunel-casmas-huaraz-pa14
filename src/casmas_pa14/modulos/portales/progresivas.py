"""Cálculo de control de tiempos tramo a tramo por progresiva y flota de acarreo."""

from __future__ import annotations

import math
from typing import Any


def calcular_control_progresivas(portales: dict[str, Any]) -> dict[str, Any]:
    """Calcula rendimientos, ciclos de volquete y tiempos de ejecución por tramos y frentes."""
    cfg = portales.get("control_tiempos_progresivas", {})
    t_carguio = float(cfg.get("cargador_tiempo_ciclo_camion_min", 2.104))
    n_volq = int(cfg.get("volquetes_en_flota", 4))
    v_cargado = float(cfg.get("volquete_vel_cargado_kmh", 25.0)) * 1000.0 / 60.0
    v_vacio = float(cfg.get("volquete_vel_vacio_kmh", 35.0)) * 1000.0 / 60.0
    t_fijo = float(cfg.get("volquete_tiempo_fijo_min", 1.10))
    rend_cuneta = float(cfg.get("cuneta_rendimiento_limpieza_m_h", 40.0))
    h_guardia = float(cfg.get("horas_efectivas_por_guardia", 10.5))
    cap_suelta = float(cfg.get("volquete_capacidad_suelta_m3", 16.0))
    factor_esp = float(portales.get("factor_esponjamiento", 1.30))

    sectores_calculados = []
    total_vol_banco = 0.0
    total_vol_suelto = 0.0
    total_viajes = 0
    total_horas = 0.0

    sectores_cfg = portales.get("sectores_progresivas", [])
    for s in sectores_cfg:
        tramos_res = []
        d_base = s["distancia_base_m"]
        sub_vol_banco = 0.0
        sub_vol_suelto = 0.0
        sub_viajes = 0
        sub_horas = 0.0

        for prog_str, l_tramo, vol_banco in s["tramos"]:
            vol_suelto = vol_banco * factor_esp
            n_viajes = math.ceil(vol_suelto / cap_suelta)

            try:
                partes = prog_str.replace("a", "-").split("-")
                p1 = float(partes[0].replace("+", "").strip())
                p2 = float(partes[1].replace("+", "").strip())
                x_med = (p1 + p2) / 2.0
            except Exception:
                x_med = l_tramo / 2.0

            d_media = d_base + x_med
            t_ciclo = t_carguio + (d_media / v_cargado) + (d_media / v_vacio) + t_fijo

            vol_viaje_banco = cap_suelta / factor_esp
            r_flota = n_volq * (60.0 / t_ciclo) * vol_viaje_banco * 0.83
            h_acarreo = vol_banco / r_flota if r_flota > 0 else 0.0
            h_cuneta = l_tramo / rend_cuneta if rend_cuneta > 0 else 0.0

            h_tramo = max(h_acarreo, h_cuneta)
            guardias = h_tramo / h_guardia
            dias = guardias / 2.0

            sub_vol_banco += vol_banco
            sub_vol_suelto += vol_suelto
            sub_viajes += n_viajes
            sub_horas += h_tramo

            tramos_res.append(
                {
                    "progresiva": prog_str,
                    "longitud_m": l_tramo,
                    "vol_banco_m3": round(vol_banco, 2),
                    "vol_suelto_m3": round(vol_suelto, 2),
                    "viajes": n_viajes,
                    "distancia_botadero_m": round(d_media, 1),
                    "ciclo_volquete_min": round(t_ciclo, 2),
                    "rendimiento_flota_m3_h": round(r_flota, 1),
                    "horas_acarreo": round(h_acarreo, 2),
                    "horas_cuneta": round(h_cuneta, 2),
                    "guardias": round(guardias, 2),
                    "dias": round(dias, 2),
                }
            )

        total_vol_banco += sub_vol_banco
        total_vol_suelto += sub_vol_suelto
        total_viajes += sub_viajes
        total_horas += sub_horas

        sectores_calculados.append(
            {
                "sector": s["sector"],
                "clave": s["clave"],
                "vol_banco_total": round(sub_vol_banco, 2),
                "vol_suelto_total": round(sub_vol_suelto, 2),
                "viajes_total": sub_viajes,
                "horas_total": round(sub_horas, 2),
                "guardias_total": round(sub_horas / h_guardia, 2),
                "dias_total": round((sub_horas / h_guardia) / 2.0, 2),
                "tramos": tramos_res,
            }
        )

    return {
        "sectores": sectores_calculados,
        "total_vol_banco_m3": round(total_vol_banco, 2),
        "total_vol_suelto_m3": round(total_vol_suelto, 2),
        "total_viajes": total_viajes,
        "total_horas": round(total_horas, 2),
        "total_guardias": round(total_horas / h_guardia, 2),
        "total_dias": round((total_horas / h_guardia) / 2.0, 2),
    }
