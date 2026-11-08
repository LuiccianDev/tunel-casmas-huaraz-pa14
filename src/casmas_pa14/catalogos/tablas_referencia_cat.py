"""Tablas de referencia estándar Caterpillar, Epiroc y Sandvik para maquinaria pesada."""

from ..modelo import OpcionLista, Tabla, tabla_parametros


def _filas_cierre_movimiento_tierras(
    eff: float,
    falt: float,
    p_perdidas: float,
    f_ll: float,
    *,
    desc_eff: str = "Factor de eficiencia operativa",
    desc_k: str = "Coeficiente de carga",
    desc_fv: str = "Factor de abundamiento",
    desc_falt: str = "Factor por altitud",
    fuente_falt: str = "3850 msnm",
    desc_p: str = "Pérdidas operativas",
    fuente_p: str = "Maniobras y demoras menores",
    desc_fll: str = "Factor de llenado",
    fuente_fll: str = "Material escarificado",
) -> list[tuple]:
    """Filas compartidas de E, K, Fv, R_teo y R_real para equipos de movimiento de tierras."""
    return [
        (desc_eff, "E", eff, "", "50 min / hora"),
        (
            "Tipo de material para factor K",
            "Mat_K",
            OpcionLista("Roca dinamitada de túnel (PA14)", "REF_CARGA_K"),
            "",
            "Selección de fragmentación",
        ),
        (
            desc_k,
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
            desc_fv,
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
        (desc_falt, "Falt", falt, "", fuente_falt),
        (desc_p, "P", p_perdidas, "", fuente_p),
        (desc_fll, "F_ll", f_ll, "", fuente_fll),
        (
            "RENDIMIENTO REAL EFECTIVO",
            "R_real",
            "={R_teo}*{Falt}*{P}*{F_ll}",
            "m³/h",
            "R_teo · Falt · P · F_ll",
        ),
    ]


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


def _tablas_sostenimiento_y_servicio(
    eq_id: str, eff: float, falt: float
) -> list[Tabla]:
    """Tablas de rendimiento operativo para equipos de shotcrete y servicios."""
    if eq_id in ("SPRAYMEC_8100", "UTIMEC_MF500"):
        es_robot = eq_id == "SPRAYMEC_8100"
        cap_nom = 30.0 if es_robot else 4.4
        return [
            tabla_parametros(
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
        ]

    return [
        tabla_parametros(
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
    ]
