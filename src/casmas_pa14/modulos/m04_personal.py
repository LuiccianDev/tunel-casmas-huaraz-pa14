"""04 · Personal: relación de cargos, organigrama y población del campamento."""

import math

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "personal"


def calcular(p: dict, ctx: dict) -> dict:
    frentes = p.get("perforacion", {}).get("frentes", 2)
    filas = []
    for x in p["personal"]:
        macro_area = x.get("macro_area", "Personal de Servicio")
        sub_area = x.get("sub_area", x.get("area", "General"))
        cargo = x["cargo"]
        categoria = x["categoria"]
        tipo_labor = x.get("tipo_labor", "indirecta").capitalize()
        campamento = x.get("campamento", "CAMP1")
        turno = x.get("turno", "Dia")
        if "cantidad" in x:
            cantidad = x["cantidad"]
        else:
            mult = frentes if x.get("por_frente", False) else 1
            cantidad = x.get("por_guardia", 1) * x.get("guardias", 1) * mult

        filas.append(
            {
                "macro_area": macro_area,
                "sub_area": sub_area,
                "area": sub_area,  # compatibilidad
                "cargo": cargo,
                "categoria": categoria,
                "tipo_labor": tipo_labor,
                "campamento": campamento,
                "turno": turno,
                "cantidad": cantidad,
                "total": cantidad,  # compatibilidad
            }
        )

    total = sum(x["cantidad"] for x in filas)
    staff = sum(x["cantidad"] for x in filas if x["categoria"] == "staff")
    obreros = total - staff
    directa = sum(x["cantidad"] for x in filas if x["tipo_labor"].lower() == "directa")
    indirecta = sum(
        x["cantidad"] for x in filas if x["tipo_labor"].lower() == "indirecta"
    )

    por_macro_area: dict[str, int] = {}
    for m in [
        "Personal de Campamento",
        "Personal de Frente",
        "Personal de Servicio",
    ]:
        por_macro_area[m] = sum(x["cantidad"] for x in filas if x["macro_area"] == m)

    por_area: dict[str, int] = {}
    for x in filas:
        por_area[x["sub_area"]] = por_area.get(x["sub_area"], 0) + x["cantidad"]

    camp1_total = sum(x["cantidad"] for x in filas if x["campamento"] == "CAMP1")
    camp2_total = sum(x["cantidad"] for x in filas if x["campamento"] == "CAMP2")
    dia_total = sum(x["cantidad"] for x in filas if x["turno"] == "Dia")
    noche_total = sum(x["cantidad"] for x in filas if x["turno"] == "Noche")

    camp1_dia = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP1" and x["turno"] == "Dia"
    )
    camp1_noche = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP1" and x["turno"] == "Noche"
    )
    camp2_dia = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP2" and x["turno"] == "Dia"
    )
    camp2_noche = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP2" and x["turno"] == "Noche"
    )

    frente_por_guardia = sum(
        x["cantidad"]
        for x in filas
        if x["macro_area"] == "Personal de Frente"
        and x["campamento"] == "CAMP1"
        and x["turno"] == "Dia"
    )

    reg = p["regimen"]
    factor = (reg["dias_trabajo"] + reg["dias_descanso"]) / reg["dias_trabajo"]
    planilla = math.ceil(total * factor)

    # Verificaciones de consistencia y balance
    assert total == camp1_total + camp2_total, "Descuadre en suma de campamentos"
    assert total == dia_total + noche_total, "Descuadre en suma de turnos"

    return {
        "filas": filas,
        "por_macro_area": por_macro_area,
        "por_area": por_area,
        "total": total,
        "staff": staff,
        "obreros": obreros,
        "directa": directa,
        "indirecta": indirecta,
        "camp1_total": camp1_total,
        "camp2_total": camp2_total,
        "dia_total": dia_total,
        "noche_total": noche_total,
        "camp1_dia": camp1_dia,
        "camp1_noche": camp1_noche,
        "camp2_dia": camp2_dia,
        "camp2_noche": camp2_noche,
        "frente_por_guardia": frente_por_guardia,
        "factor_regimen": factor,
        "planilla": planilla,
    }


