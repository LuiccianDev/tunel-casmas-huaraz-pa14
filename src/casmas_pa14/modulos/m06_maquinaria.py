"""06 · Maquinaria: frente del túnel, botadero, campamento y fichas técnicas."""

import math

from ..catalogos import FICHAS_TECNICAS
from .maquinaria_hojas import (
    _tabla_equipos,
    _tabla_ficha_individual,
    _tabla_resumen_fichas,
    libro,
    memoria,
)

CLAVE = "maquinaria"

__all__ = [
    "CLAVE",
    "calcular",
    "libro",
    "memoria",
    "_tabla_equipos",
    "_tabla_ficha_individual",
    "_tabla_resumen_fichas",
]


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

    # Cargador Frontal: limpieza del disparo dentro de la ventana
    s = m["cargador_frente"]
    prod_cargador = s["capacidad_m3"] * s["factor_llenado"] * 60 / s["tiempo_ciclo_min"]
    n_cargador = math.ceil(vs / (prod_cargador * ventana_min / 60))

    # Volquete: transporte frente → botadero
    d = m["volquete_frente"]
    distancia = sec["longitud_m"] / frentes + d["distancia_portal_botadero_m"]
    ciclo_volquete = (
        distancia / 1000 / d["velocidad_cargado_kmh"] * 60
        + distancia / 1000 / d["velocidad_vacio_kmh"] * 60
        + d["tiempo_fijo_min"]
    )
    viajes = math.ceil(vs / (d["capacidad_m3"] * d["factor_llenado"]))
    viajes_por_volquete = ventana_min / ciclo_volquete
    n_volquete = math.ceil(viajes / viajes_por_volquete)

    # Botadero
    b = m["botadero"]
    area_bot = sec["v_total_esponjado_m3"] / b["altura_m"] * b["factor_taludes"]
    n_tractor = math.ceil(
        sec["v_esponjado_dia_m3"]
        / (b["tractor_productividad_m3_h"] * b["horas_operacion_dia"])
    )

    # Banquetas
    ban = m["banquetas"]
    horas_sup = b["horas_operacion_dia"]
    n_exc_banq = max(
        1,
        math.ceil(
            ban["volumen_movimiento_m3_dia"]
            / (ban["rendimiento_excavadora_m3_h"] * horas_sup)
        ),
    )
    n_volq_banq = max(
        1,
        math.ceil(
            ban["volumen_movimiento_m3_dia"]
            / (ban["rendimiento_volquete_m3_h"] * horas_sup)
        ),
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
            "Cargador Frontal",
            n_cargador,
            True,
            s["potencia_hp"],
            True,
            "Calculado",
        ),
        (
            "Frente",
            "Camión Volquete",
            n_volquete,
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
        (
            "Banquetas",
            "Perforadora de Orugas (Rockdrill)",
            1,
            False,
            ban["potencia_hp_perforadora"],
            False,
            "Calculado",
        ),
        (
            "Banquetas",
            "Excavadora Hidráulica",
            n_exc_banq,
            False,
            ban["potencia_hp_excavadora"],
            False,
            "Calculado",
        ),
        (
            "Banquetas",
            "Camión Volquete Rígido",
            n_volq_banq,
            False,
            ban["potencia_hp_volquete"],
            False,
            "Calculado",
        ),
        (
            "Accesos",
            "Tractor de Orugas Pesado (D8)",
            1,
            False,
            m["accesos"]["potencia_hp_d8"],
            False,
            "Calculado",
        ),
        (
            "Accesos",
            "Tractor de Orugas Mediano (D6)",
            1,
            False,
            m["accesos"]["potencia_hp_d6"],
            False,
            "Calculado",
        ),
        (
            "Accesos",
            "Excavadora Hidráulica",
            1,
            False,
            m["accesos"]["potencia_hp_excavadora"],
            False,
            "Calculado",
        ),
        (
            "Accesos",
            "Camión Volquete Rígido",
            m["accesos"]["volquetes_asignados_und"],
            False,
            m["accesos"]["potencia_hp_volquete"],
            False,
            "Calculado",
        ),
        (
            "Accesos",
            "Motoniveladora",
            1,
            False,
            m["accesos"]["potencia_hp_motoniveladora"],
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
        "taladros_frente": sec["taladros"],
        "longitud_tunel_m": sec["longitud_m"],
        "v_esponjado_disparo_m3": vs,
        "v_total_esponjado_m3": sec["v_total_esponjado_m3"],
        "v_esponjado_dia_m3": sec["v_esponjado_dia_m3"],
        "t_perforacion_h": t_perforacion_h,
        "prod_cargador_m3_h": prod_cargador,
        "n_cargador": n_cargador,
        "distancia_m": distancia,
        "ciclo_volquete_min": ciclo_volquete,
        "viajes": viajes,
        "viajes_por_volquete": viajes_por_volquete,
        "n_volquete": n_volquete,
        "area_botadero_m2": area_bot,
        "lado_botadero_m": math.sqrt(area_bot),
        "n_tractor": n_tractor,
        "equipos": equipos,
        "hp_tunel_frente": hp_tunel_frente,
        "fichas": FICHAS_TECNICAS,
    }
