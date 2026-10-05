"""06 · Maquinaria: frente del túnel, botadero, campamento y fichas técnicas."""

import math

from ..fichas_maquinaria import FICHAS_TECNICAS
from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

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

    # Accesos

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
            173,
            False,
            "Calculado",
        ),
        (
            "Banquetas",
            "Excavadora Hidráulica",
            n_exc_banq,
            False,
            314,
            False,
            "Calculado",
        ),
        (
            "Banquetas",
            "Camión Volquete Rígido",
            n_volq_banq,
            False,
            500,
            False,
            "Calculado",
        ),
        ("Accesos", "Tractor de Orugas Pesado (D8)", 1, False, 354, False, "Calculado"),
        (
            "Accesos",
            "Tractor de Orugas Mediano (D6)",
            1,
            False,
            215,
            False,
            "Calculado",
        ),
        ("Accesos", "Excavadora Hidráulica", 1, False, 314, False, "Calculado"),
        ("Accesos", "Camión Volquete Rígido", 2, False, 500, False, "Calculado"),
        ("Accesos", "Motoniveladora", 1, False, 150, False, "Calculado"),
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


def _tabla_ficha_individual(f: dict) -> Tabla:
    """Genera la tabla estándar de especificaciones técnicas para la hoja individual."""
    filas = [
        ("Equipo asignado", "Eq", f["equipo"], "", "Catálogo de obra"),
        ("Marca y modelo", "Mod", f["marca_modelo"], "", "Ficha técnica fabricante"),
        ("Zona operativa", "Zona", f["zona"], "", "Asignación en proyecto"),
        ("Proceso u operación", "Proc", f["proceso"], "", "Plan de ciclo minero"),
        (
            "Potencia motriz nominal",
            "P",
            f["potencia_hp"],
            "HP",
            f"{f['potencia_kw']} kW",
        ),
        ("Fuente de energía", "Tipo", f["tipo_energia"], "", "Especificación motriz"),
        (
            "Consumo de combustible",
            "Cons. D",
            f["consumo_combustible"],
            "",
            "Régimen nominal de trabajo",
        ),
        (
            "Consumo eléctrico",
            "Cons. E",
            f["consumo_electrico_kwh"],
            "",
            "Operación de carga/bombeo",
        ),
        (
            "Dimensiones (Largo × Ancho × Alto)",
            "Dim",
            f["dimensiones_m"],
            "m",
            "Gálibo del equipo",
        ),
        ("Longitud total", "L", f["largo_m"], "m", "Ficha técnica"),
        ("Ancho de vía / total", "An", f["ancho_m"], "m", "Ficha técnica"),
        ("Altura de tránsito", "Al", f["alto_m"], "m", "Ficha técnica"),
        ("Peso operativo", "W", f["peso_operativo_t"], "t", "Peso en servicio"),
        (
            "Capacidad de trabajo / tolva / balde",
            "Cap",
            f["capacidad_operativa"],
            "",
            "Rendimiento",
        ),
        (
            "Dotación de personal asignado",
            "Pax",
            f["dotacion_personal"],
            "",
            "04_Personal",
        ),
        (
            "Operación en interior túnel",
            "Tún",
            "Sí" if f["en_tunel"] else "No",
            "",
            "Requiere ventilación",
        ),
        (
            "Enlace de visualización (Drive/Web)",
            "Link",
            f["link_ficha"],
            "",
            "Ficha del fabricante",
        ),
        (
            "Enlace de descarga directa",
            "Desc",
            f["link_descarga"],
            "",
            "Servidor de archivos",
        ),
        ("Descripción funcional", "Desc.", f["descripcion"], "", "Memoria técnica"),
    ]
    return tabla_parametros(filas, f"Ficha Técnica Detallada — {f['marca_modelo']}")


