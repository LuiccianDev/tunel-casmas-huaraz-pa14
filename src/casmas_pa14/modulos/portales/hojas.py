"""Generadores de hojas de cálculo Excel para el libro 11_Portales.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Tabla


def construir_hoja_banquetas(resultados: dict[str, Any]) -> Hoja:
    """Construye la hoja de cálculo geométrico y volumétrico de banquetas."""
    cols = [
        "ID Banqueta",
        "Largo L (m)",
        "Altura H (m)",
        "Ancho W (m)",
        "Talud α (°)",
        "Perfil β (°)",
        "Base Cuña (m)",
        "Área Sección (m²)",
        "Volumen In-Situ (m³)",
        "Esponjamiento",
        "Volumen Esponjado (m³)",
    ]

    filas = []
    fila_inicio = 5
    fila_actual = fila_inicio

    for b in resultados["banquetas"]:
        f_base = (
            f"=IF(E{fila_actual}=90, 0, C{fila_actual}/TAN(RADIANS(E{fila_actual})))"
        )
        f_area = f"=(D{fila_actual}*C{fila_actual})-(0.5*C{fila_actual}*G{fila_actual})"
        f_vol_insitu = f"=H{fila_actual}*B{fila_actual}"
        f_vol_esp = f"=I{fila_actual}*J{fila_actual}"

        filas.append(
            [
                b["id"],
                b["largo"],
                b["altura"],
                b["ancho"],
                b["alpha"],
                b["beta"],
                f_base,
                f_area,
                f_vol_insitu,
                b["factor_esp"],
                f_vol_esp,
            ]
        )
        fila_actual += 1

    if resultados["banquetas"]:
        fila_fin = fila_actual - 1
        filas.append(
            [
                "TOTAL PORTAL",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                f"=SUM(I{fila_inicio}:I{fila_fin})",
                "",
                f"=SUM(K{fila_inicio}:K{fila_fin})",
            ]
        )
    else:
        filas = [["No hay banquetas configuradas"] + [""] * 10]

    return Hoja(
        nombre="Banquetas_Portales",
        titulo="Cálculo Geométrico y Volumétrico de Banquetas de Portal",
        tablas=[Tabla(cols, filas)],
    )


def construir_hoja_q_slope(resultados: dict[str, Any]) -> Hoja | None:
    """Construye la hoja de estabilidad geomecánica Q-slope."""
    qs = resultados.get("q_slope")
    if not qs:
        return None

    cols_qs = [
        "Parámetro Geomecánico",
        "Símbolo",
        "Valor",
        "Unidad",
        "Criterio / Fuente",
    ]
    filas_qs = [
        [
            "Índice RQD en Talud",
            "RQD",
            qs["rqd"],
            "%",
            "Roca regular en portales (25% - 50%)",
        ],
        [
            "Número de Familias de Diaclasas",
            "Jn",
            qs["jn"],
            "-",
            "3 familias de discontinuidades principales",
        ],
        [
            "Rugosidad de Diaclasas",
            "Jr",
            qs["jr"],
            "-",
            "Juntas rugosas u onduladas, planas",
        ],
        [
            "Alteración y Relleno de Diaclasas",
            "Ja",
            qs["ja"],
            "-",
            "Paredes de junta alteradas con limo/arcilla",
        ],
        [
            "Factor de Agua en Talud",
            "Jw",
            qs["jw"],
            "-",
            "Presencia de goteo / humedad en ladera",
        ],
        [
            "Factor de Reducción de Tensión",
            "SRFa",
            qs["srfa"],
            "-",
            "Talud expuesto con intemperismo superficial",
        ],
        [
            "ÍNDICE Q-SLOPE CALCULADO",
            "Q_slope",
            "=(C5/C6)*(C7/C8)*(C9/C10)",
            "-",
            "Q_slope = (RQD/Jn)*(Jr/Ja)*(Jw/SRFa)",
        ],
        [
            "ÁNGULO MÁXIMO ESTABLE SIN SOSTENIMIENTO",
            "β_estable",
            "=20*LOG10(C11)+65",
            "°",
            "β = 20*LOG10(Q_slope) + 65° (Bar & Barton, 2015)",
        ],
    ]
    return Hoja(
        nombre="Q_Slope_Taludes",
        titulo="Estabilidad de Taludes de Banquetas mediante Q-Slope (Bar & Barton, 2015)",
        tablas=[
            Tabla(
                cols_qs,
                filas_qs,
                "Determinación del Ángulo Estable de Banqueta",
            )
        ],
    )


def construir_hoja_cortes_civil3d(resultados: dict[str, Any]) -> Hoja | None:
    """Construye la hoja de cubicaciones Civil 3D y parámetros DG-2018."""
    c3d = resultados.get("cortes_civil3d")
    if not c3d:
        return None

    cols_c3d = [
        "Alineamiento Civil 3D",
        "Línea de Muestreo (SLG)",
        "Estación Inicial",
        "Estación Final",
        "Longitud L (m)",
        "Calzada (m)",
        "Berma (m)",
        "Cuneta (m)",
        "Talud (H:V)",
        "Vol. Corte In-Situ (m³)",
        "Vol. Relleno (m³)",
    ]

    items_c3d = [
        ("acceso_tunel_b", "Acceso Túnel B"),
        ("acceso_botadero_b", "Acceso Botadero B"),
        ("acceso_banqueta_1", "Acceso Banqueta 1"),
        ("acceso_banqueta_2", "Acceso Banqueta 2"),
        ("banquetas_emboquille", "Banquetas Emboquille"),
    ]

    filas_c3d = []
    fila_c3d_inicio = 5
    fila_c3d_actual = fila_c3d_inicio

    for clave, etiqueta in items_c3d:
        info = c3d.get(clave, {})
        if info:
            filas_c3d.append(
                [
                    str(info.get("alineamiento", etiqueta)),
                    str(info.get("sample_line_group", "-")),
                    str(info.get("progresiva_inicio", "0+000")),
                    str(info.get("progresiva_fin", "-")),
                    float(info.get("longitud_m", 0.0)),
                    float(info.get("calzada_m", 0.0)),
                    float(info.get("berma_m", 0.0)),
                    float(info.get("cuneta_m", 0.0)),
                    str(c3d.get("talud_corte_h_v", "0.5:1")),
                    float(info.get("volumen_corte_m3", 0.0)),
                    float(info.get("volumen_relleno_m3", 0.0)),
                ]
            )
            fila_c3d_actual += 1

    if filas_c3d:
        fila_c3d_fin = fila_c3d_actual - 1
        filas_c3d.append(
            [
                "TOTAL GENERAL CORTE CIVIL 3D",
                "",
                "",
                "",
                f"=SUM(E{fila_c3d_inicio}:E{fila_c3d_fin})",
                "",
                "",
                "",
                "",
                f"=SUM(J{fila_c3d_inicio}:J{fila_c3d_fin})",
                f"=SUM(K{fila_c3d_inicio}:K{fila_c3d_fin})",
            ]
        )

    tablas_c3d = [
        Tabla(
            cols_c3d,
            filas_c3d,
            "Resumen de Cubicaciones por Alineamiento Vial",
        )
    ]

    dg2018 = resultados.get("dg2018_geometria")
    if dg2018:
        cols_dg = [
            "Parámetro de Diseño Vial (DG-2018 MTC)",
            "Símbolo",
            "Valor",
            "Unidad",
            "Fórmula / Criterio Normativo",
        ]
        filas_dg = [
            [
                "Clasificación de Vía",
                "Tipo",
                dg2018["clasificacion_via"],
                "-",
                "DG-2018 Obras Subterráneas / Accesos",
            ],
            [
                "Velocidad de Diseño",
                "V",
                dg2018["velocidad_diseno_kph"],
                "km/h",
                "DG-2018 Tabla 204.01 Orografía Tipo 4",
            ],
            [
                "Radio Mínimo Excepcional en Retornos",
                "R",
                dg2018["radio_minimo_curvatura_m"],
                "m",
                "DG-2018 Tabla 302.02 Curvas de Volteo",
            ],
            [
                "Distancia Entre Ejes de Vehículo de Diseño",
                "L",
                dg2018["distancia_ejes_vehiculo_m"],
                "m",
                "Camión C3/C4 Volvo FMX 8x4",
            ],
            [
                "Número de Carriles por Sentido",
                "n",
                dg2018["numero_carriles"],
                "-",
                "Tránsito unidireccional / alternado",
            ],
            [
                "Sobreancho Requerido en Curva",
                "S",
                dg2018["sobreancho_calculado_m"],
                "m",
                "S = n*(R - SQRT(R^2 - L^2)) + V/(10*SQRT(R))",
            ],
            [
                "Ancho de Calzada Base en Tangente",
                "B_tan",
                dg2018["ancho_calzada_base_m"],
                "m",
                "Assembly Civil 3D Subassembly LaneSuperelevation",
            ],
            [
                "Ancho de Calzada Ampliada en Curva",
                "B_curva",
                dg2018["ancho_calzada_ampliada_m"],
                "m",
                "B_curva = B_tan + S (DG-2018 Sección 302.09)",
            ],
            [
                "Pendiente Transversal de Bombeo",
                "p",
                dg2018["bombeo_calzada_pct"],
                "%",
                "DG-2018 Sección 304.04 (Drenaje de Calzada)",
            ],
            [
                "Talud de Corte en Desmonte",
                "Z",
                dg2018["talud_corte_h_v"],
                "H:V",
                "Civil 3D DaylightBasin / Q-Slope 63.42°",
            ],
            [
                "Ángulo de Talud de Desmonte",
                "α_talud",
                dg2018["angulo_talud_corte_deg"],
                "°",
                "arctan(1/0.5) = 63.43° (Estable sin soporte)",
            ],
            [
                "Ancho de Banqueta Intermedia de Resguardo",
                "W_banq",
                dg2018["ancho_banqueta_resguardo_m"],
                "m",
                "DG-2018 Sección 304.07 y Croquis Portal B",
            ],
            [
                "Altura Máxima de Banco de Corte",
                "H_banco",
                dg2018["altura_max_banco_m"],
                "m",
                "Desnivel máximo entre banquetas sucesivas",
            ],
            [
                "Contrapendiente de Banqueta hacia Talud",
                "i_banq",
                dg2018["pendiente_banqueta_pct"],
                "%",
                "Control de escorrentía pluvial hacia pie de talud",
            ],
            [
                "Diámetro de Giro Completo Cargador CAT 966H",
                "D_giro",
                dg2018["diametro_giro_cat966h_m"],
                "m",
                "Especificación Caterpillar 966H (Radio 7.26 m)",
            ],
            [
                "Ancho Mínimo de Explanada en Emboquille",
                "W_emb",
                dg2018["ancho_plataforma_emboquille_m"],
                "m",
                "Plataforma de Maniobra y Giro de Flota (Croquis Portal)",
            ],
        ]
        tablas_c3d.append(
            Tabla(
                cols_dg,
                filas_dg,
                "Parámetros Geométricos de Assemblies y Sobreanchos DG-2018",
            )
        )

    return Hoja(
        nombre="Cortes_Civil3D_Accesos",
        titulo="Cubicaciones y Secciones de Corte de Accesos y Banquetas (Autodesk Civil 3D)",
        tablas=tablas_c3d,
    )


def construir_hoja_cunetas(resultados: dict[str, Any]) -> Hoja | None:
    """Construye la hoja de diseño y verificación hidráulica de cunetas pluviales."""
    drenaje = resultados.get("drenaje_cunetas")
    if not drenaje:
        return None

    cols_hidro = [
        "Parámetro Hidrológico / Hidráulico",
        "Símbolo",
        "Valor",
        "Unidad",
        "Norma / Criterio de Diseño",
    ]
    filas_hidro = [
        [
            "Periodo de Retorno de Diseño",
            "Tr",
            drenaje["periodo_retorno_anos"],
            "años",
            "Manual de Hidrología e Hidráulica MTC (Cunetas y Drenaje Superficial)",
        ],
        [
            "Intensidad Máxima de Precipitación",
            "I",
            drenaje["intensidad_lluvia_mm_h"],
            "mm/h",
            "Isoyeta horaria de diseño - Estación Huaraz / Cuenca Casmas",
        ],
        [
            "Coeficiente de Escorrentía Medio",
            "C",
            drenaje["coeficiente_escorrentia"],
            "-",
            "Calzada compactada y taludes rocosos de desmonte",
        ],
        [
            "Coeficiente de Rugosidad de Manning",
            "n",
            drenaje["rugosidad_manning"],
            "-",
            "Cuneta de concreto simple f'c=175 kg/cm2 frotachado",
        ],
        [
            "Velocidad Mínima Permisible",
            "V_min",
            drenaje["velocidad_min_m_s"],
            "m/s",
            "Velocidad no sedimentable para arenas y limos (MTC)",
        ],
        [
            "Velocidad Máxima Permisible",
            "V_max",
            drenaje["velocidad_max_m_s"],
            "m/s",
            "Límite para evitar abrasión y cavitación en concreto",
        ],
        [
            "Borde Libre / Revancha Mínima",
            "BL_min",
            drenaje["borde_libre_min_m"],
            "m",
            "Margen de seguridad contra olas y colmatación",
        ],
    ]

    cols_cunetas = [
        "Tipo / Tramo de Cuneta",
        "Ancho T (m)",
        "Prof. H (m)",
        "Pendiente S (%)",
        "Longitud L (m)",
        "Área Cuenca (ha)",
        "Caudal Diseño Qp (l/s)",
        "Capacidad Máx Qmax (l/s)",
        "Tirante Normal yn (cm)",
        "Borde Libre BL (cm)",
        "Velocidad V (m/s)",
        "Froude Fr",
        "Factor Seg. (Qmax/Qp)",
        "Estado Normativo",
    ]

    filas_cunetas = []
    for c in drenaje.get("cunetas", []):
        filas_cunetas.append(
            [
                c["nombre"],
                c["ancho_superior_m"],
                c["profundidad_total_m"],
                c["pendiente_pct"],
                c["longitud_m"],
                c["area_cuenca_ha"],
                c["caudal_diseno_l_s"],
                c["capacidad_max_l_s"],
                c["tirante_normal_cm"],
                c["borde_libre_cm"],
                c["velocidad_flujo_m_s"],
                c["froude"],
                c["factor_seguridad_hidraulico"],
                c["estado_normativo"],
            ]
        )

    return Hoja(
        nombre="Cunetas_Drenaje_Pluvial",
        titulo="Diseño y Verificación Hidráulica de Cunetas de Drenaje (Fórmula de Manning & Método Racional)",
        tablas=[
            Tabla(
                cols_hidro,
                filas_hidro,
                "Criterios Hidrológicos y Parámetros de Diseño MTC",
            ),
            Tabla(
                cols_cunetas,
                filas_cunetas,
                "Comprobación de Tirante Normal, Velocidad Límite y Borde Libre",
            ),
        ],
    )


def construir_hoja_control_progresivas(resultados: dict[str, Any]) -> Hoja | None:
    ctrl = resultados.get("control_progresivas")
    if not ctrl:
        return None

    cols = [
        "Sector de Obra Exterior",
        "Progresiva (Tramo)",
        "Longitud L (m)",
        "Vol. Banco (m³)",
        "Vol. Suelto (m³)",
        "N° Viajes (16m³)",
        "Dist. Botadero (m)",
        "Ciclo Volquete (min)",
        "Rend. Flota (m³b/h)",
        "Horas Acarreo (h)",
        "Horas Cunetas (h)",
        "Guardias (10.5h)",
        "Días (2 g/d)",
    ]

    filas = []
    fila_actual = 5

    for s in ctrl["sectores"]:
        fila_inicio_sec = fila_actual
        for t in s["tramos"]:
            filas.append(
                [
                    s["sector"],
                    t["progresiva"],
                    t["longitud_m"],
                    t["vol_banco_m3"],
                    t["vol_suelto_m3"],
                    t["viajes"],
                    t["distancia_botadero_m"],
                    t["ciclo_volquete_min"],
                    t["rendimiento_flota_m3_h"],
                    t["horas_acarreo"],
                    t["horas_cuneta"],
                    t["guardias"],
                    t["dias"],
                ]
            )
            fila_actual += 1

        fila_fin_sec = fila_actual - 1
        filas.append(
            [
                f"SUBTOTAL {s['sector'].upper()}",
                "Resumen Sector",
                f"=SUM(C{fila_inicio_sec}:C{fila_fin_sec})",
                f"=SUM(D{fila_inicio_sec}:D{fila_fin_sec})",
                f"=SUM(E{fila_inicio_sec}:E{fila_fin_sec})",
                f"=SUM(F{fila_inicio_sec}:F{fila_fin_sec})",
                f"=AVERAGE(G{fila_inicio_sec}:G{fila_fin_sec})",
                f"=AVERAGE(H{fila_inicio_sec}:H{fila_fin_sec})",
                f"=AVERAGE(I{fila_inicio_sec}:I{fila_fin_sec})",
                f"=SUM(J{fila_inicio_sec}:J{fila_fin_sec})",
                f"=SUM(K{fila_inicio_sec}:K{fila_fin_sec})",
                f"=SUM(L{fila_inicio_sec}:L{fila_fin_sec})",
                f"=SUM(M{fila_inicio_sec}:M{fila_fin_sec})",
            ]
        )
        fila_actual += 1

    filas.append(
        [
            "TOTAL GENERAL OBRAS EXTERIORES",
            "5 Alineamientos Civil 3D",
            f"{ctrl['total_vol_banco_m3']:.2f} m3 in-situ",
            ctrl["total_vol_banco_m3"],
            ctrl["total_vol_suelto_m3"],
            ctrl["total_viajes"],
            740.0,
            6.25,
            386.3,
            ctrl["total_horas"],
            45.0,
            ctrl["total_guardias"],
            ctrl["total_dias"],
        ]
    )

    cols_resumen = [
        "Fase de Obra Exterior",
        "Alineamiento Principal",
        "Volumen Banco (m³)",
        "Equipo Clave Asignado",
        "Guardias (10.5 h)",
        "Días Netos Acarreo",
        "Días Ciclo Completo (*)",
        "Precedencia Lógica",
    ]
    filas_resumen = [
        [
            "Fase 1: Vía al Botadero",
            "ALINEAMIENTO-BOTADERO-B",
            10191.80,
            "CAT 966H + 4 Volvo FMX + D8T",
            2.3,
            1.2,
            2.0,
            "Inicio Obra Exterior",
        ],
        [
            "Fase 2: Rampas a Banquetas",
            "ACCESO-BANQUETA-1 / 2",
            12461.12,
            "Epiroc T25 + CAT 966H + 4 Volvo",
            3.4,
            1.7,
            3.0,
            "Predecesora: Fase 1",
        ],
        [
            "Fase 3: Banqueo Frontón Túnel",
            "BANQUETAS-TUNEL (Frontón)",
            24245.14,
            "Epiroc T25 + CAT 966H + Shotcrete",
            5.7,
            2.9,
            6.0,
            "Predecesora: Fase 2",
        ],
        [
            "Fase 4: Acceso Túnel y Emboquille",
            "ACCESO-TUNEL-B",
            29059.78,
            "CAT 966H + CAT 336D + 4 Volvo FMX",
            7.4,
            3.7,
            4.5,
            "Predecesora: Fase 3",
        ],
        [
            "TOTAL ACTIVIDAD D (CRONOGRAMA)",
            "Obras Exteriores y Accesos",
            75957.84,
            "Tren Pesado Completo",
            18.8,
            9.5,
            15.5,
            "Habilita Ingreso Jumbo (Act. E)",
        ],
    ]

    return Hoja(
        nombre="Control_Tiempos_Progresivas",
        titulo="Control de Tiempos Tramo a Tramo por Progresiva y Flota de Equipos (Civil 3D & Manning)",
        tablas=[
            Tabla(
                cols,
                filas,
                "Desglose por Progresiva (Corte, Acarreo Volvo FMX y Cunetas CAT 336D)",
            ),
            Tabla(
                cols_resumen,
                filas_resumen,
                "Resumen de Fases y Precedencias de Obras Exteriores (Actividad D)",
            ),
        ],
    )
