"""Motor de cálculo de rendimiento teórico y real para maquinaria pesada.

Basado en metodologías del Caterpillar Performance Handbook y manuales
técnicos de Epiroc y Sandvik. Genera las tablas de cálculo de rendimiento
y las tablas de referencia y justificación empírica (conversión volumétrica,
coeficientes de llenado, velocidades de pasada, dureza de roca, etc.).
"""

from ..modelo import OpcionLista, Tabla, tabla_parametros

# =============================================================================
#  TABLAS DE REFERENCIA ESTÁNDAR (CATERPILLAR & EPIROC)
# =============================================================================


def tabla_conversion_volumetrica() -> Tabla:
    """Matriz estándar Caterpillar de factores de conversión volumétrica."""
    columnas = [
        "Clase de Material",
        "Estado Inicial",
        "En Banco",
        "Suelto (Fv)",
        "Compactado",
    ]
    filas = [
        ["Roca Dinamitada (Túnel)", "Banco a Suelto", 1.00, 1.50, 1.30],
        ["Tierra Común", "Banco a Suelto", 1.00, 1.25, 0.90],
        ["Arcilla", "Banco a Suelto", 1.00, 1.43, 0.90],
        ["Arena", "Banco a Suelto", 1.00, 1.11, 0.95],
        ["Grava", "Banco a Suelto", 1.00, 1.12, 0.95],
        ["Roca Fracturada / Desmonte", "Banco a Suelto", 1.00, 1.40, 1.25],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 1: Factores de Conversión Volumétrica (Caterpillar)",
        id_rango="REF_CONVERSION",
    )