def _tabla_macro_areas(r: dict) -> Tabla:
    filas = []
    macros = [
        ("1. Personal de Campamento", "Personal de Campamento"),
        ("2. Personal de Frente (Túnel + Botaderos)", "Personal de Frente"),
        ("3. Personal de Servicio y Soporte", "Personal de Servicio"),
    ]
    for etiqueta, clave in macros:
        c1 = sum(
            x["cantidad"]
            for x in r["filas"]
            if x["macro_area"] == clave and x["campamento"] == "CAMP1"
        )
        c2 = sum(
            x["cantidad"]
            for x in r["filas"]
            if x["macro_area"] == clave and x["campamento"] == "CAMP2"
        )
        dia = sum(
            x["cantidad"]
            for x in r["filas"]
            if x["macro_area"] == clave and x["turno"] == "Dia"
        )
        noche = sum(
            x["cantidad"]
            for x in r["filas"]
            if x["macro_area"] == clave and x["turno"] == "Noche"
        )
        tot = r["por_macro_area"][clave]
        pct = f"{(tot / r['total'] * 100):.1f} %"
        filas.append([etiqueta, c1, c2, dia, noche, tot, pct])

    filas.append(
        [
            "TOTAL PROYECTO",
            r["camp1_total"],
            r["camp2_total"],
            r["dia_total"],
            r["noche_total"],
            r["total"],
            "100.0 %",
        ]
    )
    return Tabla(
        [
            "Macro-Área del Proyecto",
            "CAMP1 (Portal A)",
            "CAMP2 (Portal B)",
            "Guardia Día (12h)",
            "Guardia Noche (12h)",
            "Total (pax)",
            "% del Total",
        ],
        filas,
        "Distribución Consolidada por Macro-Áreas",
    )


def _tabla_cruce_campamentos(r: dict) -> Tabla:
    filas = [
        [
            "Campamento 1 — Principal (Portal A)",
            r["camp1_dia"],
            r["camp1_noche"],
            r["camp1_total"],
        ],
        [
            "Campamento 2 — Satélite (Portal B)",
            r["camp2_dia"],
            r["camp2_noche"],
            r["camp2_total"],
        ],
        [
            "TOTAL GENERAL DEL PROYECTO",
            r["dia_total"],
            r["noche_total"],
            r["total"],
        ],
    ]
    return Tabla(
        [
            "Instalación Residencial",
            "Guardia Día (07:00 – 19:00 h)",
            "Guardia Noche (19:00 – 07:00 h)",
            "Total Trabajadores Asignados",
        ],
        filas,
        "Matriz de Cruce: Campamento × Turno de Guardia",
    )


def _tabla_mano_obra(r: dict) -> Tabla:
    staff_dir = sum(
        x["cantidad"]
        for x in r["filas"]
        if x["tipo_labor"] == "Directa" and x["categoria"] == "staff"
    )
    obr_dir = sum(
        x["cantidad"]
        for x in r["filas"]
        if x["tipo_labor"] == "Directa" and x["categoria"] == "obrero"
    )
    staff_ind = sum(
        x["cantidad"]
        for x in r["filas"]
        if x["tipo_labor"] == "Indirecta" and x["categoria"] == "staff"
    )
    obr_ind = sum(
        x["cantidad"]
        for x in r["filas"]
        if x["tipo_labor"] == "Indirecta" and x["categoria"] == "obrero"
    )

    filas = [
        [
            "Mano de Obra Directa (MOD)",
            staff_dir,
            obr_dir,
            r["directa"],
            f"{(r['directa'] / r['total'] * 100):.1f} %",
            "Excavación subterránea, perforación, voladura, sostenimiento y topografía",
        ],
        [
            "Mano de Obra Indirecta (MOI)",
            staff_ind,
            obr_ind,
            r["indirecta"],
            f"{(r['indirecta'] / r['total'] * 100):.1f} %",
            "Dirección, SSOMA, talleres, transporte, catering, logística y habitabilidad",
        ],
        [
            "TOTAL",
            r["staff"],
            r["obreros"],
            r["total"],
            "100.0 %",
            "Población activa total en campamentos",
        ],
    ]
    return Tabla(
        [
            "Clasificación Laboral",
            "Staff (pax)",
            "Obreros (pax)",
            "Total (pax)",
            "% del Total",
            "Alcance Operativo",
        ],
        filas,
        "Clasificación de Mano de Obra: Directa vs Indirecta",
    )


