"""08 · Agua: consumo, PETAP, PETAR y pozo de agua."""

import math

from ..modelo import Hoja, Libro, redondear_arriba, tabla_parametros

CLAVE = "agua"
_G = 9.81
_RHO = 1000.0


def calcular(p: dict, ctx: dict) -> dict:
    a, pob = p["agua"], ctx["personal"]["total"]
    f = p["perforacion"]

    # Consumo humano (RNE OS.100)
    q_humano_dia = pob * a["dotacion_l_hab_dia"] / 1000  # m³/día
    qp = pob * a["dotacion_l_hab_dia"] / 86400  # L/s
    qmd, qmh = a["k1"] * qp, a["k2"] * qp

    # Consumo industrial dinámico
    horas_perf = (
        ctx["maquinaria"]["t_perforacion_h"]
        * f["disparos_por_dia_frente"]
        * f["frentes"]
    )
    q_perforacion = (
        a["perforacion_l_min_brazo"]
        * p["maquinaria"]["jumbo"]["brazos"]
        * 60
        * horas_perf
        / 1000
    )

    # Agua para shotcrete de sostenimiento primario (según avance diario del túnel)
    avance_dia = (
        f["disparos_por_dia_frente"]
        * f["frentes"]
        * f["longitud_barreno_m"]
        * f["eficiencia_avance"]
    )
    ancho_sec, alt_sec = p["seccion"]["ancho_m"], p["seccion"]["altura_m"]
    perim_sec = math.pi * (ancho_sec / 2) + 2 * (alt_sec - ancho_sec / 2)
    vol_shotcrete = avance_dia * perim_sec * a["espesor_shotcrete_m"]
    q_shotcrete = vol_shotcrete * a["agua_shotcrete_l_m3"] / 1000

    # Agua para lavado de maquinaria pesada y mitigación de polvo
    q_lavado = a["equipos_lavado_und"] * a["lavado_equipo_l_dia"] / 1000
    q_riego = a["area_riego_m2"] * a["tasa_riego_l_m2_dia"] / 1000

    q_industrial = q_perforacion + q_shotcrete + q_lavado + q_riego
    q_total = q_humano_dia + q_industrial

    # PTAP (solo consumo humano)
    t = p["petap"]
    v_reservorio = t["fraccion_regulacion"] * qmd * 86.4 + t["reserva_m3"]
    lado_reservorio = redondear_arriba(
        math.sqrt(v_reservorio / t["altura_tanque_m"]), 0.1
    )
    area_filtro = qmd * 3.6 / t["tasa_filtracion_m_h"]
    cloro_kg_dia = qmd * 86.4 * t["dosis_cloro_mg_l"] / 1000 / t["pureza_hipoclorito"]
    p_ptap = qmd * 86.4 * t.get("kw_especifico_por_m3_dia", 0.06)

    # PETAR — tanque séptico (RNE IS.020)
    r = p["petar"]
    q_aporte = a["dotacion_l_hab_dia"] * r["coef_retorno"]  # L/hab/día
    v_residual_dia = pob * q_aporte / 1000  # m³/día
    pr = max(1.5 - 0.3 * math.log10(pob * q_aporte), 0.25)  # días
    v_sed = pob * q_aporte * pr / 1000
    v_lodos = r["tasa_lodos_l_hab_anio"] * pob * r["intervalo_limpieza_anios"] / 1000
    v_tanque = v_sed + v_lodos + r["volumen_natas_m3"]
    ancho_ts = redondear_arriba(
        math.sqrt(v_tanque / (r["altura_util_m"] * r["relacion_largo_ancho"])), 0.1
    )
    largo_ts = redondear_arriba(ancho_ts * r["relacion_largo_ancho"], 0.1)
    p_ptar = v_residual_dia * r.get("kw_especifico_por_m3_dia", 0.05)

    # Pozo (abastece consumo total)
    z = p["pozo"]
    q_bombeo = q_total / (z["horas_bombeo"] * 3600)  # m³/s
    altura_din = z["nivel_dinamico_m"] + z["altura_elevacion_m"] + z["perdidas_m"]
    p_bomba = _RHO * _G * q_bombeo * altura_din / z["eficiencia_bomba"] / 1000
    return {
        "poblacion": pob,
        "q_humano_dia_m3": q_humano_dia,
        "qp_l_s": qp,
        "qmd_l_s": qmd,
        "qmh_l_s": qmh,
        "horas_perforacion": horas_perf,
        "q_perforacion_m3": q_perforacion,
        "avance_dia_m": avance_dia,
        "vol_shotcrete_m3": vol_shotcrete,
        "q_shotcrete_m3": q_shotcrete,
        "q_lavado_m3": q_lavado,
        "q_riego_m3": q_riego,
        "q_industrial_m3": q_industrial,
        "q_total_m3": q_total,
        "v_reservorio_m3": v_reservorio,
        "lado_reservorio_m": lado_reservorio,
        "area_filtro_m2": area_filtro,
        "cloro_kg_dia": cloro_kg_dia,
        "p_ptap_kw": p_ptap,
        "q_aporte_l_hab": q_aporte,
        "v_residual_dia_m3": v_residual_dia,
        "pr_dias": pr,
        "v_sed_m3": v_sed,
        "v_lodos_m3": v_lodos,
        "v_tanque_m3": v_tanque,
        "ancho_ts_m": ancho_ts,
        "largo_ts_m": largo_ts,
        "p_ptar_kw": p_ptar,
        "q_bombeo_l_s": q_bombeo * 1000,
        "altura_dinamica_m": altura_din,
        "p_bomba_kw": p_bomba,
    }


