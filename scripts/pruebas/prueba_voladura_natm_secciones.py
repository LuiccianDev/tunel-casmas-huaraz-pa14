"""01 · Script de prueba: Perforación y Voladura por Secciones Divididas según el Nuevo Método Austriaco (NATM).

Compara la excavación a Sección Plena (Full Face / "de uno solo") contra la excavación por fases
(Calota superior / Top Heading y Destroza inferior / Bench) para el Túnel Casmas Huaraz PA14
(sección herradura 13.30 x 9.58 m, A = 108.43 m², L = 5,556.08 m con Jumbo Sandvik DT1131).

Genera el libro dinámico de Excel:
`salidas/excel/Prueba_NATM_Seccion_Dividida.xlsx`
utilizando fórmulas nativas de Excel y estilo corporativo institucional (#2E7D32).
"""

import sys
from pathlib import Path

# Permitir importaciones del paquete casmas_pa14 si se ejecuta directamente
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent
if str(RAIZ_PROYECTO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO / "src"))

from casmas_pa14.excel import escribir_libro  # noqa: E402
from casmas_pa14.modelo import Hoja, Libro, Tabla, tabla_parametros  # noqa: E402


def crear_hoja_comparativa() -> Hoja:
    """Crea la hoja con el resumen comparativo directo de ambos métodos."""
    columnas = [
        "Parámetro Técnico / Operativo",
        "Unidad",
        "Sección Plena (Full Face)",
        "Calota (Top Heading)",
        "Destroza (Bench)",
        "Suma Fases NATM",
        "Diferencia Fases vs Plena",
    ]
    filas = [
        [
            "Área de excavación",
            "m²",
            108.43,
            69.46,
            38.97,
            "=D6+E6",
            "=F6-C6",
        ],
        [
            "Altura de frente de trabajo",
            "m",
            9.58,
            6.65,
            2.93,
            "9.58",
            "0.00",
        ],
        [
            "Ancho de excavación en base",
            "m",
            13.30,
            13.30,
            13.30,
            "13.30",
            "0.00",
        ],
        [
            "Taladros de alivio escariados (Ø 102 mm)",
            "und",
            4,
            4,
            0,
            "=D9+E9",
            "=F9-C9",
        ],
        [
            "Taladros de producción y recorte (Ø 45 mm)",
            "und",
            227,
            148,
            82,
            "=D10+E10",
            "=F10-C10",
        ],
        [
            "Total taladros perforados por ciclo",
            "und",
            231,
            152,
            82,
            "=D11+E11",
            "=F11-C11",
        ],
        [
            "Longitud de barreno Jumbo (12 ft)",
            "m",
            3.66,
            3.66,
            3.66,
            "3.66",
            "0.00",
        ],
        [
            "Eficiencia de avance",
            "%",
            0.90,
            0.90,
            0.90,
            "90.0%",
            "0.0%",
        ],
        [
            "Avance lineal por disparo",
            "m",
            3.30,
            3.30,
            3.30,
            "3.30",
            "0.00",
        ],
        [
            "Volumen in situ excavado por avance",
            "m³",
            "=C6*C14",
            "=D6*D14",
            "=E6*E14",
            "=D15+E15",
            "=F15-C15",
        ],
        [
            "Metros lineales perforados por ciclo",
            "m",
            "=C11*C12",
            "=D11*D12",
            "=E11*E12",
            "=D16+E16",
            "=F16-C16",
        ],
        [
            "Tiempo neto perforación Jumbo 3 brazos",
            "horas",
            "=C16/(3*1.50*60)",
            "=D16/(3*1.50*60)",
            "=E16/(3*1.50*60)",
            "=D17+E17",
            "=F17-C17",
        ],
        [
            "Factor de carga explosiva específico",
            "kg/m³",
            1.60,
            1.45,
            1.15,
            "=F19/F15",
            "=F18-C18",
        ],
        [
            "Consumo total de explosivo por avance",
            "kg",
            "=C15*C18",
            "=D15*D18",
            "=E15*E18",
            "=D19+E19",
            "=F19-C19",
        ],
        [
            "Carga máxima operante por retardo (Q)",
            "kg/retardo",
            32.0,
            16.0,
            10.0,
            "16.0",
            "-16.0",
        ],
        [
            "Vibración estimada PPV @ 20 m (USBM)",
            "mm/s",
            "=500*(20/SQRT(C20))^(-1.6)",
            "=500*(20/SQRT(D20))^(-1.6)",
            "=500*(20/SQRT(E20))^(-1.6)",
            "=D21",
            "=F21-C21",
        ],
        [
            "Riesgo de sobreexcavación e inestabilidad",
            "Cualitativo",
            "ALTO en RMR < 45",
            "BAJO (anillo cerrado)",
            "NULO (banco libre)",
            "CONTROLADO",
            "Reducción crítica",
        ],
        [
            "Tiempo de autosoporte disponible (Lauffer)",
            "horas",
            "< 2 h en roca mala",
            "> 8 h (vano reducido)",
            "Estable (con bóveda)",
            "SEGURO",
            "Permite soporte",
        ],
    ]
    tabla = Tabla(
        columnas=columnas,
        filas=filas,
        titulo="Cuadro Comparativo: Sección Plena vs. Excavación por Fases NATM",
    )
    return Hoja(
        nombre="01_Comparativa_Metodos",
        titulo="Resumen Técnico-Operativo: Sección Plena vs. Fases NATM (Calota y Destroza)",
        tablas=[tabla],
    )


