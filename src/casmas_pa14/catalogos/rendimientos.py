"""Motor de cálculo de rendimiento teórico y real para maquinaria pesada.

Basado en metodologías del Caterpillar Performance Handbook y manuales
técnicos de Epiroc y Sandvik.
"""

from ..modelo import OpcionLista, Tabla, tabla_parametros
from .tablas_referencia_cat import (
    _filas_cierre_movimiento_tierras,
    _tablas_sostenimiento_y_servicio,
    tabla_capas_estructurales,
    tabla_coeficientes_carga_k,
    tabla_compactacion_suelos,
    tabla_conversion_volumetrica,
    tabla_motoniveladora_trabajo,
    tabla_penetracion_rocas,
)

_TIT_MT = "Cálculo Dinámico de Rendimiento: R = (60 · E · Q · K) / (T · Fv)"


def _tablas_movimiento_tierras(
    eq_id: str, eff: float, falt: float, p_perdidas: float, f_ll: float
) -> list[Tabla]:
    """Tablas de rendimiento para tractores, cargador frontal, excavadora y volquetes."""
    ref_mt = [tabla_conversion_volumetrica(), tabla_coeficientes_carga_k()]
    if eq_id in ("CAT_D8", "CAT_D6"):
        cap_hoja = 8.7 if eq_id == "CAT_D8" else 4.2
        filas = [
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
            *_filas_cierre_movimiento_tierras(
                eff,
                falt,
                p_perdidas,
                f_ll,
                desc_k="Coeficiente de carga de la hoja",
                desc_fv="Factor de abundamiento de roca",
                desc_falt="Factor de corrección por altitud (3850 msnm)",
                fuente_falt="Pérdida por altitud",
                desc_p="Factor de pérdidas reales en obra",
                desc_fll="Factor de llenado efectivo",
                fuente_fll="Geometría del talud y cuchilla",
            ),
        ]
        return [tabla_parametros(filas, _TIT_MT), *ref_mt]

    if eq_id == "CAT_966H":
        filas = [
            (
                "Capacidad nominal del cucharón roquero",
                "Q",
                4.0,
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
            ("Tiempo de volteo y vaciado en tolva", "t3", 10.0, "seg", "Manual Cat"),
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
            *_filas_cierre_movimiento_tierras(
                eff,
                falt,
                p_perdidas,
                f_ll,
                desc_eff="Eficiencia de operación",
                desc_falt="Factor por altitud (3850 msnm)",
                fuente_falt="Catálogo de motor ACERT",
                desc_p="Pérdidas reales de posicionamiento",
                fuente_p="Tiempo de espera volquetes",
                desc_fll="Factor de llenado del balde",
                fuente_fll="Roca volada de frente",
            ),
        ]
        return [tabla_parametros(filas, _TIT_MT), *ref_mt]

    if eq_id == "CAT_336":
        filas = [
            (
                "Capacidad del cucharón Heavy Duty",
                "Q",
                2.10,
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
            *_filas_cierre_movimiento_tierras(
                eff, falt, p_perdidas, f_ll, fuente_p="Acomodo en banco y talud"
            ),
        ]
        return [tabla_parametros(filas, _TIT_MT), *ref_mt]

    cap_tolva = 16.0 if eq_id == "VOLVO_FMX_6X4" else 20.0
    dist_km = 1.9 if eq_id == "VOLVO_FMX_6X4" else 2.5
    filas = [
        ("Capacidad volumétrica de tolva", "Q", cap_tolva, "m³", "Ficha Volvo FMX"),
        ("Distancia media a botadero", "d", dist_km, "km", "Ruta de acarreo"),
        ("Velocidad cargado en pendiente", "vc", 25.0, "km/h", "Manual de operación"),
        ("Velocidad de retorno vacío", "vv", 35.0, "km/h", "Manual de operación"),
        (
            "Tiempo de carga con cargador/excavadora",
            "tc",
            3.0,
            "min",
            "4 pases de cargador",
        ),
        ("Tiempo de viaje cargado", "tida", "=({d}/{vc})*60", "min", "d / vc · 60"),
        (
            "Tiempo de basculamiento y descarga",
            "td",
            1.5,
            "min",
            "Descarga en botadero",
        ),
        ("Tiempo de retorno vacío", "tret", "=({d}/{vv})*60", "min", "d / vv · 60"),
        (
            "Tiempo de maniobras y pesaje",
            "tm",
            1.5,
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
        *_filas_cierre_movimiento_tierras(
            eff,
            falt,
            p_perdidas,
            0.85,
            desc_eff="Factor de eficiencia",
            fuente_falt="Compensación motor D13",
            fuente_p="Tránsito y cruces en túnel",
            desc_fll="Factor de llenado de tolva",
            fuente_fll="Enrase seguro",
        ),
    ]
    return [tabla_parametros(filas, _TIT_MT), *ref_mt]


def generar_tablas_rendimiento_equipo(ficha: dict, p: dict) -> list[Tabla]:
    """Genera la tabla de cálculo de rendimiento teórico y real, junto con sus tablas de justificación."""
    eq_id = ficha["id"]
    rnd = p["maquinaria"]["rendimientos"]
    falt = rnd["factor_altitud"]
    eff = rnd["eficiencia_operativa"]
    p_perdidas = rnd["porcentaje_perdidas_reales"]
    f_ll = rnd["factor_llenado_balde"]

    if eq_id in (
        "CAT_D8",
        "CAT_D6",
        "CAT_966H",
        "CAT_336",
        "VOLVO_FMX_6X4",
        "VOLVO_FMX_8X4",
    ):
        return _tablas_movimiento_tierras(eq_id, eff, falt, p_perdidas, f_ll)

    if eq_id == "CAT_140G":
        moto = rnd["motoniveladora"]
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
                    moto["ancho_hoja_m"],
                    "m",
                    "12 pies (Ficha técnica)",
                ),
                (
                    "Ancho efectivo de pasada (con cruce y solape)",
                    "A",
                    moto["ancho_efectivo_m"],
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
                    moto["eficiencia_operativa"],
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
        return [calculo, tabla_motoniveladora_trabajo(), tabla_capas_estructurales()]

    if eq_id == "CAT_CS11":
        rod = rnd["rodillo"]
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
                    rod["velocidad_trabajo_kmh"],
                    "km/h",
                    "Manual Caterpillar",
                ),
                (
                    "Ancho del tambor vibratorio",
                    "W_tamb",
                    rod["ancho_tambor_m"],
                    "m",
                    "Ficha técnica (84'')",
                ),
                (
                    "Traslape entre pasadas adyacentes",
                    "trasl",
                    rod["traslape_m"],
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
                    rod["perdidas_reales"],
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
        return [calculo, tabla_compactacion_suelos(), tabla_capas_estructurales()]

    if eq_id in ("JUMBO_DT820", "JUMBO_DT1131", "POWERROC_T25", "BOLTEC_M"):
        perf = rnd["perforacion"]
        n_brazos = 3 if "DT1131" in eq_id else (2 if "DT820" in eq_id else 1)
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
                    perf["disponibilidad_mecanica"],
                    "",
                    "Mantenimiento preventivo",
                ),
                (
                    "Factor de utilización en ciclo de perforación",
                    "U",
                    perf["factor_utilizacion"],
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
        return [calculo, tabla_penetracion_rocas()]

    return _tablas_sostenimiento_y_servicio(eq_id, eff, falt)