def libro(r: dict, p: dict) -> Libro:
    a, t, s, z = p["agua"], p["petap"], p["petar"], p["pozo"]
    pozo_pt = next((x for x in p["ubicacion"]["puntos"] if x["id"] == "POZ"), None)
    coord_pozo = (
        f"{pozo_pt['este']:.0f}, {pozo_pt['norte']:.0f}, {pozo_pt['cota']:.0f}"
        if pozo_pt
        else "Por definir por el usuario"
    )
    consumo = tabla_parametros(
        [
            ("Población", "Pob", r["poblacion"], "personas", "04_Personal"),
            (
                "Dotación",
                "Dot",
                a["dotacion_l_hab_dia"],
                "L/hab/día",
                "RNE IS.010 Art. 2.2 / DS 024-2016-EM",
            ),
            (
                "Consumo humano diario",
                "Vh",
                "=C5*C6/1000",
                "m³/día",
                "Pob · Dot / 1000",
            ),
            ("Caudal promedio", "Qp", "=C5*C6/86400", "L/s", "Pob · Dot / 86400"),
            (
                "Caudal máximo diario",
                "Qmd",
                f"={a['k1']}*C8",
                "L/s",
                "k1 · Qp (RNE OS.100)",
            ),
            (
                "Caudal máximo horario",
                "Qmh",
                f"={a['k2']}*C8",
                "L/s",
                "k2 · Qp (RNE OS.100)",
            ),
            (
                "Horas de perforación por día",
                "hp",
                r["horas_perforacion"],
                "h",
                "tp · disparos/día",
            ),
            (
                "Agua de perforación (Jumbo)",
                "Vp",
                f"={a['perforacion_l_min_brazo']}*{p['maquinaria']['jumbo']['brazos']}*60*C11/1000",
                "m³/día",
                "q · brazos · 60 · hp / 1000",
            ),
            (
                "Agua de shotcrete (Sostenimiento)",
                "Vs",
                r["q_shotcrete_m3"],
                "m³/día",
                f"Avance ({r['avance_dia_m']:.1f} m) · Perim · Espesor · Ratio",
            ),
            (
                "Agua de lavado de flota minera",
                "Vl",
                f"={a['equipos_lavado_und']}*{a['lavado_equipo_l_dia']}/1000",
                "m³/día",
                f"{a['equipos_lavado_und']} equipos · {a['lavado_equipo_l_dia']} L/día",
            ),
            (
                "Riego y mitigación de polvo",
                "Vr",
                f"={a['area_riego_m2']}*{a['tasa_riego_l_m2_dia']}/1000",
                "m³/día",
                f"{a['area_riego_m2']} m² · {a['tasa_riego_l_m2_dia']} L/m²/día",
            ),
            (
                "Consumo industrial total",
                "Vi",
                "=SUM(C12:C15)",
                "m³/día",
                "Vp + Vs + Vl + Vr",
            ),
            ("CONSUMO TOTAL DE AGUA", "VT", "=C7+C16", "m³/día", "Vh + Vi"),
        ]
    )
    petap = tabla_parametros(
        [
            (
                "Caudal de diseño",
                "Qmd",
                "='Consumo'!C9",
                "L/s",
                "Consumo humano (RNE OS.100)",
            ),
            (
                "Volumen de reservorio",
                "Vr",
                f"={t['fraccion_regulacion']}*C6*86.4+{t['reserva_m3']}",
                "m³",
                f"{t['fraccion_regulacion']}·Qmd·86.4 + reserva (RNE OS.030)",
            ),
            (
                "Reservorio (lado × lado × altura)",
                "",
                f"{r['lado_reservorio_m']:.1f} × {r['lado_reservorio_m']:.1f} × {t['altura_tanque_m']}",
                "m",
                "√(Vr / h)",
            ),
            (
                "Área de filtro lento",
                "Af",
                f"=C6*3.6/{t['tasa_filtracion_m_h']}",
                "m²",
                "Qmd · 3.6 / tasa filtración (RNE OS.020)",
            ),
            (
                "Hipoclorito de calcio",
                "Cl",
                f"=C6*86.4*{t['dosis_cloro_mg_l']}/1000/{t['pureza_hipoclorito']}",
                "kg/día",
                "Q · dosis / pureza (DS 031-2010-SA)",
            ),
            (
                "Potencia eléctrica de dosificación y bombas",
                "P_ptap",
                f"=C6*86.4*{t.get('kw_especifico_por_m3_dia', 0.06)}",
                "kW",
                f"Qmd · 86.4 · {t.get('kw_especifico_por_m3_dia', 0.06)} kW/(m³/día)",
            ),
        ],
        "Planta de Tratamiento de Agua Potable (RNE OS.020 / OS.030)",
    )
    petar = tabla_parametros(
        [
            (
                "Aporte unitario",
                "q",
                f"='Consumo'!C6*{s['coef_retorno']}",
                "L/hab/día",
                "Dot · coef. retorno (RNE IS.020 Art. 4.1)",
            ),
            (
                "Volumen diario de aguas residuales",
                "Vr",
                "='Consumo'!C5*C6/1000",
                "m³/día",
                "Pob · q / 1000",
            ),
            (
                "Periodo de retención",
                "PR",
                "=MAX(1.5-0.3*LOG10('Consumo'!C5*C6), 0.25)",
                "días",
                "1.5 − 0.3·log(Pob·q) ≥ 0.25 (RNE IS.020 Art. 4.2)",
            ),
            (
                "Volumen de sedimentación",
                "Vs",
                "='Consumo'!C5*C6*C8/1000",
                "m³",
                "Pob · q · PR / 1000 (RNE IS.020)",
            ),
            (
                "Volumen de lodos",
                "Vd",
                f"={s['tasa_lodos_l_hab_anio']}*'Consumo'!C5*{s['intervalo_limpieza_anios']}/1000",
                "m³",
                "ta · Pob · N / 1000 (RNE IS.020 Tabla 1)",
            ),
            (
                "Volumen de natas",
                "Vn",
                s["volumen_natas_m3"],
                "m³",
                "Mínimo RNE IS.020 Art. 4.4",
            ),
            (
                "Volumen útil del tanque séptico",
                "Vt",
                "=C9+C10+C11",
                "m³",
                "Vs + Vd + Vn (RNE IS.020)",
            ),
            (
                "Tanque (largo × ancho × altura útil)",
                "",
                f"{r['largo_ts_m']:.1f} × {r['ancho_ts_m']:.1f} × {s['altura_util_m']}",
                "m",
                f"L = {s['relacion_largo_ancho']}·A (RNE IS.020)",
            ),
            (
                "Potencia eléctrica de aireación y bombeo",
                "P_ptar",
                f"=C7*{s.get('kw_especifico_por_m3_dia', 0.05)}",
                "kW",
                f"Vr · {s.get('kw_especifico_por_m3_dia', 0.05)} kW/(m³/día)",
            ),
        ],
        "Tanque séptico (RNE IS.020)",
    )
    pozo = tabla_parametros(
        [
            (
                "Coordenadas (E, N, cota)",
                "",
                coord_pozo,
                "m",
                "Distancias: 01_Ubicacion" if pozo_pt else "Por definir",
            ),
            (
                "Volumen diario a bombear",
                "VT",
                "='Consumo'!C17",
                "m³/día",
                "Consumo total diario",
            ),
            ("Horas de bombeo", "hb", z["horas_bombeo"], "h", "Régimen de operación"),
            ("Caudal de bombeo", "Qb", "=C7/(C8*3600)*1000", "L/s", "VT / (hb · 3600)"),
            (
                "Altura dinámica total",
                "HDT",
                f"={z['nivel_dinamico_m']}+{z['altura_elevacion_m']}+{z['perdidas_m']}",
                "m",
                "Nivel dinámico + elevación + pérdidas",
            ),
            (
                "Potencia de la bomba",
                "Pb",
                f"=1000*9.81*(C9/1000)*C10/{z['eficiencia_bomba']}/1000",
                "kW",
                "ρ·g·Qb·HDT / η (RNE OS.010)",
            ),
        ],
        "Sistema de captación por pozo profundo (RNE OS.010)",
    )
    return Libro(
        "08_Agua.xlsx",
        [
            Hoja("Consumo", "Consumo de agua", [consumo]),
            Hoja("PETAP", "Planta de tratamiento de agua potable", [petap]),
            Hoja("PETAR", "Planta de tratamiento de aguas residuales", [petar]),
            Hoja("Pozo", "Pozo de agua", [pozo]),
        ],
    )