def crear_hoja_seccion_plena() -> Hoja:
    """Crea la hoja de parámetros detallados para Sección Plena (Full Face)."""
    filas_geo = [
        ("Ancho total de excavación", "B_PLENA", 13.30, "m", "Plano CAD Tunel PA14"),
        ("Altura total de excavación", "H_PLENA", 9.58, "m", "Plano CAD Tunel PA14"),
        ("Radio de la bóveda semicircular", "R_PLENA", "={B_PLENA}/2", "m", "B / 2"),
        (
            "Altura del hastial vertical",
            "HW_PLENA",
            "={H_PLENA}-{R_PLENA}",
            "m",
            "H - R",
        ),
        (
            "Área total de excavación",
            "A_PLENA",
            "={B_PLENA}*{HW_PLENA}+PI()*{B_PLENA}^2/8",
            "m²",
            "Sección Herradura MTC",
        ),
        (
            "Perímetro de la sección",
            "P_PLENA",
            "={B_PLENA}+2*{HW_PLENA}+PI()*{B_PLENA}/2",
            "m",
            "Perímetro total",
        ),
    ]

    filas_perf = [
        (
            "Taladros de alivio escariados Ø 102 mm",
            "N_ALIVIO_P",
            4,
            "und",
            "Cuñe de 4 secciones",
        ),
        (
            "Taladros de cuele quemado Ø 45 mm",
            "N_CUELE_P",
            16,
            "und",
            "Rombo concéntrico",
        ),
        ("Taladros de ayudas Ø 45 mm", "N_AYUDAS_P", 20, "und", "Ampliación de cuele"),
        (
            "Taladros de destroza / núcleo Ø 45 mm",
            "N_DEST_P",
            105,
            "und",
            "Malla cuadrada 0.85m",
        ),
        (
            "Taladros cuadradores (hastiales) Ø 45 mm",
            "N_CUAD_P",
            22,
            "und",
            "Contorno vertical",
        ),
        (
            "Taladros de corona (techo bóveda) Ø 45 mm",
            "N_COR_P",
            42,
            "und",
            "Recorte esp. 0.50m",
        ),
        (
            "Taladros de zapateras (piso) Ø 45 mm",
            "N_ZAP_P",
            26,
            "und",
            "Arrastre de solera",
        ),
        (
            "Total taladros cargados",
            "N_CARGADOS_P",
            "={N_CUELE_P}+{N_AYUDAS_P}+{N_DEST_P}+{N_CUAD_P}+{N_COR_P}+{N_ZAP_P}",
            "und",
            "Suma de taladros cargados",
        ),
        (
            "Total taladros perforados",
            "N_TOTAL_P",
            "={N_CARGADOS_P}+{N_ALIVIO_P}",
            "und",
            "Cargados + Alivio",
        ),
        (
            "Longitud del barreno de perforación",
            "LB_P",
            3.66,
            "m",
            "Barra Sandvik 12 ft",
        ),
        ("Eficiencia de avance", "EF_AV_P", 0.90, "%", "Efecto de cuñe quemado"),
        (
            "Avance efectivo por disparo",
            "AV_DISP_P",
            "={LB_P}*{EF_AV_P}",
            "m",
            "LB * Eficiencia",
        ),
        (
            "Volumen excavado por disparo",
            "VOL_DISP_P",
            "={A_PLENA}*{AV_DISP_P}",
            "m³",
            "Área * Avance",
        ),
        (
            "Metros totales perforados por ciclo",
            "METROS_P",
            "={N_TOTAL_P}*{LB_P}",
            "m",
            "Taladros * LB",
        ),
        ("Número de brazos del Jumbo", "BRAZOS_P", 3, "und", "Sandvik DT1131"),
        (
            "Velocidad neta de penetración",
            "VP_P",
            1.50,
            "m/min",
            "Roca andesita RMR 55",
        ),
        (
            "Tiempo neto de perforación",
            "T_PERF_P",
            "={METROS_P}/({BRAZOS_P}*{VP_P}*60)",
            "horas",
            "Metros / (Brazos * Vp * 60)",
        ),
    ]

    filas_vol = [
        ("Factor de carga explosivo", "FC_P", 1.60, "kg/m³", "Norma túneles / Konya"),
        (
            "Consumo total de explosivo por avance",
            "KG_EXP_P",
            "={VOL_DISP_P}*{FC_P}",
            "kg",
            "Volumen * FC",
        ),
        (
            "Carga máxima por retardo",
            "Q_RET_P",
            32.0,
            "kg/retardo",
            "Disparo de ayudas/destroza",
        ),
        ("Constante de terreno roca dura (K)", "K_ROCA_P", 500, "-", "Criterio USBM"),
        ("Exponente de atenuación sísmica", "BETA_P", 1.60, "-", "Criterio USBM"),
        (
            "Distancia escalada a 20 m (SD)",
            "SD_20_P",
            "=20/SQRT({Q_RET_P})",
            "m/kg^0.5",
            "D / sqrt(Q)",
        ),
        (
            "Vibración Pico de Partícula a 20 m (PPV)",
            "PPV_20_P",
            "={K_ROCA_P}*({SD_20_P})^(-{BETA_P})",
            "mm/s",
            "K * SD^(-beta)",
        ),
    ]

    t1 = tabla_parametros(
        filas_geo, "Geometría de Excavación a Sección Plena (108.43 m²)"
    )
    t2 = tabla_parametros(
        filas_perf, "Malla de Perforación y Rendimiento del Jumbo 3 Brazos"
    )
    t3 = tabla_parametros(filas_vol, "Cálculo de Carga Explosiva y Vibraciones USBM")

    return Hoja(
        nombre="02_Seccion_Plena_Base",
        titulo="Detalle de Perforación y Voladura: Excavación a Sección Plena (Full Face)",
        tablas=[t1, t2, t3],
    )


