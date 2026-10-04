"""06 · Maquinaria: frente del túnel, botadero y campamento."""

import math

from ..modelo import Hoja, Libro, Tabla, tabla_parametros

CLAVE = "maquinaria"


def calcular(p: dict, ctx: dict) -> dict:
    m, sec = p["maquinaria"], ctx["seccion"]
    frentes = p["perforacion"]["frentes"]
    ventana_min = m["ventana_limpieza_h"] * 60 * m["eficiencia"]
    vs = sec["v_esponjado_disparo_m3"]

    # Jumbo: tiempo de perforación de un disparo
    j = m["jumbo"]
    t_perforacion_h = (
        sec["taladros"]
        * p["perforacion"]["longitud_barreno_m"]
        / (j["velocidad_perforacion_m_min"] * j["brazos"])
        / 60
    )

    # Scoop: limpieza del disparo dentro de la ventana
    s = m["scoop"]
    prod_scoop = s["capacidad_m3"] * s["factor_llenado"] * 60 / s["tiempo_ciclo_min"]
    n_scoop = math.ceil(vs / (prod_scoop * ventana_min / 60))

    # Dumper: transporte frente → botadero (caso crítico: frente más lejano)
    d = m["dumper"]
    distancia = sec["longitud_m"] / frentes + d["distancia_portal_botadero_m"]
    ciclo_dumper = (
        distancia / 1000 / d["velocidad_cargado_kmh"] * 60
        + distancia / 1000 / d["velocidad_vacio_kmh"] * 60
        + d["tiempo_fijo_min"]
    )
    viajes = math.ceil(vs / (d["capacidad_m3"] * d["factor_llenado"]))
    viajes_por_dumper = ventana_min / ciclo_dumper
    n_dumper = math.ceil(viajes / viajes_por_dumper)

    # Botadero
    b = m["botadero"]
    area_bot = sec["v_total_esponjado_m3"] / b["altura_m"] * b["factor_taludes"]
    n_tractor = math.ceil(
        sec["v_esponjado_dia_m3"]
        / (b["tractor_productividad_m3_h"] * b["horas_operacion_dia"])
    )

    calculados = [
        (
            "Frente",
            "Jumbo de perforación",
            1,
            True,
            j["potencia_hp"],
            False,
            "Calculado",
        ),
        (
            "Frente",
            "Scoop (cargador LHD)",
            n_scoop,
            True,
            s["potencia_hp"],
            True,
            "Calculado",
        ),
        (
            "Frente",
            "Dumper (volquete de bajo perfil)",
            n_dumper,
            True,
            d["potencia_hp"],
            True,
            "Calculado",
        ),
        (
            "Botadero",
            "Tractor de orugas",
            n_tractor,
            False,
            b["potencia_hp_tractor"],
            False,
            "Calculado",
        ),
    ]
    asignados = [
        (
            e["zona"],
            e["equipo"],
            e["cantidad"],
            e.get("por_frente", False),
            e["potencia_hp"],
            e.get("en_tunel", False),
            "Asignado",
        )
        for e in m["equipos"]
    ]
    equipos = []
    for zona, nombre, cant, por_frente, hp, en_tunel, origen in calculados + asignados:
        equipos.append(
            {
                "zona": zona,
                "equipo": nombre,
                "cantidad_frente": cant if por_frente else None,
                "cantidad": cant * frentes if por_frente else cant,
                "potencia_hp": hp,
                "en_tunel": en_tunel,
                "origen": origen,
            }
        )
    hp_tunel_frente = sum(
        (e["cantidad_frente"] or 0) * e["potencia_hp"] for e in equipos if e["en_tunel"]
    )
    return {
        "t_perforacion_h": t_perforacion_h,
        "prod_scoop_m3_h": prod_scoop,
        "n_scoop": n_scoop,
        "distancia_m": distancia,
        "ciclo_dumper_min": ciclo_dumper,
        "viajes": viajes,
        "viajes_por_dumper": viajes_por_dumper,
        "n_dumper": n_dumper,
        "area_botadero_m2": area_bot,
        "lado_botadero_m": math.sqrt(area_bot),
        "n_tractor": n_tractor,
        "equipos": equipos,
        "hp_tunel_frente": hp_tunel_frente,
    }


