"""Construcción de tablas y libro Excel para 04 · Personal."""

from ...modelo import Hoja, Libro, Tabla, tabla_parametros


def _tabla_macro_areas(r: dict, para_excel: bool = False) -> Tabla:
    filas = []
    macros = [
        ("1. Personal de Campamento", "Personal de Campamento", "{P_Camp}"),
        ("2. Personal de Frente (Túnel + Botaderos)", "Personal de Frente", "{P_Fren}"),
        ("3. Personal de Servicio y Soporte", "Personal de Servicio", "{P_Serv}"),
    ]
    for etiqueta, clave, sim in macros:
        if para_excel:
            c1 = f'=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "{clave}", Relacion_Completa!$F:$F, "CAMP1")'
            c2 = f'=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "{clave}", Relacion_Completa!$F:$F, "CAMP2")'
            dia = f'=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "{clave}", Relacion_Completa!$G:$G, "Dia")'
            noche = f'=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "{clave}", Relacion_Completa!$G:$G, "Noche")'
        else:
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
        tot = f"={sim}" if para_excel else r["por_macro_area"][clave]
        pct = (
            f"={sim}/{{Pob}}"
            if para_excel
            else f"{(r['por_macro_area'][clave] / r['total'] * 100):.1f} %"
        )
        filas.append([etiqueta, c1, c2, dia, noche, tot, pct])

    filas.append(
        [
            "TOTAL PROYECTO",
            "={Pob_C1}" if para_excel else r["camp1_total"],
            "={Pob_C2}" if para_excel else r["camp2_total"],
            "={G_Dia}" if para_excel else r["dia_total"],
            "={G_Noc}" if para_excel else r["noche_total"],
            "={Pob}" if para_excel else r["total"],
            "={Pob}/{Pob}" if para_excel else "100.0 %",
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


def _tabla_cruce_campamentos(r: dict, para_excel: bool = False) -> Tabla:
    if para_excel:
        c1_dia = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP1", Relacion_Completa!$G:$G, "Dia")'
        c1_noc = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP1", Relacion_Completa!$G:$G, "Noche")'
        c2_dia = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP2", Relacion_Completa!$G:$G, "Dia")'
        c2_noc = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP2", Relacion_Completa!$G:$G, "Noche")'
    else:
        c1_dia = r["camp1_dia"]
        c1_noc = r["camp1_noche"]
        c2_dia = r["camp2_dia"]
        c2_noc = r["camp2_noche"]

    filas = [
        [
            "Campamento 1 — Principal (Portal A)",
            c1_dia,
            c1_noc,
            "={Pob_C1}" if para_excel else r["camp1_total"],
        ],
        [
            "Campamento 2 — Satélite (Portal B)",
            c2_dia,
            c2_noc,
            "={Pob_C2}" if para_excel else r["camp2_total"],
        ],
        [
            "TOTAL GENERAL DEL PROYECTO",
            "={G_Dia}" if para_excel else r["dia_total"],
            "={G_Noc}" if para_excel else r["noche_total"],
            "={Pob}" if para_excel else r["total"],
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


def _tabla_mano_obra(r: dict, para_excel: bool = False) -> Tabla:
    if para_excel:
        staff_dir = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Directa", Relacion_Completa!$D:$D, "staff")'
        obr_dir = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Directa", Relacion_Completa!$D:$D, "obrero")'
        staff_ind = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Indirecta", Relacion_Completa!$D:$D, "staff")'
        obr_ind = '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Indirecta", Relacion_Completa!$D:$D, "obrero")'
    else:
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
            "={MOD}" if para_excel else r["directa"],
            (
                "={MOD}/{Pob}"
                if para_excel
                else f"{(r['directa'] / r['total'] * 100):.1f} %"
            ),
            "Excavación subterránea, perforación, voladura, sostenimiento y topografía",
        ],
        [
            "Mano de Obra Indirecta (MOI)",
            staff_ind,
            obr_ind,
            "={MOI}" if para_excel else r["indirecta"],
            (
                "={MOI}/{Pob}"
                if para_excel
                else f"{(r['indirecta'] / r['total'] * 100):.1f} %"
            ),
            "Dirección, SSOMA, talleres, transporte, catering, logística y habitabilidad",
        ],
        [
            "TOTAL",
            "={Ps}" if para_excel else r["staff"],
            "={Po}" if para_excel else r["obreros"],
            "={Pob}" if para_excel else r["total"],
            "={Pob}/{Pob}" if para_excel else "100.0 %",
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

    relacion_todas = _crear_tabla_relacion(
        r["filas"], "Relación nominal de todos los puestos del proyecto"
    )

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
            (
                "Población en campamento",
                "Pob",
                "={P_Camp}+{P_Fren}+{P_Serv}",
                "personas",
                "P_Camp + P_Fren + P_Serv",
            ),
            (
                "Personal de Campamento",
                "P_Camp",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "Personal de Campamento")',
                "personas",
                "Área Administrativa",
            ),
            (
                "Personal de Frente",
                "P_Fren",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "Personal de Frente")',
                "personas",
                "Área Operativa",
            ),
            (
                "Personal de Servicio",
                "P_Serv",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "Personal de Servicio")',
                "personas",
                "Área de Soporte",
            ),
            (
                "Campamento 1 (Portal A)",
                "Pob_C1",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP1")',
                "personas",
                "Portal Entrada",
            ),
            (
                "Campamento 2 (Portal B)",
                "Pob_C2",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$F:$F, "CAMP2")',
                "personas",
                "Portal Salida",
            ),
            (
                "Guardia Día (12h)",
                "G_Dia",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$G:$G, "Dia")',
                "personas",
                "07:00–19:00 h",
            ),
            (
                "Guardia Noche (12h)",
                "G_Noc",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$G:$G, "Noche")',
                "personas",
                "19:00–07:00 h",
            ),
            (
                "Mano de Obra Directa (MOD)",
                "MOD",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Directa")',
                "personas",
                "Frente y avances",
            ),
            (
                "Mano de Obra Indirecta (MOI)",
                "MOI",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$E:$E, "Indirecta")',
                "personas",
                "Soporte y campamento",
            ),
            (
                "Staff",
                "Ps",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$D:$D, "staff")',
                "personas",
                "Σ categoría staff",
            ),
            ("Obreros", "Po", "={Pob}-{Ps}", "personas", "Pob − Ps"),
            (
                "Personal de frente por guardia (1 frente)",
                "Pf",
                '=SUMIFS(Relacion_Completa!$H:$H, Relacion_Completa!$A:$A, "Personal de Frente", Relacion_Completa!$F:$F, "CAMP1", Relacion_Completa!$G:$G, "Dia")',
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
                "=ROUNDUP({Pob}*{fr}, 0)",
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
                    _tabla_macro_areas(r, para_excel=True),
                    _tabla_mano_obra(r, para_excel=True),
                    _tabla_cruce_campamentos(r, para_excel=True),
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