def crear_hoja_calota_natm() -> Hoja:
    """Crea la hoja de parámetros detallados para la Fase 1: Calota Superior NATM."""
    filas_geo = [
        (
            "Ancho de la base de calota",
            "B_CAL",
            13.30,
            "m",
            "Ancho en plano de arranques",
        ),
        ("Altura de la calota (bóveda)", "H_CAL", 6.65, "m", "Radio R = B / 2"),
        (
            "Área de excavación de calota",
            "A_CAL",
            "=PI()*{B_CAL}^2/8",
            "m²",
            "Semicírculo superior pi*B^2/8",
        ),
        (
            "Porcentaje del área total del túnel",
            "PCT_A_CAL",
            "={A_CAL}/108.43",
            "%",
            "Área calota / 108.43 m²",
        ),
        (
            "Perímetro de bóveda expuesto (a sostener)",
            "P_CAL",
            "=PI()*{B_CAL}/2",
            "m",
            "Arco semicircular superior",
        ),
        (
            "Ancho de la plataforma provisional de trabajo",
            "BASE_CAL",
            13.30,
            "m",
            "Piso temporal de calota",
        ),
    ]

    filas_perf = [
        (
            "Taladros de alivio escariados Ø 102 mm",
            "N_ALIVIO_C",
            4,
            "und",
            "Cuñe quemado de calota",
        ),
        (
            "Taladros de cuele quemado Ø 45 mm",
            "N_CUELE_C",
            16,
            "und",
            "Apertura de cara libre",
        ),
        (
            "Taladros de ayudas de calota Ø 45 mm",
            "N_AYUDAS_C",
            20,
            "und",
            "Ampliación de cuele",
        ),
        (
            "Taladros de núcleo de calota Ø 45 mm",
            "N_NUCLEO_C",
            48,
            "und",
            "Bóveda superior",
        ),
        (
            "Taladros cuadradores superiores Ø 45 mm",
            "N_CUAD_C",
            8,
            "und",
            "Límites laterales",
        ),
        (
            "Taladros de corona (recorte) Ø 45 mm",
            "N_COR_C",
            42,
            "und",
            "Carga desacoplada 0.50m",
        ),
        (
            "Taladros de zapateras temporales Ø 45 mm",
            "N_ZAP_C",
            14,
            "und",
            "Piso provisional de calota",
        ),
        (
            "Total taladros cargados en calota",
            "N_CARGADOS_C",
            "={N_CUELE_C}+{N_AYUDAS_C}+{N_NUCLEO_C}+{N_CUAD_C}+{N_COR_C}+{N_ZAP_C}",
            "und",
            "Suma taladros cargados",
        ),
        (
            "Total taladros perforados en calota",
            "N_TOTAL_C",
            "={N_CARGADOS_C}+{N_ALIVIO_C}",
            "und",
            "Cargados + Alivio",
        ),
        (
            "Longitud del barreno de perforación",
            "LB_C",
            3.66,
            "m",
            "Barra Sandvik 12 ft",
        ),
        ("Eficiencia de avance", "EF_AV_C", 0.90, "%", "Efecto de cuñe quemado"),
        (
            "Avance efectivo por disparo",
            "AV_DISP_C",
            "={LB_C}*{EF_AV_C}",
            "m",
            "LB * Eficiencia",
        ),
        (
            "Volumen excavado por disparo en calota",
            "VOL_DISP_C",
            "={A_CAL}*{AV_DISP_C}",
            "m³",
            "Área * Avance",
        ),
        (
            "Metros lineales perforados en calota",
            "METROS_C",
            "={N_TOTAL_C}*{LB_C}",
            "m",
            "Taladros * LB",
        ),
        ("Número de brazos del Jumbo operando", "BRAZOS_C", 3, "und", "Sandvik DT1131"),
        (
            "Velocidad neta de penetración",
            "VP_C",
            1.50,
            "m/min",
            "Roca andesita RMR 55",
        ),
        (
            "Tiempo neto de perforación de calota",
            "T_PERF_C",
            "={METROS_C}/({BRAZOS_C}*{VP_C}*60)",
            "horas",
            "Metros / (Brazos * Vp * 60)",
        ),
    ]

    filas_vol = [
        (
            "Factor de carga explosivo en calota",
            "FC_C",
            1.45,
            "kg/m³",
            "Menor confinamiento base",
        ),
        (
            "Consumo total de explosivo por avance",
            "KG_EXP_C",
            "={VOL_DISP_C}*{FC_C}",
            "kg",
            "Volumen * FC",
        ),
        (
            "Carga máxima por retardo",
            "Q_RET_C",
            16.0,
            "kg/retardo",
            "50% menor que sección plena",
        ),
        ("Constante de terreno roca dura (K)", "K_ROCA_C", 500, "-", "Criterio USBM"),
        ("Exponente de atenuación sísmica", "BETA_C", 1.60, "-", "Criterio USBM"),
        (
            "Distancia escalada a 20 m (SD)",
            "SD_20_C",
            "=20/SQRT({Q_RET_C})",
            "m/kg^0.5",
            "D / sqrt(Q)",
        ),
        (
            "Vibración Pico de Partícula a 20 m (PPV)",
            "PPV_20_C",
            "={K_ROCA_C}*({SD_20_C})^(-{BETA_C})",
            "mm/s",
            "K * SD^(-beta)",
        ),
        (
            "Porcentaje de reducción de vibración frente a plena",
            "RED_PPV_C",
            "=(65.81-{PPV_20_C})/65.81",
            "%",
            "(PPV_plena - PPV_calota) / PPV_plena",
        ),
    ]

    t1 = tabla_parametros(
        filas_geo, "Geometría de la Fase 1: Calota Superior (Top Heading)"
    )
    t2 = tabla_parametros(filas_perf, "Malla de Perforación y Tiempos de Calota")
    t3 = tabla_parametros(filas_vol, "Carga Explosiva y Atenuación Sísmica en Calota")

    return Hoja(
        nombre="03_Calota_NATM",
        titulo="Fase 1: Calota Superior (Top Heading) según el Nuevo Método Austriaco",
        tablas=[t1, t2, t3],
    )


