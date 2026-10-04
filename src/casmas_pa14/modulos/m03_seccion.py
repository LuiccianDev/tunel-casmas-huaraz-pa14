"""03 · Sección del túnel: geometría, gálibo, verificación MTC, perforación y volúmenes."""

import math

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "seccion"

MANUAL_TUNELES = "MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14)"
DG_2018 = "MTC Manual de Diseño Geométrico DG-2018, Sec. 304"
COLUMNAS_NORMA = ["Elemento", "Proyecto", "Mínimo", "Unidad", "Cumple", "Fuente"]


def area_herradura(ancho: float, altura: float) -> float:
    """Área de sección herradura: rectángulo B·hw + semicírculo π·B²/8."""
    hastial = altura - ancho / 2
    if hastial < 0:
        raise ValueError("En sección herradura la altura debe ser ≥ ancho / 2.")
    return ancho * hastial + math.pi * ancho**2 / 8


def altura_libre(radio: float, hastial_rasante: float, x: float) -> float:
    """Altura libre sobre la rasante a la distancia x del eje (bajo la bóveda)."""
    if x >= radio:
        return 0.0
    return hastial_rasante + math.sqrt(radio**2 - x**2)


def _geometria(s: dict) -> dict:
    """Dimensiones de excavación a partir de B, H y la altura sobre rasante."""
    b, h = s["ancho_m"], s["altura_m"]
    radio = b / 2
    hastial = h - radio
    espesor = h - s["altura_sobre_rasante_m"]
    area = area_herradura(b, h)
    return {
        "ancho_m": b,
        "altura_m": h,
        "altura_rasante_m": s["altura_sobre_rasante_m"],
        "espesor_rasante_m": espesor,
        "radio_m": radio,
        "hastial_m": hastial,
        "hastial_rasante_m": hastial - espesor,
        "area_m2": area,
        "perimetro_m": b + 2 * hastial + math.pi * b / 2,
        "area_util_m2": area - b * espesor,
    }


def _galibo(g: dict, geo: dict) -> dict:
    """Rectángulo de gálibo, plataforma y alturas libres bajo la bóveda."""
    ancho = g["carriles"] * g["ancho_carril_m"] + 2 * g["berma_m"] + g["separador_m"]
    plataforma = ancho + 2 * g["vereda_m"]
    if abs(plataforma - geo["ancho_m"]) > g["tolerancia_m"]:
        raise ValueError(
            f"Gálibo + veredas = {plataforma:.2f} m ≠ ancho B = {geo['ancho_m']:.2f} m"
        )
    h_borde = altura_libre(geo["radio_m"], geo["hastial_rasante_m"], ancho / 2)
    return {
        "carriles": g["carriles"],
        "ancho_carril_m": g["ancho_carril_m"],
        "berma_m": g["berma_m"],
        "separador_m": g["separador_m"],
        "vereda_m": g["vereda_m"],
        "ancho_galibo_m": ancho,
        "ancho_plataforma_m": plataforma,
        "altura_galibo_m": g["altura_m"],
        "area_galibo_m2": ancho * g["altura_m"],
        "altura_borde_galibo_m": h_borde,
        "holgura_galibo_m": h_borde - g["altura_m"],
        "altura_vereda_m": geo["hastial_rasante_m"],
    }


def _verificacion(g: dict, n: dict, geo: dict, gal: dict) -> list[list]:
    """Filas Elemento | Proyecto | Mínimo | Unidad | Cumple | Fuente."""
    tol = g["tolerancia_m"]
    filas = [
        ("Ancho de carril", g["ancho_carril_m"], n["ancho_carril_m"], DG_2018),
        ("Berma (cada lado)", g["berma_m"], n["berma_m"], DG_2018 + " (S)"),
        ("Vereda (cada lado)", g["vereda_m"], n["vereda_m"], MANUAL_TUNELES),
        ("Gálibo vertical", g["altura_m"], n["galibo_vertical_m"], MANUAL_TUNELES),
        (
            "Altura libre en borde del gálibo (bóveda)",
            gal["altura_borde_galibo_m"],
            g["altura_m"],
            f"Geometría: hw' + √(R² − (Wg/2)²), tolerancia {tol} m",
        ),
        (
            "Altura libre sobre vereda (junto al hastial)",
            gal["altura_vereda_m"],
            n["altura_vereda_m"],
            MANUAL_TUNELES + " (S)",
        ),
        (
            "Gálibo + 2 veredas = ancho B",
            gal["ancho_plataforma_m"],
            geo["ancho_m"],
            "Geometría del plano CAD",
        ),
    ]
    return [
        [nombre, proy, mini, "m", "Sí" if proy >= mini - tol else "No", fuente]
        for nombre, proy, mini, fuente in filas
    ]


