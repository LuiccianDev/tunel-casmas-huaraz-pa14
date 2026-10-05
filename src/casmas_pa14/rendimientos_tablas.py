"""Motor de cálculo de rendimiento teórico y real para maquinaria pesada.

Basado en metodologías del Caterpillar Performance Handbook y manuales
técnicos de Epiroc y Sandvik. Genera las tablas de cálculo de rendimiento
y las tablas de referencia y justificación empírica (conversión volumétrica,
coeficientes de llenado, velocidades de pasada, dureza de roca, etc.).
"""

from .modelo import Tabla, tabla_parametros

# =============================================================================
#  TABLAS DE REFERENCIA ESTÁNDAR (CATERPILLAR & EPIROC)
# =============================================================================


def tabla_conversion_volumetrica() -> Tabla:
    """Matriz estándar Caterpillar de factores de conversión volumétrica."""
    columnas = [
        "Clase de Material",
        "Estado Inicial",
        "Natural (Banco)",
        "Suelto",
        "Compactado",
    ]
    filas = [
        ["Arcilla", "Natural (1)", 1.00, 1.43, 0.90],
        ["Arcilla", "Suelto (1)", 0.70, 1.00, 0.64],
        ["Arcilla", "Compactado (1)", 1.11, 1.59, 1.00],
        ["Tierra Común", "Natural (2)", 1.00, 1.25, 0.90],
        ["Tierra Común", "Suelto (2)", 0.80, 1.00, 0.72],
        ["Tierra Común", "Compactado (2)", 1.11, 1.39, 1.00],
        ["Arena", "Natural (3)", 1.00, 1.11, 0.95],
        ["Arena", "Suelto (3)", 0.90, 1.00, 0.86],
        ["Arena", "Compactado (3)", 1.05, 1.17, 1.00],
        ["Grava", "Natural (4)", 1.00, 1.12, 0.95],
        ["Grava", "Suelto (4)", 0.89, 1.00, 0.84],
        ["Grava", "Compactado (4)", 1.05, 1.18, 1.00],
        ["Roca Dinamitada (Túnel)", "Natural (5)", 1.00, 1.50, 1.30],
        ["Roca Dinamitada (Túnel)", "Suelto (5)", 0.67, 1.00, 0.87],
        ["Roca Dinamitada (Túnel)", "Compactado (5)", 0.77, 1.15, 1.00],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 1: Factores de Conversión Volumétrica (Caterpillar)",
    )