def crear_hoja_destroza_natm() -> Hoja:
    """Crea la hoja de parámetros detallados para la Fase 2: Destroza Inferior / Banco NATM."""
    filas_geo = [
        ("Ancho de la destroza", "B_DES", 13.30, "m", "Ancho entre hastiales"),
        ("Altura de la destroza", "H_DES", 2.93, "m", "Altura de hastial vertical"),
        (
            "Área de excavación de destroza",
            "A_DES",
            "={B_DES}*{H_DES}",
            "m²",
            "Rectángulo inferior B * Hw",
        ),
        (
            "Porcentaje del área total del túnel",
            "PCT_A_DES",
            "={A_DES}/108.43",
            "%",
            "Área destroza / 108.43 m²",
        ),
        (
            "Perímetro de excavación expuesto",
            "P_DES",
            "=2*{H_DES}+{B_DES}",
            "m",
            "2 hastiales + solera",
        ),
        (
            "Cara libre superior disponible",
            "CARA_LIBRE_D",
            13.30,
            "m",
            "Base abierta por la calota",
        ),
    ]

    filas_perf = [
        (
            "Taladros de alivio escariados Ø 102 mm",
            "N_ALIVIO_D",
            0,
            "und",
            "¡No requiere cuele quemado!",
        ),
        (
            "Taladros de banqueo fila superior Ø 45 mm",
            "N_BANQ_SUP_D",
            24,
            "und",
            "Salida hacia cara libre",
        ),
        (
            "Taladros de banqueo fila inferior Ø 45 mm",
            "N_BANQ_INF_D",
            24,
            "und",
            "Producción media",
        ),
        (
            "Taladros cuadradores (hastiales bajos) Ø 45 mm",
            "N_CUAD_D",
            8,
            "und",
            "Perfilado lateral",
        ),
        (
            "Taladros de zapateras definitivas Ø 45 mm",
            "N_ZAP_D",
            26,
            "und",
            "Nivel de rasante final",
        ),
        (
            "Total taladros de destroza (todos cargados)",
            "N_TOTAL_D",
            "={N_BANQ_SUP_D}+{N_BANQ_INF_D}+{N_CUAD_D}+{N_ZAP_D}",
            "und",
            "Suma total de taladros",
        ),
        (
            "Longitud del barreno de perforación",
            "LB_D",
            3.66,
            "m",
            "Barra Sandvik 12 ft",
        ),
        (
            "Eficiencia de avance (banqueo a cara libre)",
            "EF_AV_D",
            0.90,
            "%",
            "Salida abierta",
        ),
        (
            "Avance efectivo por disparo",
            "AV_DISP_D",
            "={LB_D}*{EF_AV_D}",
            "m",
            "LB * Eficiencia",
        ),
        (
            "Volumen excavado por disparo en destroza",
            "VOL_DISP_D",
            "={A_DES}*{AV_DISP_D}",
            "m³",
            "Área * Avance",
        ),
        (
            "Metros lineales perforados en destroza",
            "METROS_D",
            "={N_TOTAL_D}*{LB_D}",
            "m",
            "Taladros * LB",
        ),
        ("Número de brazos del Jumbo operando", "BRAZOS_D", 3, "und", "Sandvik DT1131"),
        (
            "Velocidad neta de penetración",
            "VP_D",
            1.50,
            "m/min",
            "Roca andesita RMR 55",
        ),
        (
            "Tiempo neto de perforación de destroza",
            "T_PERF_D",
            "={METROS_D}/({BRAZOS_D}*{VP_D}*60)",
            "horas",
            "Metros / (Brazos * Vp * 60)",
        ),
    ]

    filas_vol = [
        (
            "Factor de carga explosivo en destroza",
            "FC_D",
            1.15,
            "kg/m³",
            "Gran cara libre horizontal",
        ),
        (
            "Consumo total de explosivo por avance",
            "KG_EXP_D",
            "={VOL_DISP_D}*{FC_D}",
            "kg",
            "Volumen * FC",
        ),
        (
            "Carga máxima por retardo",
            "Q_RET_D",
            10.0,
            "kg/retardo",
            "Disparo por filas escalonadas",
        ),
        ("Constante de terreno roca dura (K)", "K_ROCA_D", 500, "-", "Criterio USBM"),
        ("Exponente de atenuación sísmica", "BETA_D", 1.60, "-", "Criterio USBM"),
        (
            "Distancia escalada a 20 m (SD)",
            "SD_20_D",
            "=20/SQRT({Q_RET_D})",
            "m/kg^0.5",
            "D / sqrt(Q)",
        ),
        (
            "Vibración Pico de Partícula a 20 m (PPV)",
            "PPV_20_D",
            "={K_ROCA_D}*({SD_20_D})^(-{BETA_D})",
            "mm/s",
            "K * SD^(-beta)",
        ),
        (
            "Porcentaje de ahorro de explosivo frente a plena",
            "AHORRO_EXP_D",
            "=(1.60-{FC_D})/1.60",
            "%",
            "(FC_plena - FC_destroza) / FC_plena",
        ),
    ]

    t1 = tabla_parametros(
        filas_geo, "Geometría de la Fase 2: Destroza Inferior (Bench)"
    )
    t2 = tabla_parametros(filas_perf, "Malla de Perforación y Tiempos de Destroza")
    t3 = tabla_parametros(filas_vol, "Carga Explosiva y Rendimiento Energético")

    return Hoja(
        nombre="04_Destroza_NATM",
        titulo="Fase 2: Destroza Inferior (Bench / Banqueo) según el Nuevo Método Austriaco",
        tablas=[t1, t2, t3],
    )