def calcular(p: dict, ctx: dict) -> dict:
    s, f = p["seccion"], p["perforacion"]
    geo = _geometria(s)
    gal = _galibo(s["galibo"], geo)
    area, perimetro = geo["area_m2"], geo["perimetro_m"]
    taladros = math.ceil(
        perimetro / f["espaciamiento_periferico_m"] + f["coeficiente_roca_k"] * area
    )
    avance = f["longitud_barreno_m"] * f["eficiencia_avance"]
    v_disparo = area * avance
    v_excavado = v_disparo * (1 + s["sobreexcavacion"])
    avance_dia = avance * f["disparos_por_dia_frente"] * f["frentes"]
    longitud = ctx["ubicacion"]["longitud_m"]
    v_total = area * (1 + s["sobreexcavacion"]) * longitud
    return {
        **geo,
        **gal,
        "verificacion": _verificacion(s["galibo"], s["norma"], geo, gal),
        "requiere_emergencia": longitud > s["norma"]["longitud_emergencia_m"],
        "taladros": taladros,
        "avance_disparo_m": avance,
        "v_disparo_m3": v_disparo,
        "v_excavado_disparo_m3": v_excavado,
        "v_esponjado_disparo_m3": v_excavado * s["factor_esponjamiento"],
        "t_disparo": v_excavado * s["densidad_roca_t_m3"],
        "avance_dia_m": avance_dia,
        "avance_mes_m": avance_dia * f["dias_trabajo_mes"],
        "dias_excavacion": math.ceil(longitud / avance_dia),
        "longitud_m": longitud,
        "v_total_m3": v_total,
        "v_total_esponjado_m3": v_total * s["factor_esponjamiento"],
        "v_esponjado_dia_m3": v_excavado
        * s["factor_esponjamiento"]
        * f["disparos_por_dia_frente"]
        * f["frentes"],
    }


# ---------------------------------------------------------------- tablas
def _tabla_geometria(r: dict, s: dict) -> Tabla:
    return tabla_parametros(
        [
            ("Tipo de sección", "", s["tipo"], "", "Plano CAD"),
            ("Ancho de excavación", "B", r["ancho_m"], "m", "Plano CAD"),
            ("Altura total (fondo → clave)", "H", r["altura_m"], "m", "Plano CAD"),
            ("Altura sobre rasante", "Hr", r["altura_rasante_m"], "m", "Plano CAD"),
            ("Espesor bajo rasante", "e", r["espesor_rasante_m"], "m", "H − Hr"),
            ("Radio de bóveda", "R", r["radio_m"], "m", "B / 2"),
            ("Hastial desde el fondo", "hw", r["hastial_m"], "m", "H − R"),
            ("Hastial sobre rasante", "hw'", r["hastial_rasante_m"], "m", "hw − e"),
            ("Área de excavación", "A", r["area_m2"], "m²", "B·hw + π·B²/8"),
            ("Perímetro de excavación", "P", r["perimetro_m"], "m", "B + 2·hw + π·B/2"),
            ("Área libre sobre rasante", "Au", r["area_util_m2"], "m²", "A − B·e"),
        ]
    )


