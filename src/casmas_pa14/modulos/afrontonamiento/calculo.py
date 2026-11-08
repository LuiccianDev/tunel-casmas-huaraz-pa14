"""Motor de cálculo geomecánico y de metrados para el afrontonamiento y sellado del portal."""

from __future__ import annotations

import math
from typing import Any


def calcular_afrontonamiento_portal(
    p: dict[str, Any], ctx: dict[str, Any]
) -> dict[str, Any]:
    """Calcula el dimensionamiento del afrontonamiento y sellado del portal del túnel."""
    af = p.get("afrontonamiento", {})
    sec_p = p.get("seccion", {})
    sec_ctx = ctx.get("seccion", {})

    ancho_b = float(sec_ctx.get("ancho_m", sec_p.get("ancho_m", 13.30)))
    alto_h = float(sec_ctx.get("altura_m", sec_p.get("altura_m", 9.58)))

    pts_ucs = int(af.get("pts_ucs", 7))
    pts_rqd = int(af.get("pts_rqd", 13))
    pts_esp = int(af.get("pts_espaciamiento", 10))
    pts_cond = int(af.get("pts_condicion_juntas", 20))
    pts_agua = int(af.get("pts_agua", 7))
    aj_ori = int(af.get("ajuste_orientacion", -5))
    rmr_basico = pts_ucs + pts_rqd + pts_esp + pts_cond + pts_agua
    rmr_corregido = rmr_basico + aj_ori

    k_terz = float(af.get("factor_k_terzaghi", 0.35))
    gamma_kn_m3 = float(af.get("peso_especifico_roca_kn_m3", 26.5))
    ancho_carga_c = ancho_b + alto_h
    hp_terzaghi_m = k_terz * ancho_carga_c
    h_fronton_m = alto_h + hp_terzaghi_m
    presion_vert_kpa = gamma_kn_m3 * hp_terzaghi_m
    presion_vert_mpa = presion_vert_kpa / 1000.0

    l_eq = float(af.get("longitud_total_equipo_m", 8.84))
    w_eq = float(af.get("ancho_sobre_neumaticos_m", 2.98))
    h_cab = float(af.get("altura_cabina_m", 3.58))
    r_giro = float(af.get("radio_giro_ext_m", 7.26))
    h_desc = float(af.get("altura_descarga_max_m", 3.10))
    d_seg = float(af.get("distancia_seguridad_op_m", 1.00))

    h_hastial_m = alto_h - (ancho_b / 2.0)
    area_rect_inf_m2 = ancho_b * h_hastial_m
    area_boveda_m2 = (math.pi * ((ancho_b / 2.0) ** 2)) / 2.0
    area_tunel_m2 = area_rect_inf_m2 + area_boveda_m2

    semiancho_maniobra_m = r_giro + l_eq + d_seg
    ancho_fronton_m = 2.0 * semiancho_maniobra_m
    area_bruta_fronton_m2 = ancho_fronton_m * h_fronton_m
    area_neta_fronton_m2 = area_bruta_fronton_m2 - area_tunel_m2

    l_pano = float(af.get("largo_pano_malla_m", 6.00))
    w_pano = float(af.get("ancho_pano_malla_m", 2.40))
    traslape = float(af.get("traslape_malla_m", 0.30))
    t_inst_pano_min = float(af.get("tiempo_instalacion_pano_min", 15.0))
    l_util_pano = l_pano - traslape
    w_util_pano = w_pano - traslape
    area_util_pano_m2 = l_util_pano * w_util_pano
    n_panos_malla = math.ceil(area_neta_fronton_m2 / area_util_pano_m2)
    t_total_malla_h = (n_panos_malla * t_inst_pano_min) / 60.0

    l_perno_f = float(af.get("longitud_perno_fronton_m", 3.00))
    d_perno_mm = float(af.get("diametro_perno_fronton_mm", 22.0))
    d_tal_mm = float(af.get("diametro_taladro_perno_mm", 32.0))
    esp_perno_f = float(af.get("espaciamiento_pernos_fronton_m", 1.50))
    d_cart_mm = float(af.get("diametro_cartucho_resina_mm", 28.0))
    l_cart_mm = float(af.get("longitud_cartucho_resina_mm", 305.0))
    peso_cart_g = float(af.get("peso_cartucho_resina_g", 320.0))
    cart_x_caja = int(af.get("cartuchos_por_caja", 50))
    vel_bolter = float(af.get("velocidad_perf_bolter_m_min", 1.50))
    t_man_bolter = float(af.get("tiempo_maniobra_bolter_min", 1.00))
    t_iny_bolter = float(af.get("tiempo_inyeccion_empernado_min", 2.50))

    area_trib_perno_m2 = esp_perno_f**2
    n_pernos_fronton = math.ceil(area_neta_fronton_m2 / area_trib_perno_m2)
    vol_tal_m3 = math.pi * ((d_tal_mm / 2000.0) ** 2) * l_perno_f
    vol_barra_m3 = math.pi * ((d_perno_mm / 2000.0) ** 2) * l_perno_f
    vol_anular_resina_m3 = vol_tal_m3 - vol_barra_m3
    vol_cartucho_m3 = math.pi * ((d_cart_mm / 2000.0) ** 2) * (l_cart_mm / 1000.0)
    cartuchos_x_tal = math.ceil(vol_anular_resina_m3 / vol_cartucho_m3)
    total_cartuchos = n_pernos_fronton * cartuchos_x_tal
    total_cajas_resina = math.ceil(total_cartuchos / cart_x_caja)
    masa_resina_kg = (total_cartuchos * peso_cart_g) / 1000.0
    t_perf_perno_min = l_perno_f / vel_bolter
    t_ciclo_perno_min = t_perf_perno_min + t_man_bolter + t_iny_bolter
    t_total_empernado_h = (n_pernos_fronton * t_ciclo_perno_min) / 60.0

    e_shot_m = float(af.get("espesor_shotcrete_fronton_m", 0.12))
    rebote = float(af.get("rebote_shotcrete_pct", 0.10))
    cem_kg_m3 = float(af.get("cemento_dosificacion_kg_m3", 425.0))
    peso_bolsa_kg = float(af.get("peso_bolsa_cemento_kg", 42.5))
    rel_ac = float(af.get("relacion_agua_cemento", 0.58))
    arena_kg_m3 = float(af.get("arena_dosificacion_kg_m3", 1700.0))
    acel_pct = float(af.get("acelerante_sikacem_pct", 0.04))
    nano_pct = float(af.get("nanosilice_pct", 0.01))
    fibra_kg_m3 = float(af.get("fibra_sintetica_kg_m3", 4.0))
    rend_robot = float(af.get("rendimiento_robot_shotcrete_m3_h", 24.0))
    t_fraguado_h = float(af.get("tiempo_fraguado_inicial_h", 3.0))

    vol_shot_teo_m3 = area_neta_fronton_m2 * e_shot_m
    vol_shot_real_m3 = vol_shot_teo_m3 * (1.0 + rebote)
    cemento_total_kg = vol_shot_real_m3 * cem_kg_m3
    bolsas_cemento = math.ceil(cemento_total_kg / peso_bolsa_kg)
    agua_total_l = vol_shot_real_m3 * (cem_kg_m3 * rel_ac)
    arena_total_t = (vol_shot_real_m3 * arena_kg_m3) / 1000.0
    acelerante_total_kg = vol_shot_real_m3 * (cem_kg_m3 * acel_pct)
    nanosilice_total_kg = vol_shot_real_m3 * (cem_kg_m3 * nano_pct)
    fibra_total_kg = vol_shot_real_m3 * fibra_kg_m3
    t_lanzado_h = vol_shot_real_m3 / rend_robot
    t_total_shotcrete_h = t_lanzado_h + t_fraguado_h

    return {
        "pts_ucs": pts_ucs,
        "pts_rqd": pts_rqd,
        "pts_esp": pts_esp,
        "pts_cond": pts_cond,
        "pts_agua": pts_agua,
        "aj_ori": aj_ori,
        "rmr_basico": rmr_basico,
        "rmr_corregido": rmr_corregido,
        "k_terz": k_terz,
        "gamma_kn_m3": gamma_kn_m3,
        "ancho_b": ancho_b,
        "alto_h": alto_h,
        "ancho_carga_c": ancho_carga_c,
        "hp_terzaghi_m": hp_terzaghi_m,
        "h_fronton_m": h_fronton_m,
        "presion_vert_kpa": presion_vert_kpa,
        "presion_vert_mpa": presion_vert_mpa,
        "l_eq": l_eq,
        "w_eq": w_eq,
        "h_cab": h_cab,
        "r_giro": r_giro,
        "h_desc": h_desc,
        "d_seg": d_seg,
        "link_ficha_cat966h": af.get(
            "link_ficha_cat966h",
            "https://drive.google.com/file/d/1MmeCiUDpEDKpKdOn1hrj8rbDK1uqPrcL/view",
        ),
        "h_hastial_m": h_hastial_m,
        "area_rect_inf_m2": area_rect_inf_m2,
        "area_boveda_m2": area_boveda_m2,
        "area_tunel_m2": area_tunel_m2,
        "semiancho_maniobra_m": semiancho_maniobra_m,
        "ancho_fronton_m": ancho_fronton_m,
        "area_bruta_fronton_m2": area_bruta_fronton_m2,
        "area_neta_fronton_m2": area_neta_fronton_m2,
        "l_pano": l_pano,
        "w_pano": w_pano,
        "traslape": traslape,
        "t_inst_pano_min": t_inst_pano_min,
        "area_util_pano_m2": area_util_pano_m2,
        "n_panos_malla": n_panos_malla,
        "t_total_malla_h": t_total_malla_h,
        "l_perno_f": l_perno_f,
        "d_perno_mm": d_perno_mm,
        "d_tal_mm": d_tal_mm,
        "esp_perno_f": esp_perno_f,
        "d_cart_mm": d_cart_mm,
        "l_cart_mm": l_cart_mm,
        "peso_cart_g": peso_cart_g,
        "cart_x_caja": cart_x_caja,
        "vel_bolter": vel_bolter,
        "t_man_bolter": t_man_bolter,
        "t_iny_bolter": t_iny_bolter,
        "area_trib_perno_m2": area_trib_perno_m2,
        "n_pernos_fronton": n_pernos_fronton,
        "vol_anular_resina_m3": vol_anular_resina_m3,
        "vol_cartucho_m3": vol_cartucho_m3,
        "cartuchos_x_tal": cartuchos_x_tal,
        "total_cartuchos": total_cartuchos,
        "total_cajas_resina": total_cajas_resina,
        "masa_resina_kg": masa_resina_kg,
        "t_ciclo_perno_min": t_ciclo_perno_min,
        "t_total_empernado_h": t_total_empernado_h,
        "e_shot_m": e_shot_m,
        "rebote": rebote,
        "cem_kg_m3": cem_kg_m3,
        "peso_bolsa_kg": peso_bolsa_kg,
        "rel_ac": rel_ac,
        "arena_kg_m3": arena_kg_m3,
        "acel_pct": acel_pct,
        "nano_pct": nano_pct,
        "fibra_kg_m3": fibra_kg_m3,
        "rend_robot": rend_robot,
        "t_fraguado_h": t_fraguado_h,
        "vol_shot_teo_m3": vol_shot_teo_m3,
        "vol_shot_real_m3": vol_shot_real_m3,
        "cemento_total_kg": cemento_total_kg,
        "bolsas_cemento": bolsas_cemento,
        "agua_total_l": agua_total_l,
        "arena_total_t": arena_total_t,
        "acelerante_total_kg": acelerante_total_kg,
        "nanosilice_total_kg": nanosilice_total_kg,
        "fibra_total_kg": fibra_total_kg,
        "t_lanzado_h": t_lanzado_h,
        "t_total_shotcrete_h": t_total_shotcrete_h,
    }