def libro(r: dict, p: dict) -> Libro:
    reg = p["regimen"]

    # Función auxiliar para crear la tabla de relación de personal filtrada
    def _crear_tabla_relacion(filas_filtradas: list, titulo: str) -> Tabla:
        return Tabla(
            [
                "Macro-Área",
                "Sub-Área",
                "Cargo",
                "Categoría",
                "Tipo Labor",
                "Campamento",
                "Turno",
                "Cantidad (pax)",
            ],
            [
                [
                    x["macro_area"],
                    x["sub_area"],
                    x["cargo"],
                    x["categoria"],
                    x["tipo_labor"],
                    x["campamento"],
                    x["turno"],
                    x["cantidad"],
                ]
                for x in filas_filtradas
            ],
            titulo,
        )

    # 1. Tabla Maestra (Todos)
    relacion_todas = _crear_tabla_relacion(
        r["filas"], "Relación nominal de todos los puestos del proyecto"
    )

    # 2. Tablas filtradas por Macro-Área
    filas_frente = [x for x in r["filas"] if x["macro_area"] == "Personal de Frente"]
    tabla_frente = _crear_tabla_relacion(
        filas_frente, "Área Operativa e Ingeniería (Frente del Túnel)"
    )

    filas_campamento = [
        x for x in r["filas"] if x["macro_area"] == "Personal de Campamento"
    ]
    tabla_campamento = _crear_tabla_relacion(
        filas_campamento, "Área Administrativa y Habitabilidad (Campamento)"
    )

    filas_servicio = [
        x for x in r["filas"] if x["macro_area"] == "Personal de Servicio"
    ]
    tabla_servicio = _crear_tabla_relacion(
        filas_servicio, "Área de Servicios y Soporte SSOMA/Mantenimiento"
    )

    resumen = tabla_parametros(
        [
            ("Población en campamento", "Pob", r["total"], "personas", "Σ Total"),
            (
                "Campamento 1 (Portal A)",
                "Pob_C1",
                r["camp1_total"],
                "personas",
                "Portal Entrada",
            ),
            (
                "Campamento 2 (Portal B)",
                "Pob_C2",
                r["camp2_total"],
                "personas",
                "Portal Salida",
            ),
            ("Guardia Día (12h)", "G_Dia", r["dia_total"], "personas", "07:00–19:00 h"),
            (
                "Guardia Noche (12h)",
                "G_Noc",
                r["noche_total"],
                "personas",
                "19:00–07:00 h",
            ),
            (
                "Mano de Obra Directa (MOD)",
                "MOD",
                r["directa"],
                "personas",
                "Frente y avances",
            ),
            (
                "Mano de Obra Indirecta (MOI)",
                "MOI",
                r["indirecta"],
                "personas",
                "Soporte y campamento",
            ),
            ("Staff", "Ps", r["staff"], "personas", "Σ categoría staff"),
            ("Obreros", "Po", r["obreros"], "personas", "Pob − Ps"),
            (
                "Personal de frente por guardia (1 frente)",
                "Pf",
                r["frente_por_guardia"],
                "personas",
                "Para ventilación",
            ),
            (
                "Régimen de trabajo",
                "",
                f"{reg['dias_trabajo']}x{reg['dias_descanso']}",
                "días",
                "D.S. 024-2016-EM Art. 201",
            ),
            (
                "Factor de relevo de régimen",
                "fr",
                r["factor_regimen"],
                "",
                "(t + d) / t",
            ),
            (
                "Personal total en planilla",
                "Pl",
                r["planilla"],
                "personas",
                "⌈Pob · (t + d) / t⌉",
            ),
        ],
        "Totales y Parámetros Consolidados",
    )

    return Libro(
        "04_Personal.xlsx",
        [
            Hoja(
                "Resumen",
                "Resumen de personal y cuadres",
                [
                    _tabla_macro_areas(r),
                    _tabla_mano_obra(r),
                    _tabla_cruce_campamentos(r),
                    resumen,
                ],
            ),
            Hoja(
                "Operativa_Frente",
                "Personal de Operaciones e Ingeniería Subterránea",
                [tabla_frente],
            ),
            Hoja(
                "Administracion_Campamento",
                "Personal Administrativo y Habitabilidad",
                [tabla_campamento],
            ),
            Hoja(
                "Servicios_Mantenimiento",
                "Personal de Servicios, Logística y Mantenimiento",
                [tabla_servicio],
            ),
            Hoja(
                "Relacion_Completa",
                "Relación nominal de todo el personal (Consolidado)",
                [relacion_todas],
            ),
        ],
    )