def _tabla_galibo(r: dict, g: dict) -> Tabla:
    return tabla_parametros(
        [
            ("Número de carriles", "n", g["carriles"], "und", "Plano CAD"),
            ("Ancho de carril", "c", g["ancho_carril_m"], "m", "Plano CAD"),
            ("Berma (cada lado)", "b", g["berma_m"], "m", "Plano CAD"),
            ("Separador central", "s", g["separador_m"], "m", "Plano CAD"),
            ("Ancho del gálibo", "Wg", r["ancho_galibo_m"], "m", "n·c + 2·b + s"),
            ("Altura del gálibo", "Hg", r["altura_galibo_m"], "m", "Plano CAD"),
            ("Área del gálibo", "Ag", r["area_galibo_m2"], "m²", "Wg · Hg"),
            ("Vereda (cada lado)", "v", g["vereda_m"], "m", "Plano CAD"),
            ("Ancho de plataforma", "Wp", r["ancho_plataforma_m"], "m", "Wg + 2·v"),
            (
                "Altura libre en borde del gálibo",
                "hb",
                r["altura_borde_galibo_m"],
                "m",
                "hw' + √(R² − (Wg/2)²)",
            ),
            ("Holgura gálibo – bóveda", "Δ", r["holgura_galibo_m"], "m", "hb − Hg"),
            ("Ancho de cuneta", "ac", g["cuneta_ancho_m"], "m", "Plano CAD"),
            ("Profundidad de cuneta", "pc", g["cuneta_prof_m"], "m", "Plano CAD"),
            ("Bombeo transversal", "i", g["bombeo_pct"], "%", "Plano CAD"),
        ]
    )


def _tabla_norma(r: dict) -> Tabla:
    return Tabla(COLUMNAS_NORMA, r["verificacion"])


def libro(r: dict, p: dict) -> Libro:
    s, f = p["seccion"], p["perforacion"]
    perforacion = tabla_parametros(
        [
            ("Frentes de ataque", "nf", f["frentes"], "und", "Dato"),
            (
                "Disparos por día y frente",
                "nd",
                f["disparos_por_dia_frente"],
                "und",
                "Dato",
            ),
            ("Longitud de barreno", "Lb", f["longitud_barreno_m"], "m", "Dato"),
            ("Eficiencia de avance", "η", f["eficiencia_avance"], "", "Dato"),
            ("Área de excavación", "A", r["area_m2"], "m²", "Hoja Geometria"),
            ("Perímetro de excavación", "P", r["perimetro_m"], "m", "Hoja Geometria"),
            (
                "Número de taladros",
                "N",
                r["taladros"],
                "und",
                "P/E + K·A (E, K: datos)",
            ),
            ("Avance por disparo", "a", r["avance_disparo_m"], "m", "Lb · η"),
            ("Avance diario (total)", "ad", r["avance_dia_m"], "m/día", "a · nd · nf"),
            (
                "Avance mensual (total)",
                "am",
                r["avance_mes_m"],
                "m/mes",
                "ad · días/mes",
            ),
            ("Duración de excavación", "Te", r["dias_excavacion"], "días", "⌈L / ad⌉"),
        ]
    )
    volumenes = tabla_parametros(
        [
            ("Volumen teórico por disparo", "Vd", r["v_disparo_m3"], "m³", "A · a"),
            (
                "Volumen excavado por disparo",
                "Ve",
                r["v_excavado_disparo_m3"],
                "m³",
                "Vd · (1 + sobreexcavación)",
            ),
            (
                "Volumen esponjado por disparo",
                "Vs",
                r["v_esponjado_disparo_m3"],
                "m³",
                "Ve · fe",
            ),
            ("Tonelaje por disparo", "T", r["t_disparo"], "t", "Ve · ρ"),
            ("Longitud del túnel", "L", r["longitud_m"], "m", "01_Ubicacion"),
            (
                "Volumen total excavado",
                "VT",
                r["v_total_m3"],
                "m³",
                "A · (1 + sobreexcavación) · L",
            ),
            (
                "Volumen total esponjado (a botadero)",
                "VTs",
                r["v_total_esponjado_m3"],
                "m³",
                "VT · fe",
            ),
        ]
    )
    return Libro(
        "03_Seccion.xlsx",
        [
            Hoja("Geometria", "Geometría de excavación", [_tabla_geometria(r, s)]),
            Hoja("Galibo", "Gálibo y plataforma", [_tabla_galibo(r, s["galibo"])]),
            Hoja("Justificacion MTC", "Verificación normativa", [_tabla_norma(r)]),
            Hoja("Perforacion y avance", "Perforación y avance", [perforacion]),
            Hoja("Volumenes", "Volúmenes de excavación", [volumenes]),
        ],
    )