def _tabla_resumen_fichas(fichas: list[dict]) -> Tabla:
    """Tabla resumen consolidada con todas las maquinarias y especificaciones clave."""
    columnas = [
        "Zona",
        "Proceso / Tarea",
        "Tipo de Equipo",
        "Marca y Modelo",
        "Potencia (HP)",
        "Potencia (kW)",
        "Dimensiones (m)",
        "Peso (t)",
        "Capacidad / Rendimiento",
        "Consumo",
        "Dotación",
        "Túnel",
        "Ficha Técnica (Link)",
    ]
    filas = []
    for f in fichas:
        filas.append(
            [
                f["zona"],
                f["proceso"],
                f["equipo"],
                f["marca_modelo"],
                f["potencia_hp"],
                f["potencia_kw"],
                f["dimensiones_m"],
                f["peso_operativo_t"],
                f["capacidad_operativa"],
                f["consumo_combustible"]
                if f["consumo_combustible"] != "N/A"
                else f["consumo_electrico_kwh"],
                f["dotacion_personal"],
                "Sí" if f["en_tunel"] else "No",
                f["link_ficha"],
            ]
        )
    return Tabla(
        columnas, filas, "Resumen Consolidado de Fichas Técnicas de Maquinaria"
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
                "Productividad del cargador frontal",
                "Qs",
                r["prod_cargador_m3_h"],
                "m³/h",
                "C · fll · 60 / ciclo",
            ),
            ("Cargadores por frente", "nc", r["n_cargador"], "und", "⌈Vs / (Qs · tv)⌉"),
            (
                "Distancia de acarreo crítica",
                "D",
                r["distancia_m"],
                "m",
                "L / nf + distancia a botadero",
            ),
            (
                "Ciclo del volquete",
                "tvq",
                r["ciclo_volquete_min"],
                "min",
                "D/vc + D/vv + t fijo",
            ),
            ("Viajes por disparo", "nv", r["viajes"], "und", "⌈Vs / (C · fll)⌉"),
            (
                "Viajes por volquete en la ventana",
                "vvq",
                r["viajes_por_volquete"],
                "und",
                "tv / td",
            ),
            ("Volquetes por frente", "nvq", r["n_volquete"], "und", "⌈nv / vd⌉"),
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

    # 1. Hojas base
    hojas = [
        Hoja(
            "Frente",
            "Maquinaria del frente del túnel",
            [frente, _tabla_equipos(r, "Frente")],
        ),
        Hoja(
            "Accesos",
            "Maquinaria para construcción y mantenimiento de accesos",
            [_tabla_equipos(r, "Accesos")],
        ),
        Hoja(
            "Banquetas",
            "Maquinaria para excavación de portales y banquetas",
            [_tabla_equipos(r, "Banquetas")],
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
    ]

    # 2. Hojas individuales por cada maquinaria
    fichas = r.get("fichas", FICHAS_TECNICAS)
    for ficha in fichas:
        nombre_hoja = ficha["hoja"][:31]
        hojas.append(
            Hoja(
                nombre_hoja,
                f"Ficha Técnica: {ficha['marca_modelo']} ({ficha['equipo']})",
                [_tabla_ficha_individual(ficha)],
            )
        )

    # 3. Hoja final: Resumen consolidado de todas las fichas
    hojas.append(
        Hoja(
            "Resumen_Flota",
            "Consolidado General de Flota y Fichas Técnicas",
            [_tabla_resumen_fichas(fichas)],
        )
    )

    return Libro("06_Maquinaria.xlsx", hojas)


def memoria(r: dict, p: dict) -> Memoria:
    """Genera la memoria técnica de dimensionamiento y selección de maquinaria en Markdown."""
    fichas = r.get("fichas", FICHAS_TECNICAS)
    secciones = [
        (
            "1. Criterios de Selección y Dimensionamiento de Flota",
            [
                "La selección de la flota de maquinaria pesada responde a los requerimientos "
                f"de excavación mecanizada a sección completa ({p['seccion']['ancho_m']:.2f} m × "
                f"{p['seccion']['altura_m']:.2f} m) y a la necesidad de evacuar el material "
                "con camiones volquetes convencionales de alta potencia y capacidad.",
                "Se garantiza la compatibilidad de gálibos entre los equipos seleccionados y la sección "
                "del túnel, así como el cumplimiento normativo D.S. 024-2016-EM en cuanto a ventilación "
                "por potencia diésel en interior mina.",
            ],
        ),
        (
            "2. Ciclos Operativos de Perforación, Carguío y Evacuación",
            [
                f"- **Tiempo de perforación de barreno:** {r['t_perforacion_h']:.2f} h por disparo.",
                f"- **Productividad del cargador en frente:** {r['prod_cargador_m3_h']:.2f} m³/h.",
                f"- **Ciclo de acarreo a botadero:** {r['ciclo_volquete_min']:.2f} min por viaje.",
                f"- **Área requerida de botadero:** {r['area_botadero_m2']:,.0f} m².",
            ],
        ),
        (
            "3. Tabla Consolidada de Fichas Técnicas de Maquinaria",
            [_tabla_resumen_fichas(fichas)],
        ),
    ]
    return Memoria(
        "06_Maquinaria.md",
        "Memoria Técnica: Gestión y Asignación de Flota de Maquinaria",
        secciones,
    )