def _tabla_equipos(r: dict, zona: str) -> Tabla:
    return Tabla(
        [
            "Equipo",
            "Por frente",
            "Cantidad total",
            "Potencia (HP)",
            "Diésel en túnel",
            "Origen",
        ],
        [
            [
                e["equipo"],
                e["cantidad_frente"],
                e["cantidad"],
                e["potencia_hp"],
                e["en_tunel"],
                e["origen"],
            ]
            for e in r["equipos"]
            if e["zona"] == zona
        ],
        "Relación de equipos",
    )


def libro(r: dict, p: dict) -> Libro:
    m, f = p["maquinaria"], p["perforacion"]
    j, b = m["jumbo"], m["botadero"]
    frente = tabla_parametros(
        [
            (
                "Tiempo de perforación por disparo",
                "tp",
                r["t_perforacion_h"],
                "h",
                "N · Lb / (v · brazos) / 60",
            ),
            ("Ventana de perforación", "", j["ventana_perforacion_h"], "h", "Dato"),
            (
                "¿Un jumbo por frente es suficiente?",
                "",
                r["t_perforacion_h"] <= j["ventana_perforacion_h"],
                "",
                "tp ≤ ventana",
            ),
            (
                "Ventana de limpieza efectiva",
                "tv",
                m["ventana_limpieza_h"] * m["eficiencia"],
                "h",
                "ventana · eficiencia",
            ),
            (
                "Productividad del scoop",
                "Qs",
                r["prod_scoop_m3_h"],
                "m³/h",
                "C · fll · 60 / ciclo",
            ),
            ("Scoops por frente", "ns", r["n_scoop"], "und", "⌈Vs / (Qs · tv)⌉"),
            (
                "Distancia de acarreo crítica",
                "D",
                r["distancia_m"],
                "m",
                "L / nf + distancia a botadero",
            ),
            (
                "Ciclo del dumper",
                "td",
                r["ciclo_dumper_min"],
                "min",
                "D/vc + D/vv + t fijo",
            ),
            ("Viajes por disparo", "nv", r["viajes"], "und", "⌈Vs / (C · fll)⌉"),
            (
                "Viajes por dumper en la ventana",
                "vd",
                r["viajes_por_dumper"],
                "und",
                "tv / td",
            ),
            ("Dumpers por frente", "nd", r["n_dumper"], "und", "⌈nv / vd⌉"),
        ],
        f"Cálculo por frente ({f['frentes']} frentes)",
    )
    botadero = tabla_parametros(
        [
            ("Altura de apilamiento", "hb", b["altura_m"], "m", "Dato"),
            (
                "Área requerida",
                "Ab",
                r["area_botadero_m2"],
                "m²",
                "VTs / hb · f taludes",
            ),
            ("Lado equivalente", "Lb", r["lado_botadero_m"], "m", "√Ab"),
            (
                "Tractores de orugas",
                "nt",
                r["n_tractor"],
                "und",
                "⌈Vs día / (Qt · horas)⌉",
            ),
        ],
        "Cálculo del botadero (VTs y Vs día: 03_Seccion)",
    )
    return Libro(
        "06_Maquinaria.xlsx",
        [
            Hoja(
                "Frente",
                "Maquinaria del frente del túnel",
                [frente, _tabla_equipos(r, "Frente")],
            ),
            Hoja(
                "Botadero",
                "Maquinaria y dimensión del botadero",
                [botadero, _tabla_equipos(r, "Botadero")],
            ),
            Hoja(
                "Campamento",
                "Maquinaria de campamento (grupo electrógeno: ver 09_Electricidad)",
                [_tabla_equipos(r, "Campamento")],
            ),
        ],
    )
