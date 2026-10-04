"""09 · Electricidad: ventilación, cargas, demanda y grupo electrógeno."""

from ..modelo import Hoja, Libro, Tabla, tabla_parametros

CLAVE = "electricidad"
GRUPOS_KVA = [100, 150, 200, 250, 300, 400, 500, 625, 750, 1000, 1250, 1500, 2000, 2500]


def caudal_por_persona(altitud: float) -> float:
    """m³/min por persona según altitud (DS 024-2016-EM)."""
    if altitud <= 1500:
        return 3.0
    if altitud <= 3000:
        return 4.0
    if altitud <= 4000:
        return 5.0
    return 6.0


def grupo_comercial(kva: float) -> int:
    """Primer tamaño comercial de grupo electrógeno ≥ kva."""
    return next((g for g in GRUPOS_KVA if g >= kva), GRUPOS_KVA[-1])


def calcular(p: dict, ctx: dict) -> dict:
    v, e = p["ventilacion"], p["electricidad"]
    frentes = p["perforacion"]["frentes"]

    # Ventilación (por frente)
    q_persona = caudal_por_persona(p["proyecto"]["altitud_msnm"])
    personas = ctx["personal"]["frente_por_guardia"]
    q_personas = personas * q_persona
    q_equipos = (
        ctx["maquinaria"]["hp_tunel_frente"]
        * v["caudal_por_hp_m3_min"]
        * v["simultaneidad_equipos"]
    )
    q_total = (q_personas + q_equipos) * v["factor_fugas"]
    velocidad = q_total / ctx["seccion"]["area_m2"]
    p_vent = q_total / 60 * v["presion_total_pa"] / v["eficiencia_ventilador"] / 1000

    # Cargas
    cargas = [
        ("Frente", "Ventilador principal", 1, True, p_vent, 24.0, 1.0),
        (
            "Campamento",
            "Bomba del pozo",
            1,
            False,
            ctx["agua"]["p_bomba_kw"],
            p["pozo"]["horas_bombeo"],
            1.0,
        ),
    ] + [
        (
            c["zona"],
            c["equipo"],
            c["cantidad"],
            c.get("por_frente", False),
            c["potencia_kw"],
            c["horas_dia"],
            c["factor_demanda"],
        )
        for c in e["cargas"]
    ]
    filas = []
    for zona, equipo, cant, por_frente, kw, horas, fd in cargas:
        n = cant * frentes if por_frente else cant
        demanda = n * kw * fd
        filas.append(
            {
                "zona": zona,
                "equipo": equipo,
                "cantidad": n,
                "kw": kw,
                "fd": fd,
                "demanda_kw": demanda,
                "horas": horas,
                "kwh_dia": demanda * horas,
            }
        )
    demanda = sum(f["demanda_kw"] for f in filas)
    energia = sum(f["kwh_dia"] for f in filas)
    kva = demanda / e["factor_potencia"] * (1 + e["reserva"])
    return {
        "q_persona": q_persona,
        "personas": personas,
        "q_personas": q_personas,
        "q_equipos": q_equipos,
        "q_total": q_total,
        "velocidad": velocidad,
        "cumple_velocidad": v["velocidad_min_m_min"]
        <= velocidad
        <= v["velocidad_max_m_min"],
        "p_ventilador_kw": p_vent,
        "cargas": filas,
        "demanda_kw": demanda,
        "energia_kwh_dia": energia,
        "kva_requerido": kva,
        "grupo_kva": grupo_comercial(kva),
        "combustible_l_dia": energia * e["consumo_combustible_l_kwh"],
    }


def libro(r: dict, p: dict) -> Libro:
    v, e = p["ventilacion"], p["electricidad"]
    ventilacion = tabla_parametros(
        [
            ("Altitud", "z", p["proyecto"]["altitud_msnm"], "msnm", "Dato"),
            (
                "Caudal por persona",
                "qp",
                r["q_persona"],
                "m³/min",
                "DS 024-2016-EM según altitud",
            ),
            (
                "Personas en el frente (por guardia)",
                "n",
                r["personas"],
                "und",
                "04_Personal",
            ),
            ("Caudal por personas", "Q1", r["q_personas"], "m³/min", "n · qp"),
            (
                "Caudal por equipos diésel",
                "Q2",
                r["q_equipos"],
                "m³/min",
                "HP en túnel · 3 · simultaneidad",
            ),
            ("Caudal requerido", "Qr", r["q_total"], "m³/min", "(Q1 + Q2) · f fugas"),
            ("Velocidad del aire", "v", r["velocidad"], "m/min", "Qr / A"),
            (
                "¿Velocidad dentro de límites?",
                "",
                r["cumple_velocidad"],
                "",
                f"{v['velocidad_min_m_min']:.0f} ≤ v ≤ {v['velocidad_max_m_min']:.0f}",
            ),
            (
                "Potencia del ventilador",
                "Pv",
                r["p_ventilador_kw"],
                "kW",
                "Qr/60 · ΔP / η / 1000",
            ),
        ],
        "Por frente",
    )
    cargas = Tabla(
        [
            "Zona",
            "Equipo / carga",
            "Cantidad",
            "Potencia unit. (kW)",
            "F. demanda",
            "Demanda (kW)",
            "Horas/día",
            "Energía (kWh/día)",
        ],
        [
            [
                c["zona"],
                c["equipo"],
                c["cantidad"],
                c["kw"],
                c["fd"],
                c["demanda_kw"],
                c["horas"],
                c["kwh_dia"],
            ]
            for c in r["cargas"]
        ],
        "Demanda = cantidad · potencia · f. demanda · Energía = demanda · horas",
    )
    resumen = tabla_parametros(
        [
            ("Máxima demanda", "MD", r["demanda_kw"], "kW", "Σ demandas"),
            (
                "Consumo de energía diario",
                "E",
                r["energia_kwh_dia"],
                "kWh/día",
                "Σ energías",
            ),
            (
                "Consumo de energía mensual",
                "Em",
                r["energia_kwh_dia"] * 30,
                "kWh/mes",
                "E · 30",
            ),
            (
                "Potencia aparente requerida",
                "S",
                r["kva_requerido"],
                "kVA",
                f"MD / {e['factor_potencia']} · (1 + {e['reserva']})",
            ),
            (
                "Grupo electrógeno comercial",
                "G",
                r["grupo_kva"],
                "kVA",
                "Tamaño comercial ≥ S",
            ),
            (
                "Consumo de combustible",
                "Cc",
                r["combustible_l_dia"],
                "L/día",
                "E · consumo específico",
            ),
        ]
    )
    return Libro(
        "09_Electricidad.xlsx",
        [
            Hoja("Ventilacion", "Ventilación del túnel", [ventilacion]),
            Hoja("Cargas", "Cuadro de cargas", [cargas]),
            Hoja("Resumen", "Consumo eléctrico y grupo electrógeno", [resumen]),
        ],
    )
