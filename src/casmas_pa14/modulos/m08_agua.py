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

    # Consumo industrial
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
    q_industrial = q_perforacion + a["riego_m3_dia"] + a["otros_industrial_m3_dia"]
    q_total = q_humano_dia + q_industrial

    # PETAP (solo consumo humano)
    t = p["petap"]
    v_reservorio = t["fraccion_regulacion"] * qmd * 86.4 + t["reserva_m3"]
    lado_reservorio = redondear_arriba(
        math.sqrt(v_reservorio / t["altura_tanque_m"]), 0.1
    )
    area_filtro = qmd * 3.6 / t["tasa_filtracion_m_h"]
    cloro_kg_dia = qmd * 86.4 * t["dosis_cloro_mg_l"] / 1000 / t["pureza_hipoclorito"]

    # PETAR — tanque séptico (RNE IS.020)
    r = p["petar"]
    q_aporte = a["dotacion_l_hab_dia"] * r["coef_retorno"]  # L/hab/día
    pr = max(1.5 - 0.3 * math.log10(pob * q_aporte), 0.25)  # días
    v_sed = pob * q_aporte * pr / 1000
    v_lodos = r["tasa_lodos_l_hab_anio"] * pob * r["intervalo_limpieza_anios"] / 1000
    v_tanque = v_sed + v_lodos + r["volumen_natas_m3"]
    ancho_ts = redondear_arriba(
        math.sqrt(v_tanque / (r["altura_util_m"] * r["relacion_largo_ancho"])), 0.1
    )
    largo_ts = redondear_arriba(ancho_ts * r["relacion_largo_ancho"], 0.1)

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
        "q_industrial_m3": q_industrial,
        "q_total_m3": q_total,
        "v_reservorio_m3": v_reservorio,
        "lado_reservorio_m": lado_reservorio,
        "area_filtro_m2": area_filtro,
        "cloro_kg_dia": cloro_kg_dia,
        "q_aporte_l_hab": q_aporte,
        "pr_dias": pr,
        "v_sed_m3": v_sed,
        "v_lodos_m3": v_lodos,
        "v_tanque_m3": v_tanque,
        "ancho_ts_m": ancho_ts,
        "largo_ts_m": largo_ts,
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
                "Dato (RNE IS.010)",
            ),
            (
                "Consumo humano diario",
                "Vh",
                r["q_humano_dia_m3"],
                "m³/día",
                "Pob · Dot / 1000",
            ),
            ("Caudal promedio", "Qp", r["qp_l_s"], "L/s", "Pob · Dot / 86400"),
            ("Caudal máximo diario", "Qmd", r["qmd_l_s"], "L/s", "k1 · Qp"),
            ("Caudal máximo horario", "Qmh", r["qmh_l_s"], "L/s", "k2 · Qp"),
            (
                "Horas de perforación por día",
                "hp",
                r["horas_perforacion"],
                "h",
                "tp · disparos/día",
            ),
            (
                "Agua de perforación",
                "Vp",
                r["q_perforacion_m3"],
                "m³/día",
                "q · brazos · 60 · hp / 1000",
            ),
            (
                "Riego + otros usos",
                "Vo",
                a["riego_m3_dia"] + a["otros_industrial_m3_dia"],
                "m³/día",
                "Dato",
            ),
            ("Consumo industrial", "Vi", r["q_industrial_m3"], "m³/día", "Vp + Vo"),
            ("CONSUMO TOTAL DE AGUA", "VT", r["q_total_m3"], "m³/día", "Vh + Vi"),
        ]
    )
    petap = tabla_parametros(
        [
            ("Caudal de diseño", "Qmd", r["qmd_l_s"], "L/s", "Consumo humano"),
            (
                "Volumen de reservorio",
                "Vr",
                r["v_reservorio_m3"],
                "m³",
                f"{t['fraccion_regulacion']}·Qmd·86.4 + reserva",
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
                r["area_filtro_m2"],
                "m²",
                "Qmd · 3.6 / tasa de filtración",
            ),
            (
                "Hipoclorito de calcio",
                "Cl",
                r["cloro_kg_dia"],
                "kg/día",
                "Q · dosis / pureza",
            ),
        ]
    )
    petar = tabla_parametros(
        [
            (
                "Aporte unitario",
                "q",
                r["q_aporte_l_hab"],
                "L/hab/día",
                "Dot · coef. retorno",
            ),
            (
                "Periodo de retención",
                "PR",
                r["pr_dias"],
                "días",
                "1.5 − 0.3·log(Pob·q) ≥ 0.25 (IS.020)",
            ),
            (
                "Volumen de sedimentación",
                "Vs",
                r["v_sed_m3"],
                "m³",
                "Pob · q · PR / 1000",
            ),
            ("Volumen de lodos", "Vd", r["v_lodos_m3"], "m³", "ta · Pob · N / 1000"),
            ("Volumen de natas", "Vn", s["volumen_natas_m3"], "m³", "Mínimo IS.020"),
            (
                "Volumen útil del tanque séptico",
                "Vt",
                r["v_tanque_m3"],
                "m³",
                "Vs + Vd + Vn",
            ),
            (
                "Tanque (largo × ancho × altura útil)",
                "",
                f"{r['largo_ts_m']:.1f} × {r['ancho_ts_m']:.1f} × {s['altura_util_m']}",
                "m",
                f"L = {s['relacion_largo_ancho']}·A",
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
                r["q_total_m3"],
                "m³/día",
                "Consumo total",
            ),
            ("Horas de bombeo", "hb", z["horas_bombeo"], "h", "Dato"),
            ("Caudal de bombeo", "Qb", r["q_bombeo_l_s"], "L/s", "VT / (hb · 3600)"),
            (
                "Altura dinámica total",
                "HDT",
                r["altura_dinamica_m"],
                "m",
                "Nivel dinámico + elevación + pérdidas",
            ),
            ("Potencia de la bomba", "Pb", r["p_bomba_kw"], "kW", "ρ·g·Qb·HDT / η"),
        ]
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