def tabla_coeficientes_carga_k() -> Tabla:
    """Tabla de coeficientes de carga (K) y llenado según material."""
    columnas = [
        "Tipo de Material / Fragmentación",
        "K de Diseño",
        "Rango Típico",
        "Observación Operativa",
    ]
    filas = [
        [
            "Roca dinamitada de túnel (PA14)",
            0.80,
            "0.75 – 0.80",
            "Fragmentación controlada con precorte",
        ],
        [
            "Roca fracturada o suelo húmedo",
            0.75,
            "0.65 – 0.80",
            "Huecos intergranulares mayores",
        ],
        [
            "Grava o material denso",
            0.80,
            "0.70 – 0.85",
            "Resistencia media a penetración",
        ],
        [
            "Tierra suelta o común",
            0.90,
            "0.80 – 1.00",
            "Llenado fácil sin sobrecarga",
        ],
        [
            "Arena seca o limpia",
            0.85,
            "0.80 – 0.90",
            "Escurrimiento leve en bordes",
        ],
        [
            "Material fácilmente empujable (blando)",
            1.05,
            "1.00 – 1.10",
            "Corona abombada sobre cuchilla",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 2: Coeficiente de Carga K (Caterpillar Handbook)",
        id_rango="REF_CARGA_K",
    )


def tabla_motoniveladora_trabajo() -> Tabla:
    """Tabla de velocidades y pasadas de motoniveladora según tipo de labor."""
    columnas = [
        "Tipo de Trabajo",
        "Velocidad (km/h)",
        "Espesor Capa (m)",
        "N° Pasadas",
        "Rango Operativo",
    ]
    filas = [
        [
            "Nivelación intermedia o extendido de base",
            6.5,
            0.15,
            5,
            "5.0 – 8.0 km/h | 10 – 15 cm | 4 – 6 pasadas",
        ],
        [
            "Desbaste grueso (corte o extendido rápido)",
            4.0,
            0.20,
            3,
            "3.0 – 5.0 km/h | 15 – 25 cm | 3 – 4 pasadas",
        ],
        [
            "Perfilado fino y bombeo de calzada",
            5.0,
            0.08,
            5,
            "4.0 – 6.0 km/h | 5 – 10 cm | 4 – 6 pasadas",
        ],
        [
            "Conformado de talud y cunetas",
            3.0,
            0.12,
            7,
            "2.0 – 4.0 km/h | Variable | 6 – 8 pasadas",
        ],
        [
            "Escarificado de afirmado existente",
            2.5,
            0.15,
            3,
            "2.0 – 3.5 km/h | 10 – 20 cm | 2 – 3 pasadas",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 3: Modos de Trabajo y Pasadas de Motoniveladora (Cat 140G)",
        id_rango="REF_MOTO",
    )


def tabla_compactacion_suelos() -> Tabla:
    """Tabla de compactación por tipo de suelo y modo de vibración para rodillo."""
    columnas = [
        "Tipo de Material a Compactar",
        "Espesor Compactado (m)",
        "N° Pasadas",
        "Modo de Vibración",
        "Condición Óptima",
    ]
    filas = [
        [
            "Subbase estabilizada / afirmado",
            0.22,
            8,
            "Vibración media frecuencia",
            "Ligera humedad",
        ],
        [
            "Arena, grava, afirmado granular",
            0.25,
            5,
            "Frecuencia alta / baja amplitud",
            "Seca o con humedad óptima",
        ],
        [
            "Toba lítica / roca alterada",
            0.20,
            7,
            "Vibración alta amplitud",
            "Seca / semicompacta",
        ],
        [
            "Arcilla, limo (cohesivos)",
            0.18,
            10,
            "Vibración intermitente / pata de cabra",
            "Humedad óptima ±2%",
        ],
        [
            "Relleno rocoso o pedraplén",
            0.30,
            4,
            "Vibración alta amplitud",
            "Seco / con bloques",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 4: Parámetros de Compactación por Tipo de Suelo (Cat CS11)",
        id_rango="REF_RODILLO",
    )


def tabla_capas_estructurales() -> Tabla:
    """Espesores típicos de capas estructurales de vía de acceso y emboquille."""
    columnas = [
        "Tipo de Capa",
        "Descripción del Material",
        "Espesor Típico Compactado (cm)",
    ]
    filas = [
        [
            "Capa de subrasante",
            "Terreno natural escarificado y recompactado",
            "15 – 30 cm",
        ],
        [
            "Capa de subbase granular",
            "Material granular clasificado e inerte",
            "15 – 30 cm",
        ],
        [
            "Capa de base granular",
            "Grava chancada o afirmado de alta calidad",
            "15 – 25 cm",
        ],
        [
            "Capa de afirmado / rodadura",
            "Capa final de rodadura para tránsito pesado",
            "10 – 20 cm",
        ],
        [
            "Nivelación de berma y cuneta",
            "Material perfilado y compactado",
            "5 – 15 cm",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 5: Espesores Típicos de Capas Estructurales",
    )


def tabla_penetracion_rocas() -> Tabla:
    """Tabla Epiroc/Sandvik de velocidad de penetración según calidad geomecánica."""
    columnas = [
        "Calidad Geomecánica de Roca",
        "RMR Estimado",
        "Vp Diseño (m/min)",
        "Rango Vp",
        "Desgaste de Broca",
    ]
    filas = [
        [
            "Roca Regular (Diorita PA14)",
            "41 – 60",
            1.60,
            "1.50 – 1.80",
            "220 – 300 m",
        ],
        [
            "Roca Buena (Andesita/Granodiorita)",
            "61 – 80",
            1.50,
            "1.40 – 1.60",
            "160 – 220 m",
        ],
        [
            "Roca Muy Buena (Granito masivo)",
            "> 80",
            1.20,
            "1.10 – 1.30",
            "120 – 160 m",
        ],
        [
            "Roca Mala (Pizarras/Esquistos)",
            "21 – 40",
            2.00,
            "1.80 – 2.20",
            "300 – 400 m",
        ],
        [
            "Roca Muy Mala (Fallas y brechas)",
            "< 20",
            2.40,
            "2.20 – 2.60",
            "400 – 500 m",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 6: Velocidad de Penetración según Geomecánica (Sandvik / Epiroc)",
        id_rango="REF_PERFORACION",
    )


# =============================================================================
#  MOTOR DE CÁLCULO DE RENDIMIENTOS (TEÓRICO Y REAL)
# =============================================================================


def generar_tablas_rendimiento_equipo(ficha: dict, p: dict) -> list[Tabla]:
    """Genera la tabla de cálculo de rendimiento teórico y real, junto con sus tablas de justificación."""
    eq_id = ficha["id"]
    rnd = p["maquinaria"]["rendimientos"]
    falt = rnd["factor_altitud"]
    eff = rnd["eficiencia_operativa"]
    p_perdidas = rnd["porcentaje_perdidas_reales"]
    f_ll = rnd["factor_llenado_balde"]

    tablas = []

    # 1. TRACTORES DE ORUGAS (CAT D8, CAT D6)
    if eq_id in ("CAT_D8", "CAT_D6"):
        cap_hoja = 8.7 if eq_id == "CAT_D8" else 4.2
        calculo = tabla_parametros(
            [
                (
                    "Capacidad teórica de la hoja (SU / VPAT)",
                    "Q",
                    cap_hoja,
                    "m³",
                    "Especificación Caterpillar",
                ),
                ("Distancia media de empuje", "d", 30.0, "m", "Frente / plataforma"),
                ("Tiempo de corte y llenado", "t1", 15.0, "seg", "Manual Cat"),
                ("Tiempo de empuje", "t2", 18.0, "seg", "Manual Cat"),
                ("Tiempo de descarga y nivelación", "t3", 10.0, "seg", "Manual Cat"),
                ("Tiempo de retorno en retroceso", "t4", 14.0, "seg", "Manual Cat"),
                ("Tiempo de maniobras y giro", "t5", 10.0, "seg", "Manual Cat"),
                (
                    "Tiempo total del ciclo de empuje",
                    "T",
                    "=({t1}+{t2}+{t3}+{t4}+{t5})/60",
                    "min",
                    "Σ(t1..t5) / 60",
                ),
                ("Factor de eficiencia operativa", "E", eff, "", "50 min / hora"),
                (
                    "Tipo de material para factor K",
                    "Mat_K",
                    OpcionLista("Roca dinamitada de túnel (PA14)", "REF_CARGA_K"),
                    "",
                    "Selección de fragmentación",
                ),
                (
                    "Coeficiente de carga de la hoja",
                    "K",
                    "=VLOOKUP({Mat_K},{REF_CARGA_K},2,FALSE)",
                    "",
                    "Tabla 2 (Caterpillar)",
                ),
                (
                    "Clase de material en banco",
                    "Mat_Fv",
                    OpcionLista("Roca Dinamitada (Túnel)", "REF_CONVERSION"),
                    "",
                    "Selección geológica banco",
                ),
                (
                    "Factor de abundamiento de roca",
                    "Fv",
                    "=VLOOKUP({Mat_Fv},{REF_CONVERSION},4,FALSE)",
                    "",
                    "Tabla 1 (Banco a Suelto)",
                ),
                (
                    "RENDIMIENTO TEÓRICO",
                    "R_teo",
                    "=60*{E}*{Q}*{K}/({T}*{Fv})",
                    "m³/h",
                    "60 · E · Q · K / (T · Fv)",
                ),
                (
                    "Factor de corrección por altitud (3850 msnm)",
                    "Falt",
                    falt,
                    "",
                    "Pérdida por altitud",
                ),
                (
                    "Factor de pérdidas reales en obra",
                    "P",
                    p_perdidas,
                    "",
                    "Maniobras y demoras menores",
                ),
                (
                    "Factor de llenado efectivo",
                    "F_ll",
                    f_ll,
                    "",
                    "Geometría del talud y cuchilla",
                ),
                (
                    "RENDIMIENTO REAL EFECTIVO",
                    "R_real",
                    "={R_teo}*{Falt}*{P}*{F_ll}",
                    "m³/h",
                    "R_teo · Falt · P · F_ll",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (60 · E · Q · K) / (T · Fv)",
        )
        tablas.extend(
            [calculo, tabla_conversion_volumetrica(), tabla_coeficientes_carga_k()]
        )

    # 2. CARGADOR FRONTAL (CAT 966H)
    elif eq_id == "CAT_966H":
        cap_cucharon = 4.0
        calculo = tabla_parametros(
            [
                (
                    "Capacidad nominal del cucharón roquero",
                    "Q",
                    cap_cucharon,
                    "m³",
                    "Ficha técnica Caterpillar",
                ),
                (
                    "Distancia media de acarreo en 'V'",
                    "d",
                    35.0,
                    "m",
                    "Patrón de carguío estándar",
                ),
                ("Tiempo de llenado y penetración", "t1", 12.0, "seg", "Manual Cat"),
                ("Tiempo desplazamiento cargado", "t2", 12.0, "seg", "Manual Cat"),
                (
                    "Tiempo de volteo y vaciado en tolva",
                    "t3",
                    10.0,
                    "seg",
                    "Manual Cat",
                ),
                ("Tiempo desplazamiento vacío", "t4", 10.0, "seg", "Manual Cat"),
                (
                    "Tiempo de maniobras y cambios de marcha",
                    "t5",
                    8.0,
                    "seg",
                    "Manual Cat",
                ),
                (
                    "Tiempo total del ciclo de carguío",
                    "T",
                    "=({t1}+{t2}+{t3}+{t4}+{t5})/60",
                    "min",
                    "Σ(t1..t5) / 60",
                ),
                ("Eficiencia de operación", "E", eff, "", "50 min / hora"),
                (
                    "Tipo de material para factor K",
                    "Mat_K",
                    OpcionLista("Roca dinamitada de túnel (PA14)", "REF_CARGA_K"),
                    "",
                    "Selección de fragmentación",
                ),
                (
                    "Coeficiente de carga",
                    "K",
                    "=VLOOKUP({Mat_K},{REF_CARGA_K},2,FALSE)",
                    "",
                    "Tabla 2 (Caterpillar)",
                ),
                (
                    "Clase de material en banco",
                    "Mat_Fv",
                    OpcionLista("Roca Dinamitada (Túnel)", "REF_CONVERSION"),
                    "",
                    "Selección geológica banco",
                ),
                (
                    "Factor de abundamiento",
                    "Fv",
                    "=VLOOKUP({Mat_Fv},{REF_CONVERSION},4,FALSE)",
                    "",
                    "Tabla 1 (Banco a Suelto)",
                ),
                (
                    "RENDIMIENTO TEÓRICO",
                    "R_teo",
                    "=60*{E}*{Q}*{K}/({T}*{Fv})",
                    "m³/h",
                    "60 · E · Q · K / (T · Fv)",
                ),
                (
                    "Factor por altitud (3850 msnm)",
                    "Falt",
                    falt,
                    "",
                    "Catálogo de motor ACERT",
                ),
                (
                    "Pérdidas reales de posicionamiento",
                    "P",
                    p_perdidas,
                    "",
                    "Tiempo de espera volquetes",
                ),
                (
                    "Factor de llenado del balde",
                    "F_ll",
                    f_ll,
                    "",
                    "Roca volada de frente",
                ),
                (
                    "RENDIMIENTO REAL EFECTIVO",
                    "R_real",
                    "={R_teo}*{Falt}*{P}*{F_ll}",
                    "m³/h",
                    "R_teo · Falt · P · F_ll",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (60 · E · Q · K) / (T · Fv)",
        )
        tablas.extend(
            [calculo, tabla_conversion_volumetrica(), tabla_coeficientes_carga_k()]
        )

    # 3. EXCAVADORA HIDRÁULICA (CAT 336)
    elif eq_id == "CAT_336":
        cap_balde = 2.10
        calculo = tabla_parametros(
            [
                (
                    "Capacidad del cucharón Heavy Duty",
                    "Q",
                    cap_balde,
                    "m³",
                    "Ficha técnica Cat 336",
                ),
                (
                    "Ángulo medio de giro",
                    "ang",
                    90.0,
                    "grados",
                    "Operación óptima zanja/talud",
                ),
                (
                    "Tiempo del ciclo de excavación y giro",
                    "T",
                    0.40,
                    "min",
                    "24 seg / ciclo (Manual Cat)",
                ),
                ("Factor de eficiencia operativa", "E", eff, "", "50 min / hora"),
                (
                    "Tipo de material para factor K",
                    "Mat_K",
                    OpcionLista("Roca dinamitada de túnel (PA14)", "REF_CARGA_K"),
                    "",
                    "Selección de fragmentación",
                ),
                (
                    "Coeficiente de carga",
                    "K",
                    "=VLOOKUP({Mat_K},{REF_CARGA_K},2,FALSE)",
                    "",
                    "Tabla 2 (Caterpillar)",
                ),
                (
                    "Clase de material en banco",
                    "Mat_Fv",
                    OpcionLista("Roca Dinamitada (Túnel)", "REF_CONVERSION"),
                    "",
                    "Selección geológica banco",
                ),
                (
                    "Factor de abundamiento",
                    "Fv",
                    "=VLOOKUP({Mat_Fv},{REF_CONVERSION},4,FALSE)",
                    "",
                    "Tabla 1 (Banco a Suelto)",
                ),
                (
                    "RENDIMIENTO TEÓRICO",
                    "R_teo",
                    "=60*{E}*{Q}*{K}/({T}*{Fv})",
                    "m³/h",
                    "60 · E · Q · K / (T · Fv)",
                ),
                ("Factor por altitud", "Falt", falt, "", "3850 msnm"),
                (
                    "Pérdidas operativas",
                    "P",
                    p_perdidas,
                    "",
                    "Acomodo en banco y talud",
                ),
                ("Factor de llenado", "F_ll", f_ll, "", "Material escarificado"),
                (
                    "RENDIMIENTO REAL EFECTIVO",
                    "R_real",
                    "={R_teo}*{Falt}*{P}*{F_ll}",
                    "m³/h",
                    "R_teo · Falt · P · F_ll",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (60 · E · Q · K) / (T · Fv)",
        )
        tablas.extend(
            [calculo, tabla_conversion_volumetrica(), tabla_coeficientes_carga_k()]
        )

    # 4. CAMIONES VOLQUETE (VOLVO FMX 6X4, VOLVO FMX 8X4)
    elif eq_id in ("VOLVO_FMX_6X4", "VOLVO_FMX_8X4"):
        cap_tolva = 16.0 if eq_id == "VOLVO_FMX_6X4" else 20.0
        dist_km = 1.9 if eq_id == "VOLVO_FMX_6X4" else 2.5
        v_cargado = 25.0
        v_vacio = 35.0
        t_carga = 3.0
        t_descarga = 1.5
        t_maniobras = 1.5

        calculo = tabla_parametros(
            [
                (
                    "Capacidad volumétrica de tolva",
                    "Q",
                    cap_tolva,
                    "m³",
                    "Ficha Volvo FMX",
                ),
                ("Distancia media a botadero", "d", dist_km, "km", "Ruta de acarreo"),
                (
                    "Velocidad cargado en pendiente",
                    "vc",
                    v_cargado,
                    "km/h",
                    "Manual de operación",
                ),
                (
                    "Velocidad de retorno vacío",
                    "vv",
                    v_vacio,
                    "km/h",
                    "Manual de operación",
                ),
                (
                    "Tiempo de carga con cargador/excavadora",
                    "tc",
                    t_carga,
                    "min",
                    "4 pases de cargador",
                ),
                (
                    "Tiempo de viaje cargado",
                    "tida",
                    "=({d}/{vc})*60",
                    "min",
                    "d / vc · 60",
                ),
                (
                    "Tiempo de basculamiento y descarga",
                    "td",
                    t_descarga,
                    "min",
                    "Descarga en botadero",
                ),
                (
                    "Tiempo de retorno vacío",
                    "tret",
                    "=({d}/{vv})*60",
                    "min",
                    "d / vv · 60",
                ),
                (
                    "Tiempo de maniobras y pesaje",
                    "tm",
                    t_maniobras,
                    "min",
                    "Alineación en frente y botadero",
                ),
                (
                    "Tiempo total del ciclo de acarreo",
                    "T",
                    "={tc}+{tida}+{td}+{tret}+{tm}",
                    "min",
                    "Σ(tc + tida + td + tret + tm)",
                ),
                ("Factor de eficiencia", "E", eff, "", "50 min / hora"),
                (
                    "Tipo de material para factor K",
                    "Mat_K",
                    OpcionLista("Roca dinamitada de túnel (PA14)", "REF_CARGA_K"),
                    "",
                    "Selección de fragmentación",
                ),
                (
                    "Coeficiente de carga",
                    "K",
                    "=VLOOKUP({Mat_K},{REF_CARGA_K},2,FALSE)",
                    "",
                    "Tabla 2 (Caterpillar)",
                ),
                (
                    "Clase de material en banco",
                    "Mat_Fv",
                    OpcionLista("Roca Dinamitada (Túnel)", "REF_CONVERSION"),
                    "",
                    "Selección geológica banco",
                ),
                (
                    "Factor de abundamiento",
                    "Fv",
                    "=VLOOKUP({Mat_Fv},{REF_CONVERSION},4,FALSE)",
                    "",
                    "Tabla 1 (Banco a Suelto)",
                ),
                (
                    "RENDIMIENTO TEÓRICO",
                    "R_teo",
                    "=60*{E}*{Q}*{K}/({T}*{Fv})",
                    "m³/h",
                    "60 · E · Q · K / (T · Fv)",
                ),
                ("Factor por altitud", "Falt", falt, "", "Compensación motor D13"),
                (
                    "Pérdidas operativas",
                    "P",
                    p_perdidas,
                    "",
                    "Tránsito y cruces en túnel",
                ),
                ("Factor de llenado de tolva", "F_ll", 0.85, "", "Enrase seguro"),
                (
                    "RENDIMIENTO REAL EFECTIVO",
                    "R_real",
                    "={R_teo}*{Falt}*{P}*{F_ll}",
                    "m³/h",
                    "R_teo · Falt · P · F_ll",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (60 · E · Q · K) / (T · Fv)",
        )
        tablas.extend(
            [calculo, tabla_conversion_volumetrica(), tabla_coeficientes_carga_k()]
        )

    # 5. MOTONIVELADORA (CAT 140G)
    elif eq_id == "CAT_140G":
        moto = rnd["motoniveladora"]
        h_hoja = moto["ancho_hoja_m"]
        ancho_ef = moto["ancho_efectivo_m"]
        eff_moto = moto["eficiencia_operativa"]

        calculo = tabla_parametros(
            [
                (
                    "Modo de trabajo asignado",
                    "Modo",
                    OpcionLista(
                        "Nivelación intermedia o extendido de base", "REF_MOTO"
                    ),
                    "",
                    "Selección de modo de trabajo",
                ),
                (
                    "Velocidad media de trabajo",
                    "V",
                    "=VLOOKUP({Modo},{REF_MOTO},2,FALSE)",
                    "km/h",
                    "Tabla 3",
                ),
                (
                    "Longitud total de vertedera",
                    "H",
                    h_hoja,
                    "m",
                    "12 pies (Ficha técnica)",
                ),
                (
                    "Ancho efectivo de pasada (con cruce y solape)",
                    "A",
                    ancho_ef,
                    "m",
                    "H · cos(30°) - solape",
                ),
                (
                    "Espesor de capa de nivelación",
                    "E_capa",
                    "=VLOOKUP({Modo},{REF_MOTO},3,FALSE)",
                    "m",
                    "Tabla 3",
                ),
                (
                    "Número de pasadas requeridas",
                    "P",
                    "=VLOOKUP({Modo},{REF_MOTO},4,FALSE)",
                    "und",
                    "Tabla 3",
                ),
                (
                    "Eficiencia de motoniveladora",
                    "E",
                    eff_moto,
                    "",
                    "Habilidad de operador",
                ),
                (
                    "RENDIMIENTO TEÓRICO EN ÁREA",
                    "R_teo_A",
                    "=(1000*{V}*{A}*{E})/{P}",
                    "m²/h",
                    "(1000 · V · A · E) / P",
                ),
                (
                    "RENDIMIENTO TEÓRICO EN VOLUMEN",
                    "R_teo_V",
                    "={R_teo_A}*{E_capa}",
                    "m³/h",
                    "R_teo_A · E_capa",
                ),
                ("Factor de corrección por altitud", "Falt", falt, "", "3850 msnm"),
                (
                    "RENDIMIENTO REAL EN ÁREA",
                    "R_real_A",
                    "={R_teo_A}*{Falt}*{E}",
                    "m²/h",
                    "R_teo_A · Falt · E",
                ),
                (
                    "RENDIMIENTO REAL EN VOLUMEN",
                    "R_real_V",
                    "={R_teo_V}*{Falt}*{E}",
                    "m³/h",
                    "R_teo_V · Falt · E",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (1000 · V · A · E_capa · E) / P",
        )
        tablas.extend(
            [calculo, tabla_motoniveladora_trabajo(), tabla_capas_estructurales()]
        )

    # 6. RODILLO COMPACTADOR (CAT CS11)
    elif eq_id == "CAT_CS11":
        rod = rnd["rodillo"]
        v_rod = rod["velocidad_trabajo_kmh"]
        w_tamb = rod["ancho_tambor_m"]
        trasl = rod["traslape_m"]
        perd_rod = rod["perdidas_reales"]

        calculo = tabla_parametros(
            [
                (
                    "Tipo de material a compactar",
                    "Mat_Rod",
                    OpcionLista("Subbase estabilizada / afirmado", "REF_RODILLO"),
                    "",
                    "Selección de material",
                ),
                (
                    "Velocidad de avance con vibración",
                    "V",
                    v_rod,
                    "km/h",
                    "Manual Caterpillar",
                ),
                (
                    "Ancho del tambor vibratorio",
                    "W_tamb",
                    w_tamb,
                    "m",
                    "Ficha técnica (84'')",
                ),
                (
                    "Traslape entre pasadas adyacentes",
                    "trasl",
                    trasl,
                    "m",
                    "Criterio de compactación",
                ),
                (
                    "Ancho efectivo de pasada",
                    "A",
                    "={W_tamb}-{trasl}",
                    "m",
                    "W_tamb - traslape",
                ),
                (
                    "Espesor de capa compactada",
                    "C",
                    "=VLOOKUP({Mat_Rod},{REF_RODILLO},2,FALSE)",
                    "m",
                    "Tabla 4",
                ),
                (
                    "Número de pasadas recomendadas",
                    "P",
                    "=VLOOKUP({Mat_Rod},{REF_RODILLO},3,FALSE)",
                    "und",
                    "Tabla 4",
                ),
                ("Eficiencia de operación", "E", eff, "", "50 min / hora"),
                (
                    "RENDIMIENTO TEÓRICO DE COMPACTACIÓN",
                    "R_teo",
                    "=(1000*{V}*{A}*{C}*{E})/{P}",
                    "m³/h",
                    "(1000 · V · A · C · E) / P",
                ),
                ("Factor de corrección por altitud", "Falt", falt, "", "3850 msnm"),
                (
                    "Factor de pérdidas reales por maniobras",
                    "Floss",
                    perd_rod,
                    "",
                    "Pérdidas operativas",
                ),
                (
                    "RENDIMIENTO REAL EFECTIVO",
                    "R_real",
                    "={R_teo}*{Falt}*{Floss}",
                    "m³/h",
                    "R_teo · Falt · Floss",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = (1000 · V · A · C · E) / P",
        )
        tablas.extend(
            [calculo, tabla_compactacion_suelos(), tabla_capas_estructurales()]
        )

    # 7. PERFORADORAS (JUMBOS Y ROCKDRILL)
    elif eq_id in ("JUMBO_DT820", "JUMBO_DT1131", "POWERROC_T25", "BOLTEC_M"):
        perf = rnd["perforacion"]
        n_brazos = 3 if "DT1131" in eq_id else (2 if "DT820" in eq_id else 1)
        dmec = perf["disponibilidad_mecanica"]
        u_turno = perf["factor_utilizacion"]

        calculo = tabla_parametros(
            [
                (
                    "Calidad geomecánica de roca",
                    "Cal_Roca",
                    OpcionLista("Roca Regular (Diorita PA14)", "REF_PERFORACION"),
                    "",
                    "Selección de calidad de roca",
                ),
                (
                    "Número de brazos / martillos hidráulicos",
                    "N_brazos",
                    n_brazos,
                    "und",
                    "Ficha técnica",
                ),
                (
                    "Velocidad de penetración neta",
                    "Vp",
                    "=VLOOKUP({Cal_Roca},{REF_PERFORACION},3,FALSE)",
                    "m/min",
                    "Tabla 6",
                ),
                ("Longitud estándar de barreno", "Lb", 3.66, "m", "Barra de 12 pies"),
                (
                    "RENDIMIENTO TEÓRICO EN PERFORACIÓN",
                    "R_teo",
                    "={Vp}*60*{N_brazos}",
                    "m/h",
                    "Vp · 60 · N_brazos",
                ),
                ("Eficiencia de operadores", "E", eff, "", "50 min / hora"),
                (
                    "Disponibilidad mecánica del equipo",
                    "Dmec",
                    dmec,
                    "",
                    "Mantenimiento preventivo",
                ),
                (
                    "Factor de utilización en ciclo de perforación",
                    "U",
                    u_turno,
                    "",
                    "Tiempo efectivo de perforación",
                ),
                (
                    "Factor por altitud en unidad compresora",
                    "Falt",
                    falt,
                    "",
                    "3850 msnm",
                ),
                (
                    "RENDIMIENTO REAL EN METROS LINEALES",
                    "R_real",
                    "={R_teo}*{E}*{Falt}*{Dmec}*{U}",
                    "m/h",
                    "R_teo · E · Falt · Dmec · U",
                ),
                (
                    "Rendimiento equivalente en taladros perforados",
                    "N_tal_h",
                    "={R_real}/{Lb}",
                    "taladros/h",
                    "R_real / Lb",
                ),
            ],
            "Cálculo Dinámico de Rendimiento: R = Vp · 60 · N_brazos · Factores",
        )
        tablas.extend([calculo, tabla_penetracion_rocas()])

    # 8. EQUIPOS DE HORMIGÓN / SHOTCRETE (SPRAYMEC 8100, UTIMEC MF500)
    elif eq_id in ("SPRAYMEC_8100", "UTIMEC_MF500"):
        es_robot = eq_id == "SPRAYMEC_8100"
        cap_nom = 30.0 if es_robot else 4.4  # m3/h o m3/viaje

        calculo = tabla_parametros(
            [
                (
                    "Capacidad nominal de bombeo / tambor",
                    "Q_nom",
                    cap_nom,
                    "m³/h" if es_robot else "m³/viaje",
                    "Ficha fabricante Normet",
                ),
                (
                    "Factor de rebote y desperdicio de shotcrete",
                    "f_reb",
                    0.15,
                    "",
                    "Pérdida por impacto en roca",
                ),
                ("Eficiencia de colocado", "E", 0.80, "", "Condiciones en bóveda"),
                ("Factor por altitud", "Falt", falt, "", "3850 msnm"),
                (
                    "RENDIMIENTO REAL PROYECTADO",
                    "R_real",
                    "={Q_nom}*(1-{f_reb})*{E}*{Falt}",
                    "m³/h" if es_robot else "m³/viaje efectivo",
                    "Q_nom · (1 - f_reb) · E · Falt",
                ),
            ],
            "Cálculo Dinámico de Rendimiento Operativo de Hormigón / Shotcrete",
        )
        tablas.append(calculo)

    # 9. OTROS EQUIPOS LOGÍSTICOS Y SERVICIOS (Cisternas, Buses, Utilitarios, etc.)
    else:
        calculo = tabla_parametros(
            [
                (
                    "Régimen de operación asignado",
                    "Turno",
                    "Continuo 24h",
                    "",
                    "04_Personal",
                ),
                ("Disponibilidad mecánica estimada", "Dmec", 0.90, "", "Plan de flota"),
                (
                    "Eficiencia operativa de ruta",
                    "E",
                    eff,
                    "",
                    "Velocidad controlada en obra",
                ),
                ("Factor por altitud de motor", "Falt", falt, "", "3850 msnm"),
                (
                    "Cumplimiento normativo",
                    "Norma",
                    "D.S. 024-2016-EM",
                    "",
                    "Transporte y seguridad",
                ),
            ],
            "Parámetros de Operatividad y Rendimiento de Servicio",
        )
        tablas.append(calculo)

    return tablas
