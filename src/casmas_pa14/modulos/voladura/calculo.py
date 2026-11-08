"""Motor de cálculo matemático para voladura subterránea en el frente del túnel (Jumbo 3 brazos)."""

from __future__ import annotations

from typing import Any


def calcular_voladura_tunel(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula la perforación y voladura subterránea del túnel con Jumbo 3 brazos Sandvik DT1131."""
    vol = p.get("voladura", {})
    perf = p.get("perforacion", {})
    sec = ctx.get("seccion", {})

    ancho_m = float(sec.get("ancho_m", 13.30))
    altura_m = float(sec.get("altura_m", 9.58))
    area_m2 = float(sec.get("area_m2", 108.43))
    perimetro_m = float(sec.get("perimetro_m", 39.99))

    equipo_tunel = str(
        vol.get(
            "equipo_perforacion_tunel",
            "Jumbo Frontal Computarizado 3 brazos Sandvik DT1131 / XE3C",
        )
    )
    brazos_jumbo = int(vol.get("brazos_jumbo", 3))
    potencia_jumbo_hp = int(vol.get("potencia_jumbo_hp", 300))
    vp_m_min = float(vol.get("velocidad_penetracion_m_min", 1.50))
    lb_m = float(perf.get("longitud_barreno_m", 3.66))
    ef_avance = float(perf.get("eficiencia_avance", 0.90))
    esp_perif_m = float(perf.get("espaciamiento_periferico_m", 0.60))
    k_langefors = float(perf.get("coeficiente_roca_k", 1.50))
    fc_especifico = float(perf.get("factor_carga_kg_m3", 1.60))

    d_alivio_mm = float(vol.get("diametro_alivio_mm", 102.0))
    de_mm = float(vol.get("diametro_explosivo_mm", 45.0))

    n_alivio_vacios = int(vol.get("taladros_alivio_vacios", 4))
    n_cuele = int(vol.get("taladros_cuele_und", 16))
    n_ayudas = int(vol.get("taladros_ayudas_und", 20))
    n_destroza = int(vol.get("taladros_destroza_und", 105))
    n_cuadradores = int(vol.get("taladros_cuadradores_und", 22))
    n_corona = int(vol.get("taladros_corona_und", 42))
    n_arrastres = int(vol.get("taladros_arrastres_und", 26))

    taladros_cargados = (
        n_cuele + n_ayudas + n_destroza + n_cuadradores + n_corona + n_arrastres
    )
    taladros_perforados = taladros_cargados + n_alivio_vacios
    avance_disparo_m = lb_m * ef_avance
    vol_disparo_m3 = area_m2 * avance_disparo_m
    metros_perf_disparo = taladros_perforados * lb_m
    tiempo_perf_neto_h = metros_perf_disparo / (vp_m_min * brazos_jumbo * 60.0)
    kg_explosivo_disparo = vol_disparo_m3 * fc_especifico

    sge = float(vol.get("densidad_explosivo_g_cm3", 1.20))
    sgr = float(vol.get("densidad_roca_g_cm3", 2.60))
    h = float(vol.get("altura_banco_m", avance_disparo_m))
    th_factor = float(vol.get("constante_retardo_ms_m", 4.5))
    tr_factor = float(vol.get("factor_tiempo_filas_ms_m", 11.5))
    kr_lineas = float(vol.get("factor_kr_lineas", 0.90))
    kd_depo = float(vol.get("factor_kd_depositacion", 1.00))
    ks_estr = float(vol.get("factor_ks_estructura", 1.10))

    if "geologia" in ctx and ctx["geologia"].get("tramos"):
        primer_tramo = ctx["geologia"]["tramos"][0]
        if isinstance(primer_tramo, dict) and "densidad_t_m3" in primer_tramo:
            sgr = float(primer_tramo["densidad_t_m3"])

    burden_m = 0.012 * ((2.0 * (sge / sgr)) + 1.5) * de_mm
    burden_corr_m = burden_m * kr_lineas * kd_depo * ks_estr
    espaciamiento_m = 1.4 * burden_m
    sobre_perf_m = 0.3 * burden_m
    taco_m = 0.7 * burden_m
    rigidez = h / burden_m if burden_m > 0 else 0.0
    longitud_taladro_m = h + sobre_perf_m
    vol_romper_m3 = burden_m * espaciamiento_m * h
    de_cm = de_mm / 10.0
    qbk_kg_m = 0.078539 * sge * (de_cm**2)

    carga_fondo_m = 1.3 * burden_m
    carga_columna_m = max(0.0, longitud_taladro_m - (carga_fondo_m + taco_m))
    if carga_columna_m == 0:
        carga_fondo_m = max(0.0, longitud_taladro_m - taco_m)

    carga_total_kg = (carga_fondo_m + carga_columna_m) * qbk_kg_m
    factor_carga_kg_m3 = carga_total_kg / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    toneladas_romper = vol_romper_m3 * sgr
    factor_potencia_kg_tm = (
        carga_total_kg / toneladas_romper if toneladas_romper > 0 else 0.0
    )
    retardo_barrenos_ms = th_factor * espaciamiento_m
    retardo_filas_ms = tr_factor * burden_m
    perf_especifica_m_m3 = (
        longitud_taladro_m / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    )

    return {
        "frente_tunel": {
            "equipo_tunel": equipo_tunel,
            "brazos_jumbo": brazos_jumbo,
            "potencia_jumbo_hp": potencia_jumbo_hp,
            "vp_m_min": vp_m_min,
            "ancho_m": ancho_m,
            "altura_m": altura_m,
            "area_m2": area_m2,
            "perimetro_m": perimetro_m,
            "lb_m": lb_m,
            "ef_avance": ef_avance,
            "esp_perif_m": esp_perif_m,
            "k_langefors": k_langefors,
            "fc_especifico": fc_especifico,
            "d_alivio_mm": d_alivio_mm,
            "de_mm": de_mm,
            "n_alivio_vacios": n_alivio_vacios,
            "n_cuele": n_cuele,
            "n_ayudas": n_ayudas,
            "n_destroza": n_destroza,
            "n_cuadradores": n_cuadradores,
            "n_corona": n_corona,
            "n_arrastres": n_arrastres,
            "taladros_cargados": taladros_cargados,
            "taladros_perforados": taladros_perforados,
            "avance_disparo_m": avance_disparo_m,
            "vol_disparo_m3": vol_disparo_m3,
            "metros_perf_disparo": metros_perf_disparo,
            "tiempo_perf_neto_h": tiempo_perf_neto_h,
            "kg_explosivo_disparo": kg_explosivo_disparo,
        },
        "inputs": {
            "sge": sge,
            "sgr": sgr,
            "de_mm": de_mm,
            "h": h,
            "th_factor": th_factor,
            "tr_factor": tr_factor,
            "kr_lineas": kr_lineas,
            "kd_depo": kd_depo,
            "ks_estr": ks_estr,
            "burden_m": burden_m,
            "espaciamiento_m": espaciamiento_m,
        },
        "calculados": {
            "burden_m": burden_m,
            "burden_corr_m": burden_corr_m,
            "espaciamiento_m": espaciamiento_m,
            "sobre_perf_m": sobre_perf_m,
            "taco_m": taco_m,
            "rigidez": rigidez,
            "longitud_taladro_m": longitud_taladro_m,
            "vol_romper_m3": vol_romper_m3,
            "qbk_kg_m": qbk_kg_m,
            "carga_fondo_m": carga_fondo_m,
            "carga_columna_m": carga_columna_m,
            "carga_total_kg": carga_total_kg,
            "factor_carga_kg_m3": factor_carga_kg_m3,
            "factor_potencia_kg_tm": factor_potencia_kg_tm,
            "retardo_barrenos_ms": retardo_barrenos_ms,
            "retardo_filas_ms": retardo_filas_ms,
            "perf_especifica_m_m3": perf_especifica_m_m3,
        },
    }