def crear_hoja_sostenimiento_natm() -> Hoja:
    """Crea la hoja con el diseño de soporte progresivo por etapas según NATM."""
    columnas = [
        "Etapa Constructiva NATM",
        "Momento de Aplicación",
        "Pernos de Anclaje (L=4m)",
        "Shotcrete con Fibra (mm)",
        "Cerchas de Acero",
        "Control de Convergencia",
    ]
    filas = [
        [
            "1. Sellado Inmediato de Calota",
            "0 - 30 min tras disparo y desatado",
            "—",
            "50 mm (sellado de fracturas)",
            "—",
            "Inspección visual del macizo",
        ],
        [
            "2. Soporte Primario de Calota",
            "1 - 2 horas tras desatado",
            "Sistemático radial @ 1.25 m",
            "150 mm adicional (e_total = 200 mm)",
            "Cercha HEB 140 / 3 celosías",
            "Instalación de pernos convergencia",
        ],
        [
            "3. Apoyo 'Pata de Elefante'",
            "Conexión arranque de calota",
            "2 pernos inclinados en el talón",
            "Engrosamiento a 250 mm en talón",
            "Apoyo sobre zapata provisional",
            "Monitoreo de asiento de arranques",
        ],
        [
            "4. Desfase Calota - Destroza",
            "Distancia L = 15 a 30 m",
            "—",
            "Fraguado completo (f'c >= 25 MPa)",
            "—",
            "Estabilización de deformación < 1 mm/día",
        ],
        [
            "5. Excavación de Destroza",
            "Tras estabilizar calota",
            "2 filas en hastiales bajos @ 1.25 m",
            "100 mm en hastiales verticales",
            "Prolongación pies derechos HEB",
            "Medición de convergencia en hastiales",
        ],
        [
            "6. Cierre de Anillo / Solera",
            "En roca Clase V (RMR <= 20)",
            "Pernos en radier invertido",
            "Contrabóveda de concreto e = 300 mm",
            "Cierre inferior del arco metálico",
            "Cese total de convergencia volumétrica",
        ],
    ]
    tabla = Tabla(
        columnas=columnas,
        filas=filas,
        titulo="Secuencia de Sostenimiento Progresivo por Etapas (NATM)",
    )
    return Hoja(
        nombre="05_Sostenimiento_NATM",
        titulo="Filosofía del Sostenimiento Progresivo y Cierre de Anillo según NATM",
        tablas=[tabla],
    )