def tabla_coeficientes_carga_k() -> Tabla:
    """Tabla de coeficientes de carga (K) y llenado según material."""
    columnas = ["Tipo de Material", "Coeficiente de Carga (k)", "Observación Operativa"]
    filas = [
        ["Tierra suelta o común", "0.80 – 1.00", "Llenado fácil sin sobrecarga"],
        ["Arena seca o limpia", "0.80 – 0.90", "Escurrimiento en bordes"],
        ["Grava o material denso", "0.70 – 0.85", "Resistencia a la penetración"],
        [
            "Roca fracturada o suelo húmedo",
            "0.65 – 0.80",
            "Huecos intergranulares mayores",
        ],
        [
            "Roca dinamitada de túnel (PA14)",
            "0.75 – 0.80",
            "Fragmentación controlada con precorte",
        ],
        [
            "Material fácilmente empujable (blando)",
            "1.00 – 1.10",
            "Corona abombada sobre la hoja/cucharón",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 2: Coeficiente de Carga K (Caterpillar Handbook)",
    )


def tabla_motoniveladora_trabajo() -> Tabla:
    """Tabla de velocidades y pasadas de motoniveladora según tipo de labor."""
    columnas = [
        "Tipo de Trabajo",
        "Velocidad Típica (km/h)",
        "Espesor de Corte/Capa (cm)",
        "N° Pasadas Típicas",
    ]
    filas = [
        ["Desbaste grueso (corte o extendido rápido)", "3.0 – 5.0", "15 – 25", "3 – 4"],
        ["Nivelación intermedia o extendido de base", "5.0 – 8.0", "10 – 15", "4 – 6"],
        ["Perfilado fino y bombeo de calzada", "4.0 – 6.0", "5 – 10", "4 – 6"],
        ["Conformado de talud y cunetas", "2.0 – 4.0", "Variable", "6 – 8"],
        ["Escarificado de afirmado existente", "2.0 – 3.5", "10 – 20", "2 – 3"],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 3: Modos de Trabajo y Pasadas de Motoniveladora (Cat 140G)",
    )


def tabla_compactacion_suelos() -> Tabla:
    """Tabla de compactación por tipo de suelo y modo de vibración para rodillo."""
    columnas = [
        "Tipo de Material",
        "Condición del Material",
        "Espesor Compactado (m)",
        "N° Pasadas",
        "Modo de Vibración",
    ]
    filas = [
        [
            "Arena, grava, afirmado granular",
            "Seca o con humedad óptima",
            "0.20 – 0.30",
            "4 – 6",
            "Frecuencia alta / baja amplitud",
        ],
        [
            "Toba lítica / roca alterada",
            "Seca / semicompacta",
            "0.15 – 0.25",
            "6 – 8",
            "Vibración alta amplitud",
        ],
        [
            "Arcilla, limo (cohesivos)",
            "Humedad óptima ±2%",
            "0.15 – 0.20",
            "8 – 12",
            "Vibración intermitente / pata de cabra",
        ],
        [
            "Subbase estabilizada / afirmado",
            "Ligera humedad",
            "0.20 – 0.25",
            "6 – 10",
            "Vibración media frecuencia",
        ],
        [
            "Relleno rocoso o pedraplén",
            "Seco / con bloques",
            "0.25 – 0.35",
            "3 – 5",
            "Vibración alta amplitud",
        ],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 4: Parámetros de Compactación por Tipo de Suelo (Cat CS11)",
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
        "Tipo de Roca / Calidad",
        "RMR Estimado",
        "Velocidad Penetración Vp (m/min)",
        "Desgaste de Broca (m/afilado)",
    ]
    filas = [
        ["Roca Muy Buena (Granito masivo)", "> 80", "1.10 – 1.30", "120 – 160 m"],
        ["Roca Buena (Andesita/Granodiorita)", "61 – 80", "1.40 – 1.60", "160 – 220 m"],
        [
            "Roca Regular (Diorita fracturada - PA14)",
            "41 – 60",
            "1.50 – 1.80",
            "220 – 300 m",
        ],
        [
            "Roca Mala (Pizarras/Esquistos cizallados)",
            "21 – 40",
            "1.80 – 2.20",
            "300 – 400 m",
        ],
        ["Roca Muy Mala (Fallas y brechas)", "< 20", "2.20 – 2.60", "400 – 500 m"],
    ]
    return Tabla(
        columnas,
        filas,
        "Tabla de Referencia 6: Velocidad de Penetración según Geomecánica (Sandvik / Epiroc)",
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
    fv = rnd["factor_abundamiento"]
    k_carga = rnd["coeficiente_carga_k"]
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
                    "Coeficiente de carga de la hoja",
                    "K",
                    k_carga,
                    "",
                    "Tabla 2 (Roca fragmentada)",
                ),
                (
                    "Factor de abundamiento de roca",
                    "Fv",
                    fv,
                    "",
                    "Tabla 1 (Roca dinamitada natural a suelto)",
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

    # 2. CARGADORES FRONTALES (CAT 966H, CAT 966GC)
    elif eq_id in ("CAT_966H", "CAT_966GC"):
        cap_cucharon = 4.0 if eq_id == "CAT_966H" else 3.8
        calculo = tabla_parametros(
            [
                (
                    "Capacidad nominal del cucharón roquero",
                    "Q",
                    cap_cucharon,
                    "m³",
                    "Ficha técnica fabricante",
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
                    "Coeficiente de carga",
                    "K",
                    k_carga,
                    "",
                    "Tabla 2 (Roca fragmentada)",
                ),
                ("Factor de abundamiento", "Fv", fv, "", "Tabla 1 (Roca dinamitada)"),
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
                    "Coeficiente de carga",
                    "K",
                    k_carga,
                    "",
                    "Tabla 2 (Material granular/roca)",
                ),
                ("Factor de abundamiento", "Fv", fv, "", "Tabla 1 (Roca dinamitada)"),
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
                ("Coeficiente de carga", "K", k_carga, "", "Tabla 2"),
                ("Factor de abundamiento", "Fv", fv, "", "Tabla 1"),
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
        v_moto = moto["velocidad_trabajo_kmh"]
        h_hoja = moto["ancho_hoja_m"]
        ancho_ef = moto["ancho_efectivo_m"]
        esp_capa = moto["espesor_capa_m"]
        n_pasadas = moto["numero_pasadas"]
        eff_moto = moto["eficiencia_operativa"]

        calculo = tabla_parametros(
            [
                (
                    "Velocidad media de trabajo",
                    "V",
                    v_moto,
                    "km/h",
                    "Tabla 3 (Nivelación intermedia)",
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
                    esp_capa,
                    "m",
                    "Tabla 5 (Subbase/base)",
                ),
                ("Número de pasadas requeridas", "P", n_pasadas, "und", "Tabla 3"),
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
        esp_comp = rod["espesor_capa_compactada_m"]
        n_pasadas_rod = rod["numero_pasadas"]
        perd_rod = rod["perdidas_reales"]

        calculo = tabla_parametros(
            [
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
                    esp_comp,
                    "m",
                    "Tabla 4 (Afirmado granular)",
                ),
                (
                    "Número de pasadas recomendadas",
                    "P",
                    n_pasadas_rod,
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
        vp = perf["velocidad_penetracion_m_min"]
        dmec = perf["disponibilidad_mecanica"]
        u_turno = perf["factor_utilizacion"]

        calculo = tabla_parametros(
            [
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
                    vp,
                    "m/min",
                    "Tabla 6 (Roca Regular PA14)",
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
