"""14 · Afrontonamiento: Diseño de Afrontonamiento y Sellado de Portal del Túnel.

Dimensiona el sellado y estabilización del talud frontal exterior de emboquille
(frontón del portal) antes de iniciar la excavación subterránea:
1. Valoración Geomecánica RMR de Bieniawski (1989) del macizo en el portal.
2. Teoría de Cargas de Roca de Karl Terzaghi (1946) sobre la clave (Hp).
3. Geometría del Frontón según el radio de giro del cargador Caterpillar 966H
   y descuento de la sección herradura del túnel (Área Neta a Sellar).
4. Malla Electrosoldada Q-188 con traslape.
5. Pernos Helicoidales RockBolt con Cartuchos de Resina Epóxica y Ciclo del Bolter.
6. Sellado con Shotcrete Robotizado Vía Húmeda reforzado con Macrofibra Sintética.
"""

import math
from typing import Any

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "afrontonamiento"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula el dimensionamiento del afrontonamiento y sellado del portal del túnel."""
    af = p.get("afrontonamiento", {})
    sec_p = p.get("seccion", {})
    sec_ctx = ctx.get("seccion", {})

    ancho_b = float(sec_ctx.get("ancho_m", sec_p.get("ancho_m", 13.30)))
    alto_h = float(sec_ctx.get("altura_m", sec_p.get("altura_m", 9.58)))

    # 1. Valoración RMR Bieniawski (1989) en el Frontón
    pts_ucs = int(af.get("pts_ucs", 7))
    pts_rqd = int(af.get("pts_rqd", 13))
    pts_esp = int(af.get("pts_espaciamiento", 10))
    pts_cond = int(af.get("pts_condicion_juntas", 20))
    pts_agua = int(af.get("pts_agua", 7))
    aj_ori = int(af.get("ajuste_orientacion", -5))
    rmr_basico = pts_ucs + pts_rqd + pts_esp + pts_cond + pts_agua
    rmr_corregido = rmr_basico + aj_ori

    # 2. Teoría de Cargas de Terzaghi (1946)
    k_terz = float(af.get("factor_k_terzaghi", 0.35))
    gamma_kn_m3 = float(af.get("peso_especifico_roca_kn_m3", 26.5))
    ancho_carga_c = ancho_b + alto_h
    hp_terzaghi_m = k_terz * ancho_carga_c
    h_fronton_m = alto_h + hp_terzaghi_m
    presion_vert_kpa = gamma_kn_m3 * hp_terzaghi_m
    presion_vert_mpa = presion_vert_kpa / 1000.0

    # 3. Geometría del Afrontonamiento (Maniobra Cargador Caterpillar 966H)
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

    # 4. Malla Electrosoldada
    l_pano = float(af.get("largo_pano_malla_m", 6.00))
    w_pano = float(af.get("ancho_pano_malla_m", 2.40))
    traslape = float(af.get("traslape_malla_m", 0.30))
    t_inst_pano_min = float(af.get("tiempo_instalacion_pano_min", 15.0))
    l_util_pano = l_pano - traslape
    w_util_pano = w_pano - traslape
    area_util_pano_m2 = l_util_pano * w_util_pano
    n_panos_malla = math.ceil(area_neta_fronton_m2 / area_util_pano_m2)
    t_total_malla_h = (n_panos_malla * t_inst_pano_min) / 60.0

    # 5. Pernos RockBolt + Cartuchos de Resina + Ciclo del Bolter
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

    # 6. Sellado con Shotcrete Robotizado
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


def libro(r: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 14_Afrontonamiento.xlsx con las 6 hojas dinámicas del sellado del portal."""
    af_p = p.get("afrontonamiento", {})

    # 1. Hoja RMR_Geomecanica
    filas_rmr = [
        (
            "1. Resistencia de la roca intacta (UCS = 50 - 100 MPa)",
            "P_ucs",
            r["pts_ucs"],
            "pts",
            "Bieniawski (1989) - Roca moderadamente dura",
        ),
        (
            "2. Índice de calidad de la roca (RQD = 50% - 75%)",
            "P_rqd",
            r["pts_rqd"],
            "pts",
            "Bieniawski (1989) - Calidad media en portal",
        ),
        (
            "3. Espaciamiento de discontinuidades (0.20 - 0.60 m)",
            "P_esp",
            r["pts_esp"],
            "pts",
            "Bieniawski (1989) - Fracturación moderada",
        ),
        (
            "4. Condición de las discontinuidades (Ligeramente rugosas, sep. < 1 mm)",
            "P_cond",
            r["pts_cond"],
            "pts",
            "Bieniawski (1989)",
        ),
        (
            "5. Agua subterránea (Húmedo / goteo ligero)",
            "P_agua",
            r["pts_agua"],
            "pts",
            "Bieniawski (1989) - Caudal < 10 L/min",
        ),
        (
            "RMR Básico (Suma de los 5 parámetros)",
            "RMR_b",
            "={P_ucs}+{P_rqd}+{P_esp}+{P_cond}+{P_agua}",
            "pts",
            "RMR_b = P_ucs + P_rqd + P_esp + P_cond + P_agua",
        ),
        (
            "6. Ajuste por orientación de discontinuidades (Regular)",
            "Aj_ori",
            r["aj_ori"],
            "pts",
            "Bieniawski (1989) para talud/portal",
        ),
        (
            "RMR Corregido de Diseño en el Frontón",
            "RMR_corr",
            "={RMR_b}+{Aj_ori}",
            "pts",
            "RMR_corr = RMR_b + Aj_ori (Clase III Regular)",
        ),
    ]
    tabla_clases_rmr = Tabla(
        [
            "Rango RMR",
            "Clase",
            "Calidad del Macizo Rocoso",
            "Cohesión (kPa)",
            "Ángulo de Fricción (°)",
            "Tiempo de Autosoporte Referencial",
        ],
        [
            [
                "81 - 100",
                "I",
                "Muy Buena",
                "> 400",
                "> 45°",
                "20 años para claro de 15 m",
            ],
            [
                "61 - 80",
                "II",
                "Buena",
                "300 - 400",
                "35° - 45°",
                "1 año para claro de 10 m",
            ],
            [
                "41 - 60",
                "III",
                "Regular (CASO PORTAL PA14 = 42)",
                "200 - 300",
                "25° - 35°",
                "1 semana para claro de 5 m",
            ],
            [
                "21 - 40",
                "IV",
                "Mala",
                "100 - 200",
                "15° - 25°",
                "10 horas para claro de 2.5 m",
            ],
            ["< 21", "V", "Muy Mala", "< 100", "< 15°", "30 minutos para claro de 1 m"],
        ],
        "Tabla de Clasificación Geomecánica RMR de Bieniawski (1989)",
    )

    # 2. Hoja Teoria_Cargas_Terzaghi
    filas_terzaghi = [
        (
            "Ancho de excavación del túnel",
            "B_exc",
            r["ancho_b"],
            "m",
            "03_Seccion (Ancho herradura B = 13.30 m)",
        ),
        (
            "Altura de excavación del túnel",
            "Ht_exc",
            r["alto_h"],
            "m",
            "03_Seccion (Altura herradura Ht = 9.58 m)",
        ),
        (
            "Condición de roca según Terzaghi (1946)",
            "Cond_T",
            4,
            "-",
            "Condición 4: Medianamente fracturada en bloques algo abiertos",
        ),
        (
            "Factor de carga de roca de Terzaghi",
            "k_terz",
            r["k_terz"],
            "-",
            "Terzaghi (1946): Hp = 0.25*B a 0.35*(B + Ht)",
        ),
        (
            "Peso específico del macizo rocoso",
            "gamma_r",
            r["gamma_kn_m3"],
            "kN/m³",
            "Geomecánica del portal (2.65 t/m³)",
        ),
        (
            "Ancho de influencia de carga (B + Ht)",
            "C_terz",
            "={B_exc}+{Ht_exc}",
            "m",
            "C = B_exc + Ht_exc",
        ),
        (
            "Altura de carga de roca aflojada (Hp)",
            "Hp_terz",
            "={k_terz}*{C_terz}",
            "m",
            "Hp = k_terz * (B_exc + Ht_exc)",
        ),
        (
            "Altura total de diseño del frontón (Ht + Hp)",
            "H_front",
            "={Ht_exc}+{Hp_terz}",
            "m",
            "H_front = Ht_exc + Hp_terz",
        ),
        (
            "Presión vertical de soporte requerida (kPa)",
            "Pv_kpa",
            "={gamma_r}*{Hp_terz}",
            "kPa",
            "Pv = gamma_r * Hp_terz",
        ),
        (
            "Presión vertical de soporte requerida (MPa)",
            "Pv_mpa",
            "={Pv_kpa}/1000",
            "MPa",
            "Pv(MPa) = Pv(kPa) / 1000",
        ),
    ]
    filas_clases_terz = [
        [c["id"], c["condicion"], c["formula_hp"], c["factor_k"], c["observacion"]]
        for c in af_p.get("terzaghi_clases", [])
    ]
    tabla_clases_terz = Tabla(
        [
            "N°",
            "Condición del Macizo Rocoso (Terzaghi 1946)",
            "Carga de Roca (Altura Hp)",
            "Factor k Adoptado",
            "Observaciones Técnicas",
        ],
        filas_clases_terz,
        "Clasificación de Cargas de Roca de Karl Terzaghi (1946)",
    )

    # 3. Hoja Afrontonamiento_Portal
    filas_afrontonamiento = [
        (
            "Longitud total del equipo con cuchara en suelo (CAT 966H)",
            "L_eq",
            r["l_eq"],
            "m",
            f"Ficha Técnica CAT 966H ({r['link_ficha_cat966h']})",
        ),
        (
            "Ancho sobre neumáticos (CAT 966H)",
            "W_eq",
            r["w_eq"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Altura hasta el techo de la cabina (CAT 966H)",
            "H_cab",
            r["h_cab"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Radio de giro exterior de neumáticos (CAT 966H)",
            "R_giro",
            r["r_giro"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Altura de descarga máxima a 45° (CAT 966H)",
            "H_desc",
            r["h_desc"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Distancia de seguridad operacional lateral",
            "D_seg",
            r["d_seg"],
            "m",
            "D.S. 024-2016-EM (Resguardo de maniobra)",
        ),
        (
            "Ancho de la sección del túnel (B)",
            "B_tun",
            "=Teoria_Cargas_Terzaghi!C6",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Altura de la sección del túnel (Ht)",
            "H_tun",
            "=Teoria_Cargas_Terzaghi!C7",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Altura recta de hastiales",
            "H_hast",
            "={H_tun}-({B_tun}/2)",
            "m",
            "H_hast = H_tun - B_tun / 2",
        ),
        (
            "Área rectangular inferior del túnel",
            "A_rect",
            "={B_tun}*{H_hast}",
            "m²",
            "A_rect = B_tun * H_hast",
        ),
        (
            "Área semicircular de la bóveda",
            "A_bov",
            "=(PI()*({B_tun}/2)^2)/2",
            "m²",
            "A_bov = pi * (B_tun/2)² / 2",
        ),
        (
            "Área total de la sección del túnel a descontar",
            "A_tun",
            "={A_rect}+{A_bov}",
            "m²",
            "A_tun = A_rect + A_bov (03_Seccion)",
        ),
        (
            "Semiancho de maniobra en explanada de portal",
            "W_semi",
            "={R_giro}+{L_eq}+{D_seg}",
            "m",
            "W_semi = R_giro + L_eq + D_seg",
        ),
        (
            "Ancho total del frontón (2 * Semiancho)",
            "W_front",
            "=2*{W_semi}",
            "m",
            "W_front = 2 * W_semi",
        ),
        (
            "Altura total del frontón (Ht + Hp)",
            "H_front_p",
            "=Teoria_Cargas_Terzaghi!C13",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Área bruta total del frontón",
            "A_bruta",
            "={W_front}*{H_front_p}",
            "m²",
            "A_bruta = W_front * H_front",
        ),
        (
            "TOTAL ÁREA NETA A SELLAR / AFRONTONAR",
            "A_neta",
            "={A_bruta}-{A_tun}",
            "m²",
            "A_neta = A_bruta - A_tun",
        ),
    ]

    # 4. Hoja Malla_Electrosoldada
    filas_malla = [
        (
            "Área neta del frontón a sellar",
            "A_neta_m",
            "=Afrontonamiento_Portal!C22",
            "m²",
            "Vínculo dinámico a Afrontonamiento_Portal",
        ),
        (
            "Largo comercial del paño de malla electrosoldada",
            "L_pano",
            r["l_pano"],
            "m",
            "Paño estándar Q-188 (6.00 x 2.40 m)",
        ),
        (
            "Ancho comercial del paño de malla electrosoldada",
            "W_pano",
            r["w_pano"],
            "m",
            "Paño estándar Q-188 (6.00 x 2.40 m)",
        ),
        (
            "Traslape mínimo en ambos sentidos (3 cocadas)",
            "Traslape",
            r["traslape"],
            "m",
            "MTC EG-2013 / D.S. 024-2016-EM (0.30 m)",
        ),
        (
            "Largo efectivo útil del paño (con traslape)",
            "L_util",
            "={L_pano}-{Traslape}",
            "m",
            "L_util = L_pano - Traslape",
        ),
        (
            "Ancho efectivo útil del paño (con traslape)",
            "W_util",
            "={W_pano}-{Traslape}",
            "m",
            "W_util = W_pano - Traslape",
        ),
        (
            "Área neta efectiva cubierta por paño",
            "A_util_p",
            "={L_util}*{W_util}",
            "m²/paño",
            "A_util = L_util * W_util",
        ),
        (
            "Cantidad exacta de paños requeridos",
            "N_panos_ex",
            "={A_neta_m}/{A_util_p}",
            "paños",
            "N_exacto = A_neta / A_util",
        ),
        (
            "Cantidad de paños a instalar (Redondeo superior)",
            "N_panos",
            "=ROUNDUP({N_panos_ex}, 0)",
            "und",
            "ROUNDUP(N_exacto, 0)",
        ),
        (
            "Tiempo unitario de instalación por paño",
            "t_pano",
            r["t_inst_pano_min"],
            "min/paño",
            "Cuadrilla de emboquille con telehandler",
        ),
        (
            "Tiempo total de instalación de malla (minutos)",
            "T_malla_min",
            "={N_panos}*{t_pano}",
            "min",
            "T_min = N_panos * t_pano",
        ),
        (
            "TOTAL TIEMPO DE INSTALACIÓN DE MALLA (HORAS)",
            "T_malla_h",
            "={T_malla_min}/60",
            "h",
            "T_h = T_min / 60",
        ),
    ]

    # 5. Hoja Pernos_RockBolt
    filas_pernos = [
        (
            "Área neta del frontón a sellar",
            "A_neta_p",
            "=Afrontonamiento_Portal!C22",
            "m²",
            "Vínculo dinámico a Afrontonamiento_Portal",
        ),
        (
            "Longitud del perno RockBolt helicoidal",
            "L_perno",
            r["l_perno_f"],
            "m",
            "Barra helicoidal ASTM A615 G60 (3.00 m)",
        ),
        (
            "Diámetro de la barra del perno",
            "d_perno",
            r["d_perno_mm"],
            "mm",
            'Barra de 22 mm (7/8")',
        ),
        (
            "Diámetro de perforación del taladro",
            "d_tal",
            r["d_tal_mm"],
            "mm",
            'Broca de 32 mm (1 1/4")',
        ),
        (
            "Espaciamiento sistemático entre pernos (e x e)",
            "e_perno",
            r["esp_perno_f"],
            "m",
            "Cuadrícula de 1.50 x 1.50 m en Clase III",
        ),
        (
            "Área de influencia tributaria por perno",
            "A_trib",
            "={e_perno}^2",
            "m²/perno",
            "A_trib = e_perno²",
        ),
        (
            "Cantidad de pernos requeridos en el frontón",
            "N_pernos",
            "=ROUNDUP({A_neta_p}/{A_trib}, 0)",
            "und",
            "ROUNDUP(A_neta / A_trib, 0)",
        ),
        (
            "Diámetro del cartucho de resina epóxica/poliéster",
            "d_cart",
            r["d_cart_mm"],
            "mm",
            "Ficha técnica cartucho de resina (28 mm)",
        ),
        (
            "Longitud del cartucho de resina",
            "L_cart",
            r["l_cart_mm"],
            "mm",
            "Cartucho estándar de 305 mm (1 pie)",
        ),
        (
            "Peso unitario del cartucho de resina",
            "w_cart",
            r["peso_cart_g"],
            "g",
            "320 g por cartucho",
        ),
        (
            "Cantidad de cartuchos por caja comercial",
            "u_caja",
            r["cart_x_caja"],
            "und/caja",
            "Caja comercial de 50 unidades",
        ),
        (
            "Volumen total del taladro perforado",
            "V_tal_p",
            "=PI()*({d_tal}/2000)^2*{L_perno}",
            "m³",
            "V_tal = pi * (d_tal/2)² * L_perno",
        ),
        (
            "Volumen ocupado por la barra de acero",
            "V_bar",
            "=PI()*({d_perno}/2000)^2*{L_perno}",
            "m³",
            "V_bar = pi * (d_perno/2)² * L_perno",
        ),
        (
            "Volumen anular libre requerido de resina",
            "V_anul",
            "={V_tal_p}-{V_bar}",
            "m³",
            "V_anul = V_tal - V_bar",
        ),
        (
            "Volumen unitario de 1 cartucho de resina",
            "V_cart",
            "=PI()*({d_cart}/2000)^2*({L_cart}/1000)",
            "m³",
            "V_cart = pi * (d_cart/2)² * L_cart",
        ),
        (
            "Cartuchos de resina por taladro (Redondeado)",
            "N_cart_tal",
            "=ROUNDUP({V_anul}/{V_cart}, 0)",
            "und",
            "ROUNDUP(V_anul / V_cart, 0)",
        ),
        (
            "Total de cartuchos de resina para el frontón",
            "N_cart_tot",
            "={N_pernos}*{N_cart_tal}",
            "und",
            "N_pernos * N_cart_tal",
        ),
        (
            "Total de cajas de resina a suministrar",
            "N_cajas",
            "=ROUNDUP({N_cart_tot}/{u_caja}, 0)",
            "und",
            "ROUNDUP(N_cart_tot / u_caja, 0)",
        ),
        (
            "Masa total de resina epóxica requerida",
            "M_resina",
            "=({N_cart_tot}*{w_cart})/1000",
            "kg",
            "M_resina = N_cart_tot * w_cart / 1000",
        ),
        (
            "Velocidad de perforación del Bolter Robótico",
            "v_bolter",
            r["vel_bolter"],
            "m/min",
            "Ficha técnica Bolter Robótico (06_Maquinaria)",
        ),
        (
            "Tiempo de perforación pura por taladro",
            "t_perf_p",
            "={L_perno}/{v_bolter}",
            "min",
            "t_perf = L_perno / v_bolter",
        ),
        (
            "Tiempo de posicionamiento y maniobra del brazo",
            "t_man_p",
            r["t_man_bolter"],
            "min",
            "1.00 min por taladro",
        ),
        (
            "Tiempo de inyección de resina e inserción de perno",
            "t_iny_p",
            r["t_iny_bolter"],
            "min",
            "2.50 min por perno",
        ),
        (
            "Tiempo de ciclo completo por perno instalado",
            "t_ciclo_p",
            "={t_perf_p}+{t_man_p}+{t_iny_p}",
            "min/perno",
            "t_ciclo = t_perf + t_man + t_iny",
        ),
        (
            "TOTAL TIEMPO DE EMPERNADO CON BOLTER (HORAS)",
            "T_pernos_h",
            "=({N_pernos}*{t_ciclo_p})/60",
            "h",
            "T_h = (N_pernos * t_ciclo) / 60",
        ),
    ]

    # 6. Hoja Shotcrete_Robotizado
    filas_shotcrete = [
        (
            "Área neta del frontón a sellar",
            "A_neta_s",
            "=Afrontonamiento_Portal!C22",
            "m²",
            "Vínculo dinámico a Afrontonamiento_Portal",
        ),
        (
            "Espesor de diseño del concreto lanzado (Shotcrete)",
            "e_shot",
            r["e_shot_m"],
            "m",
            "e = 0.12 m (120 mm) para sellado Clase III",
        ),
        (
            "Factor de pérdida por rebote (Lanzado robotizado)",
            "f_reb",
            r["rebote"],
            "-",
            "10% de rebote vía húmeda robotizada",
        ),
        (
            "Volumen geométrico teórico de shotcrete",
            "V_shot_teo",
            "={A_neta_s}*{e_shot}",
            "m³",
            "V_teo = A_neta * e_shot",
        ),
        (
            "Volumen real de producción considerando rebote",
            "V_shot_real",
            "={V_shot_teo}*(1+{f_reb})",
            "m³",
            "V_real = V_teo * (1 + f_reb)",
        ),
        (
            "Dosificación de Cemento Portland Tipo I por m³",
            "Cem_m3",
            r["cem_kg_m3"],
            "kg/m³",
            "Diseño de mezcla f'c = 28 - 30 MPa",
        ),
        (
            "Peso comercial de 1 bolsa de cemento",
            "w_bolsa",
            r["peso_bolsa_kg"],
            "kg/bolsa",
            "Estándar comercial en Perú (42.5 kg)",
        ),
        (
            "Relación Agua / Cemento (A/C)",
            "Rel_AC",
            r["rel_ac"],
            "-",
            "Diseño reológico vía húmeda (0.58)",
        ),
        (
            "Dosificación de agregado / arena graduada por m³",
            "Arena_m3",
            r["arena_kg_m3"],
            "kg/m³",
            "Huso granulométrico EFNARC (1,700 kg/m³)",
        ),
        (
            "Porcentaje de aditivo acelerante SikaCem Gunite PE",
            "Pct_acel",
            r["acel_pct"],
            "-",
            "4.0% del peso del cemento",
        ),
        (
            "Porcentaje de adición de Nanosílice / Microsílice",
            "Pct_nano",
            r["nano_pct"],
            "-",
            "1.0% del peso del cemento",
        ),
        (
            "Dosificación de macrofibra sintética SikaFiber Force-60",
            "Fibra_m3",
            r["fibra_kg_m3"],
            "kg/m³",
            "Absorción de energía >= 500 J (EFNARC)",
        ),
        (
            "Cemento total requerido para el frontón",
            "Cem_tot",
            "={V_shot_real}*{Cem_m3}",
            "kg",
            "Cem_tot = V_real * Cem_m3",
        ),
        (
            "Cantidad total de bolsas de cemento (Redondeado)",
            "Bolsas_tot",
            "=ROUNDUP({Cem_tot}/{w_bolsa}, 0)",
            "und",
            "ROUNDUP(Cem_tot / 42.5, 0)",
        ),
        (
            "Agua de mezcla total requerida",
            "Agua_tot_l",
            "={V_shot_real}*({Cem_m3}*{Rel_AC})",
            "L",
            "Agua(L) = V_real * (Cem_m3 * A/C)",
        ),
        (
            "Arena graduada total requerida (Toneladas)",
            "Arena_tot_t",
            "=({V_shot_real}*{Arena_m3})/1000",
            "t",
            "Arena(t) = V_real * Arena_m3 / 1000",
        ),
        (
            "Aditivo acelerante SikaCem total requerido",
            "Acel_tot",
            "={Cem_tot}*{Pct_acel}",
            "kg",
            "Acel_tot = Cem_tot * Pct_acel",
        ),
        (
            "Nanosílice total requerida",
            "Nano_tot",
            "={Cem_tot}*{Pct_nano}",
            "kg",
            "Nano_tot = Cem_tot * Pct_nano",
        ),
        (
            "Macrofibra sintética SikaFiber total requerida",
            "Fibra_tot",
            "={V_shot_real}*{Fibra_m3}",
            "kg",
            "Fibra_tot = V_real * Fibra_m3",
        ),
        (
            "Rendimiento horario del Robot Lanzador de Shotcrete",
            "Rend_rob",
            r["rend_robot"],
            "m³/h",
            "Putzmeister Wetkret 4 / Normet (06_Maquinaria)",
        ),
        (
            "Tiempo efectivo de lanzado robotizado",
            "t_lanz_h",
            "={V_shot_real}/{Rend_rob}",
            "h",
            "t_lanz = V_real / Rend_rob",
        ),
        (
            "Tiempo de fraguado inicial requerido",
            "t_frag_h",
            r["t_fraguado_h"],
            "h",
            "Espera de endurecimiento temprano",
        ),
        (
            "TOTAL TIEMPO DE APLICACIÓN Y FRAGUADO DE SHOTCRETE",
            "T_shot_h",
            "={t_lanz_h}+{t_frag_h}",
            "h",
            "T_shot = t_lanz + t_frag",
        ),
    ]

    return Libro(
        "14_Afrontonamiento.xlsx",
        [
            Hoja(
                "RMR_Geomecanica",
                "Valoración Geomecánica RMR de Bieniawski (1989) en el Portal y Frontón",
                [
                    tabla_parametros(
                        filas_rmr, "Valoración RMR del Macizo Rocoso en el Frontón"
                    ),
                    tabla_clases_rmr,
                ],
            ),
            Hoja(
                "Teoria_Cargas_Terzaghi",
                "Teoría de Cargas de Roca de Karl Terzaghi (1946) Aplicada al Frontón del Portal",
                [
                    tabla_parametros(
                        filas_terzaghi,
                        "Cálculo de Altura de Carga (Hp) y Presión Vertical",
                    ),
                    tabla_clases_terz,
                ],
            ),
            Hoja(
                "Afrontonamiento_Portal",
                "Geometría del Afrontonamiento y Sellado del Portal (Maniobra CAT 966H) — Área Neta",
                [
                    tabla_parametros(
                        filas_afrontonamiento,
                        "Dimensionamiento del Frontón y Descuento de Sección del Túnel",
                    )
                ],
            ),
            Hoja(
                "Malla_Electrosoldada",
                "Cálculo de Malla Electrosoldada Q-188 en el Frontón del Portal",
                [
                    tabla_parametros(
                        filas_malla,
                        "Metrado de Paños con Traslape y Tiempo de Instalación",
                    )
                ],
            ),
            Hoja(
                "Pernos_RockBolt",
                "Cálculo de Pernos Helicoidales RockBolt, Cartuchos de Resina y Ciclo del Bolter",
                [
                    tabla_parametros(
                        filas_pernos,
                        "Dimensionamiento de Empernado Sistemático y Consumo de Resina",
                    )
                ],
            ),
            Hoja(
                "Shotcrete_Robotizado",
                "Dosificación y Rendimiento de Shotcrete Vía Húmeda con Fibra Sintética (Sellado del Portal)",
                [
                    tabla_parametros(
                        filas_shotcrete,
                        "Volúmenes, Insumos Sika y Tiempos de Lanzado Robotizado",
                    )
                ],
            ),
        ],
    )


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 14_Afrontonamiento.md del afrontonamiento y sellado del portal."""
    t_resumen_fronton = Tabla(
        [
            "Componente / Parámetro",
            "Valor Calculado",
            "Unidad",
            "Criterio Técnico / Fuente",
        ],
        [
            [
                "Valoración Geomecánica RMR Básico / Corregido",
                f"{r['rmr_basico']} / {r['rmr_corregido']}",
                "pts",
                "Bieniawski (1989) — Clase III (Roca Regular)",
            ],
            [
                "Altura de carga de roca aflojada (Hp Terzaghi)",
                r["hp_terzaghi_m"],
                "m",
                "Condición 4: Hp = 0.35 * (B + Ht)",
            ],
            [
                "Altura total del frontón (Ht + Hp)",
                r["h_fronton_m"],
                "m",
                f"Ht = {r['alto_h']} m + Hp = {r['hp_terzaghi_m']:.2f} m",
            ],
            [
                "Presión vertical de diseño sobre clave",
                r["presion_vert_kpa"],
                "kPa",
                f"gamma = {r['gamma_kn_m3']} kN/m³ * Hp",
            ],
            [
                "Ancho total de maniobra en portal (CAT 966H)",
                r["ancho_fronton_m"],
                "m",
                f"2 * (R_giro {r['r_giro']} + L_eq {r['l_eq']} + D_seg {r['d_seg']})",
            ],
            [
                "Área bruta del frontón",
                r["area_bruta_fronton_m2"],
                "m²",
                "Ancho frontón * Altura frontón",
            ],
            [
                "Área de la sección herradura del túnel descontada",
                r["area_tunel_m2"],
                "m²",
                "03_Seccion (13.30 x 9.58 m)",
            ],
            [
                "ÁREA NETA A SELLAR / AFRONTONAR EN EL PORTAL",
                r["area_neta_fronton_m2"],
                "m²",
                "Área bruta - Área sección del túnel",
            ],
            [
                "Paños de malla electrosoldada (6.0 x 2.4 m, traslape 0.30 m)",
                r["n_panos_malla"],
                "paños",
                f"Área útil {r['area_util_pano_m2']:.2f} m²/paño ({r['t_total_malla_h']:.2f} h)",
            ],
            [
                "Pernos RockBolt (L=3.0 m, d=22 mm, malla 1.5x1.5 m)",
                r["n_pernos_fronton"],
                "pernos",
                f"Ciclo Bolter Robótico: {r['t_total_empernado_h']:.2f} h",
            ],
            [
                "Cartuchos de resina epóxica (28x305 mm, 320 g)",
                r["total_cartuchos"],
                "cartuchos",
                f"{r['cartuchos_x_tal']} cart/perno ({r['total_cajas_resina']} cajas, {r['masa_resina_kg']:.1f} kg)",
            ],
            [
                "Volumen real de Shotcrete (e=0.12 m + 10% rebote)",
                r["vol_shot_real_m3"],
                "m³",
                f"Cemento: {r['bolsas_cemento']} bolsas, Fibra: {r['fibra_total_kg']:.1f} kg ({r['t_total_shotcrete_h']:.2f} h)",
            ],
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