def generar_libro_natm(ruta_salida: Path | None = None) -> Path:
    """Genera el libro Excel de pruebas NATM con todas sus hojas dinámicas."""
    if ruta_salida is None:
        carpeta_excel = RAIZ_PROYECTO / "salidas" / "excel"
    else:
        carpeta_excel = ruta_salida.parent

    libro = Libro(
        archivo="Prueba_NATM_Seccion_Dividida.xlsx"
        if ruta_salida is None
        else ruta_salida.name,
        hojas=[
            crear_hoja_comparativa(),
            crear_hoja_seccion_plena(),
            crear_hoja_calota_natm(),
            crear_hoja_destroza_natm(),
            crear_hoja_sostenimiento_natm(),
        ],
    )

    return escribir_libro(
        libro=libro,
        carpeta=carpeta_excel,
        proyecto="Túnel Casmas Huaraz PA14 · Estudio de Excavación por Secciones (NATM)",
    )


def main() -> None:
    """Punto de entrada de prueba."""
    print("=" * 80)
    print(" GENERADOR DE CÁLCULO: EXCAVACIÓN POR SECCIONES (CALOTA Y DESTROZA) NATM")
    print(" Proyecto: Túnel Casmas Huaraz PA14")
    print("=" * 80)

    ruta = generar_libro_natm()
    print("\n[OK] Libro Excel generado exitosamente:")
    print(f" -> {ruta.resolve()}")
    print("\nHojas incluidas con fórmulas nativas dinámicas:")
    print(
        " 1. 01_Comparativa_Metodos   : Resumen comparativo directo (Plena vs. Calota + Destroza)"
    )
    print(
        " 2. 02_Seccion_Plena_Base    : Detalle sección plena (108.43 m², 231 taladros, FC 1.60)"
    )
    print(
        " 3. 03_Calota_NATM           : Fase 1 Calota superior (69.46 m², 152 taladros, FC 1.45)"
    )
    print(
        " 4. 04_Destroza_NATM         : Fase 2 Destroza inferior (38.97 m², 82 taladros, FC 1.15)"
    )
    print(
        " 5. 05_Sostenimiento_NATM    : Secuencia de sostenimiento progresivo y cierre de anillo"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