# ---------------------------------------------------------------- memoria
def memoria(r: dict, p: dict) -> Memoria:
    """Memoria de cálculo y justificación normativa de la sección (Markdown)."""
    s = p["seccion"]
    g, n = s["galibo"], s["norma"]
    incumple = [f[0] for f in r["verificacion"] if f[4] == "No"]
    estado = (
        "Todas las comprobaciones **cumplen**."
        if not incumple
        else "**No cumplen:** " + ", ".join(incumple) + "."
    )
    justificacion = [
        f"- **Carriles de {g['ancho_carril_m']:.2f} m**: igual al mínimo de "
        f"{n['ancho_carril_m']:.2f} m de la DG-2018 para carreteras de 1.ª clase, "
        "lo que permite el paso de vehículos pesados de obra y de servicio.",
        f"- **Bermas de {g['berma_m']:.2f} m**: superan la referencia de "
        f"{n['berma_m']:.2f} m (S); dan espacio lateral de seguridad y para "
        "vehículos detenidos.",
        f"- **Veredas de {g['vereda_m']:.2f} m** a cada lado: cumplen el mínimo del "
        "Manual de Túneles para mantenimiento y auxilio, aunque no circulen peatones.",
        f"- **Gálibo de {r['ancho_galibo_m']:.2f} × {g['altura_m']:.2f} m**: la altura "
        f"cumple el gálibo vertical mínimo de {n['galibo_vertical_m']:.2f} m. En sus "
        f"esquinas superiores la bóveda pasa a {r['altura_borde_galibo_m']:.3f} m "
        f"sobre la rasante (holgura {r['holgura_galibo_m']:+.3f} m, dentro de la "
        f"tolerancia de {g['tolerancia_m']} m del plano): el gálibo queda inscrito "
        "en el arco.",
        f"- **Bóveda semicircular de R = {r['radio_m']:.2f} m** sobre hastiales: "
        "forma que trabaja a compresión y se excava con perforación y voladura. "
        f"El ancho B = Wg + 2·v = {r['ancho_plataforma_m']:.2f} m aloja gálibo y "
        "veredas.",
        f"- **Espesor bajo rasante de {r['espesor_rasante_m']:.2f} m**: aloja el "
        f"pavimento, la subbase y el drenaje (cunetas de {g['cuneta_ancho_m']:.2f} × "
        f"{g['cuneta_prof_m']:.2f} m y bombeo de {g['bombeo_pct']:.1f} %).",
    ]
    observaciones = [
        "- Los valores marcados **(S)** no están confirmados con el texto oficial; "
        "verificarlos en el manual correspondiente.",
        "- El sostenimiento y el revestimiento dependen de la geología (02_Geologia, "
        "pendiente) y pueden cambiar la sección de excavación.",
    ]
    if r["requiere_emergencia"]:
        observaciones.insert(
            0,
            f"- Longitud L = {r['longitud_m']:.1f} m > "
            f"{n['longitud_emergencia_m']} m: prever **zonas de emergencia / "
            "apartaderos** (Manual de Túneles) (S).",
        )
    return Memoria(
        "03_Seccion.md",
        "03 · Sección del túnel — Memoria de cálculo y justificación normativa",
        [
            (
                "1. Objetivo",
                [
                    "Definir y justificar la sección transversal del túnel según la "
                    "normativa peruana del MTC, a partir del plano CAD del proyecto "
                    f"({r['altura_m']:.2f} m × {r['ancho_m']:.2f} m)."
                ],
            ),
            (
                "2. Normativa aplicada",
                [
                    f"- {MANUAL_TUNELES}: gálibo vertical, veredas, zonas de "
                    "emergencia.\n"
                    f"- {DG_2018}: ancho de carril y bermas.\n"
                    "- Valores normativos en `datos/parametros.toml` → "
                    "`[seccion.norma]`."
                ],
            ),
            ("3. Geometría de excavación", [_tabla_geometria(r, s)]),
            ("4. Gálibo y plataforma", [_tabla_galibo(r, g)]),
            ("5. Verificación normativa", [_tabla_norma(r), estado]),
            ("6. Justificación de las dimensiones", ["\n".join(justificacion)]),
            ("7. Observaciones", ["\n".join(observaciones)]),
        ],
    )