def memoria(r: dict, p: dict) -> Memoria:
    reg = p["regimen"]
    resumen_ejecutivo = [
        "El presente informe documenta el dimensionamiento definitivo, la justificación "
        "técnico-operativa y la estructura jerárquica del personal para la construcción "
        f"del **Túnel Casmas Huaraz PA14**, infraestructura subterránea bidireccional "
        f"ubicada a una altitud de {p['proyecto']['altitud_msnm']:.0f} m s.n.m.",
        "La excavación se realiza mediante el método convencional de perforación y "
        "voladura mecanizada (*Drill & Blast*), atacando simultáneamente e ininterrumpidamente "
        "desde dos frentes: **Frente 1 (Portal A - Entrada, 3,900 msnm)** y **Frente 2 "
        "(Portal B - Salida, 3,800 msnm)**.",
    ]

    justificacion_regimen = [
        f"### 2.1 Justificación del Régimen {reg['dias_trabajo']}×{reg['dias_descanso']} "
        f"({reg['dias_trabajo']} días de trabajo por {reg['dias_descanso']} de descanso)\n"
        "1. **Condición Fisiológica y Mal de Montaña (Hipoxia a gran altitud):**\n"
        f"   El proyecto se sitúa a {p['proyecto']['altitud_msnm']:.0f} m s.n.m. bajo "
        "condiciones climáticas frías y reducida presión de oxígeno. Jornadas estándar "
        "de 6×1 o 5×2 obligarían a constantes traslados por vías de montaña, generando "
        "fatiga severa. El régimen atípico acumulativo permite que el personal labore "
        "aclimatado y descienda una semana continua a valles de menor cota para su "
        "recuperación biológica y psicológica.\n"
        "2. **Sustento Legal y Constitucional Peruano:**\n"
        "   - **D.S. N° 024-2016-EM (Reglamento de Seguridad Minera), Art. 201:** "
        "autoriza jornadas atípicas y acumulativas en obras subterráneas aisladas "
        "siempre que el promedio no exceda 48 horas semanales.\n"
        "   - **Sentencia del Tribunal Constitucional (STC N° 4635-2004-AA/TC):** "
        "convalida los regímenes acumulativos (como el 14×7) al garantizar el descanso "
        "profiláctico adecuado en altitud.\n\n"
        "### 2.2 Justificación de las Guardias de 12 Horas (Día y Noche)\n"
        "1. **Minimización de Tiempos Muertos:**\n"
        "   En túneles largos donde el frente avanza kilómetros hacia el interior, "
        "el tránsito toma entre 30 y 45 minutos. Con tres turnos de 8 h se perderían "
        "hasta 4.5 h diarias en relevos. Dos guardias de 12 h optimizan la utilización "
        "de maquinaria pesada mediante un único relevo en caliente.\n"
        "2. **Ciclo Completo de Perforación y Voladura (*Drill & Blast*):**\n"
        "   El ciclo típico por pase (perforación con Jumbo 2.5 h, cargado de explosivos "
        "1.5 h, disparo y ventilación 1.0 h, desate mecanizado y acarreo LHD/volquetes "
        "3.5 h, sostenimiento con robot de shotcrete y pernos 3.0 h) suma ~11.5 a 12.0 h. "
        "La guardia de 12 horas asegura exactamente un ciclo cerrado y sostenido por turno.\n"
        f"3. **Distribución de Cargas:** {r['dia_total']} pax ({r['dia_total'] / r['total'] * 100:.1f}%) "
        f"en Guardia Día y {r['noche_total']} pax ({r['noche_total'] / r['total'] * 100:.1f}%) "
        "en Guardia Noche.",
    ]

    justificacion_mano_obra = [
        "Para una asignación de costos y responsabilidades operativas transparente, "
        "la dotación se descompone en Mano de Obra Directa (MOD) y Mano de Obra Indirecta (MOI):\n\n"
        "1. **Mano de Obra Directa (MOD — 110 pax · 31.8%):**\n"
        "   Trabajadores que intervienen directamente en el ciclo de arranque, "
        "sostenimiento y acarreo de la roca en el túnel:\n"
        "   - **Perforación y Voladura (38 pax):** Jumboístas titulares y de relevo, "
        "perforistas de emboquillado, blasters certificados SUCAMEC (Ley N° 30299) "
        "y ayudantes de cargado de explosivos.\n"
        "   - **Sostenimiento Mecanizado (12 pax):** Operadores de robot lanzador de "
        "shotcrete vía húmeda y cuadrillas de empernado / malla electrosoldada.\n"
        "   - **Carguío y Acarreo a DME (24 pax):** Operadores de pala LHD (Scooptram) "
        "y choferes de volquetes roqueros hacia botaderos autorizados.\n"
        "   - **Servicios de Frente y Plantas (15 pax):** Operadores de planta de concreto, "
        "mixers, bombas de achique y ventilación principal.\n"
        "   - **Ingeniería Subterránea y Geomecánica (21 pax):** Jefes de frente, "
        "geólogos de mina (RMR / Q de Barton), geomecánicos, topógrafos láser de precisión, "
        "ingenieros de planeamiento y laboratoristas de concreto.\n\n"
        "2. **Mano de Obra Indirecta (MOI — 236 pax · 68.2%):**\n"
        "   Personal que asegura la continuidad logística, habitabilidad, seguridad, "
        "mantenimiento y soporte institucional:\n"
        "   - **Personal de Campamento (155 pax):** Alta Dirección, Contabilidad y Costos, "
        "Asesoría Legal, RR.HH., Asistencia Social, Relaciones Comunitarias, TI/Redes, "
        "Servicio Médico Ocupacional / Paramédicos 24h, y el equipo integral de Catering, "
        "Cuartelería, Lavandería Industrial y Plantas PTAP/PTAR (99 pax).\n"
        "   - **Personal de Servicio y Soporte (81 pax):** Jefatura y supervisores SSOMA "
        "subterráneos 24h, especialistas en ventilación/gases, logística y almaceneros, "
        "talleres de mantenimiento electromecánico (jumbos, scoops, volquetes, electricistas), "
        "control de polvorín SUCAMEC, garitas de vigilancia y la flota de conductores "
        "(buses interprovinciales, ambulancias tipo II 24h, cisternas diésel y agua).",
    ]

    justificacion_campamentos = [
        "El dimensionamiento de los campamentos responde estrictamente a la ubicación de los frentes:\n"
        f"- **Campamento Principal CAMP1 (Portal A - Entrada): {r['camp1_total']} pax "
        f"({r['camp1_total'] / r['total'] * 100:.1f}%):** Aloja la administración central, "
        "talleres electromecánicos principales, ingeniería y el Frente 1 de excavación.\n"
        f"- **Campamento Satélite CAMP2 (Portal B - Salida): {r['camp2_total']} pax "
        f"({r['camp2_total'] / r['total'] * 100:.1f}%):** Instalación satélite autónoma dedicada "
        "al Frente 2 de excavación, con cuadrillas operativas, tópico médico de guardia, "
        "mantenimiento de retén y servicio de comedor/dormitorios propio.\n"
        f"- **Población Total en Campamento:** {r['total']} personas.\n"
        f"- **Dotación en Planilla (con relevo 14×7):** {r['planilla']} personas "
        f"(= ⌈{r['total']} × {r['factor_regimen']:.3f}⌉).",
    ]

    return Memoria(
        "04_Personal.md",
        "04 · Personal, Organigrama y Gestión de Capital Humano",
        [
            ("1. Resumen ejecutivo y parámetros maestros", resumen_ejecutivo),
            (
                "2. Justificación del régimen laboral y guardias de 12 horas",
                justificacion_regimen,
            ),
            (
                "3. Clasificación de Mano de Obra Directa (MOD) e Indirecta (MOI)",
                [_tabla_mano_obra(r), "\n".join(justificacion_mano_obra)],
            ),
            ("4. Estructura y macro-áreas funcionales", [_tabla_macro_areas(r)]),
            (
                "5. Distribución espacial y cruce de guardias",
                [_tabla_cruce_campamentos(r), "\n".join(justificacion_campamentos)],
            ),
        ],
    )
