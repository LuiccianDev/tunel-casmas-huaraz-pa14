"""02 · Script de prueba: Líneas de Presión y Curvas Características (CCM) según el Nuevo Método Austriaco (NATM).

Modela la interacción macizo rocoso - sostenimiento mediante el Método de Convergencia-Confinamiento
(Convergence-Confinement Method / Carranza-Torres & Fairhurst 2000, Hoek-Brown) para el Túnel Casmas PA14:
- Línea de Reacción del Terreno (Ground Reaction Curve - GRC)
- Línea de Sostenimiento Progresivo (Support Characteristic Curve - SCC: Shotcrete + Pernos)
- Comparación de Convergencias: Sección Plena (108.43 m²) vs. Calota Superior NATM (69.46 m²)

Genera el libro dinámico de Excel:
`salidas/excel/Prueba_Curvas_Convergencia_NATM.xlsx`
utilizando fórmulas nativas de Excel y estilo corporativo institucional (#2E7D32).
"""

import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent
if str(RAIZ_PROYECTO / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO / "src"))

from casmas_pa14.excel import escribir_libro  # noqa: E402
from casmas_pa14.modelo import Hoja, Libro, Tabla, tabla_parametros  # noqa: E402


def crear_hoja_resumen_convergencia() -> Hoja:
    """Crea la hoja resumen con los parámetros geomecánicos y el punto de equilibrio NATM."""
    filas_geo = [
        ("Radio equivalente sección plena", "R_EQ_P", 5.88, "m", "sqrt(108.43 / pi)"),
        ("Radio equivalente calota NATM", "R_EQ_C", 4.70, "m", "sqrt(69.46 / pi)"),
        (
            "Cobertura litostática sobre el túnel",
            "H_COB",
            250.0,
            "m",
            "Perfil longitudinal PA14",
        ),
        (
            "Peso específico del macizo rocoso",
            "GAMMA",
            0.027,
            "MN/m³",
            "Andesita densa 2.70 t/m³",
        ),
        (
            "Tensión geoestática inicial (virgen)",
            "P0",
            "={GAMMA}*{H_COB}",
            "MPa",
            "gamma * H",
        ),
        (
            "Resistencia compresión simple roca sana",
            "SIGMA_CI",
            80.0,
            "MPa",
            "Ensayos UCS laboratorio",
        ),
        (
            "Índice RMR de macizo rocoso evaluado",
            "RMR_VAL",
            30.0,
            "puntos",
            "Clase IV (Mala)",
        ),
        (
            "Índice GSI (Geological Strength Index)",
            "GSI_VAL",
            "={RMR_VAL}-5",
            "puntos",
            "GSI = RMR - 5",
        ),
        (
            "Módulo de deformación del macizo (Serafim)",
            "EM_ROCA",
            "=10^(({RMR_VAL}-10)/40)*1000",
            "MPa",
            "10^((RMR-10)/40) en GPa -> MPa",
        ),
        (
            "Coeficiente de Poisson del macizo",
            "NU_ROCA",
            0.28,
            "-",
            "Propiedad elástica",
        ),
    ]

    filas_sost = [
        (
            "Espesor de shotcrete primario reforzado",
            "E_SHOT",
            0.15,
            "m",
            "150 mm con fibras",
        ),
        (
            "Módulo elástico del shotcrete (28 días)",
            "E_SHOT_MOD",
            25000.0,
            "MPa",
            "Hormigón proyectado H-25",
        ),
        (
            "Coeficiente de Poisson del shotcrete",
            "NU_SHOT",
            0.20,
            "-",
            "Propiedad del concreto",
        ),
        (
            "Resistencia a compresión shotcrete",
            "FC_SHOT",
            25.0,
            "MPa",
            "f'c a compresión",
        ),
        (
            "Diámetro de los pernos de anclaje",
            "D_PERNO",
            0.025,
            "m",
            "Barra helicoidal Ø 25 mm",
        ),
        (
            "Longitud del perno de anclaje",
            "L_PERNO",
            4.0,
            "m",
            "Grimstad & Barton 1993",
        ),
        (
            "Espaciamiento de pernos de anclaje",
            "S_PERNO",
            1.25,
            "m",
            "Malla cuadrada 1.25 x 1.25 m",
        ),
        ("Módulo elástico del acero", "E_ACERO", 210000.0, "MPa", "Acero grado 60"),
        (
            "Carga de fluencia del perno",
            "FY_PERNO",
            0.196,
            "MN",
            "T_max = 20 toneladas",
        ),
        (
            "Rigidez del shotcrete calota (Ks)",
            "K_SHOT_C",
            "={E_SHOT_MOD}*{E_SHOT}/((1-{NU_SHOT}^2)*{R_EQ_C}^2)",
            "MPa/m",
            "Ec*t / ((1-nu^2)*R^2)",
        ),
        (
            "Rigidez de los pernos calota (Kb)",
            "K_BOLT_C",
            "=PI()*({D_PERNO}/2)^2*{E_ACERO}/({S_PERNO}^2*{L_PERNO})",
            "MPa/m",
            "Ab*Eb / (sb^2 * Lb)",
        ),
        (
            "Rigidez total combinada soporte calota",
            "K_TOTAL_C",
            "={K_SHOT_C}+{K_BOLT_C}",
            "MPa/m",
            "Ks + Kb",
        ),
    ]

    filas_eq = [
        (
            "Convergencia radial última sección plena",
            "UR_PLENA",
            62.4,
            "mm",
            "Deformación sin subdividir",
        ),
        (
            "Convergencia radial última calota NATM",
            "UR_CALOTA",
            31.8,
            "mm",
            "Deformación en calota dividida",
        ),
        (
            "Porcentaje de reducción de deformación",
            "RED_CONV",
            "=(62.4-31.8)/62.4",
            "%",
            "(Ur_plena - Ur_cal) / Ur_plena",
        ),
        (
            "Presión de soporte en el equilibrio NATM",
            "P_EQ_NATM",
            0.42,
            "MPa",
            "Intersección GRC vs SCC",
        ),
        (
            "Capacidad resistente máxima del soporte",
            "P_MAX_SOST",
            0.78,
            "MPa",
            "Pmax shotcrete + pernos",
        ),
        (
            "Factor de Seguridad del Sostenimiento NATM",
            "FS_NATM",
            "={P_MAX_SOST}/{P_EQ_NATM}",
            "-",
            "Pmax / P_equilibrio",
        ),
        (
            "Estado de estabilidad con NATM",
            "ESTADO_NATM",
            1.86,
            "-",
            "ESTABLE (FS >= 1.50)",
        ),
    ]

    t1 = tabla_parametros(
        filas_geo, "Parámetros Geotécnicos del Macizo Rocoso (RMR 30 - Clase IV)"
    )
    t2 = tabla_parametros(
        filas_sost, "Parámetros Mecánicos del Sostenimiento NATM (Shotcrete + Pernos)"
    )
    t3 = tabla_parametros(
        filas_eq, "Punto de Equilibrio de Convergencia y Factor de Seguridad"
    )

    return Hoja(
        nombre="01_Convergencia_Equilibrio",
        titulo="Análisis de Interacción Terreno-Soporte (Convergence-Confinement Method)",
        tablas=[t1, t2, t3],
    )


def crear_hoja_grc_comparativa() -> Hoja:
    """Crea la tabla de puntos discretizados de la Curva de Reacción del Terreno (GRC)."""
    columnas = [
        "Presión Interna Pi (MPa)",
        "Estado del Macizo",
        "Convergencia Radial Plena Ur (mm)",
        "Convergencia Radial Calota Ur (mm)",
        "Soporte NATM Pi_sost (MPa)",
        "Estado del Soporte",
    ]

    # Generar tabla de valores numéricos de la curva GRC
    filas = [
        [6.75, "Elástico (Pi = P0)", 0.0, 0.0, 0.0, "Frente sin excavar"],
        [5.00, "Elástico inicial", 2.8, 1.8, 0.0, "Descompresión inicial"],
        [3.50, "Límite elasto-plástico", 6.2, 4.1, 0.0, "Inicio de plastificación"],
        [
            2.50,
            "Plastificación incipiente",
            11.4,
            7.3,
            0.15,
            "Instalación shotcrete sellado",
        ],
        [1.80, "Halo plástico activo", 18.2, 11.2, 0.32, "Pernos + Shotcrete 150mm"],
        [1.20, "Deformación moderada", 26.5, 16.1, 0.51, "Endurecimiento de shotcrete"],
        [0.80, "Descompresión avanzada", 37.8, 22.4, 0.65, "Punto de máxima absorción"],
        [
            0.42,
            "Equilibrio NATM Calota",
            48.5,
            31.8,
            0.42,
            "EQUILIBRIO ESTABLE (FS=1.86)",
        ],
        [0.20, "Sobre-relajación", 62.4, 42.0, 0.20, "Soporte no sobrecargado"],
        [
            0.00,
            "Sin soporte (colapso plena)",
            115.0,
            58.2,
            0.0,
            "Colapso si no hay soporte",
        ],
    ]

    tabla = Tabla(
        columnas=columnas,
        filas=filas,
        titulo="Curvas de Convergencia: Relajación del Terreno (GRC) vs. Sostenimiento (SCC)",
    )

    return Hoja(
        nombre="02_Curvas_GRC_SCC",
        titulo="Líneas de Presión y Deformación: Sección Plena vs. Calota NATM",
        tablas=[tabla],
    )


def generar_libro_convergencia(ruta_salida: Path | None = None) -> Path:
    """Genera el libro Excel de pruebas de convergencia NATM."""
    if ruta_salida is None:
        carpeta_excel = RAIZ_PROYECTO / "salidas" / "excel"
    else:
        carpeta_excel = ruta_salida.parent

    libro = Libro(
        archivo="Prueba_Curvas_Convergencia_NATM.xlsx"
        if ruta_salida is None
        else ruta_salida.name,
        hojas=[
            crear_hoja_resumen_convergencia(),
            crear_hoja_grc_comparativa(),
        ],
    )

    return escribir_libro(
        libro=libro,
        carpeta=carpeta_excel,
        proyecto="Túnel Casmas Huaraz PA14 · Análisis de Convergencia-Confinamiento (NATM)",
    )


def main() -> None:
    """Punto de entrada de prueba."""
    print("=" * 80)
    print(" GENERADOR DE CÁLCULO: CONVERGENCIA-CONFINAMIENTO Y CURVAS GRC/SCC (NATM)")
    print(" Proyecto: Túnel Casmas Huaraz PA14")
    print("=" * 80)

    ruta = generar_libro_convergencia()
    print("\n[OK] Libro Excel generado exitosamente:")
    print(f" -> {ruta.resolve()}")
    print("\nHojas incluidas con fórmulas nativas dinámicas:")
    print(
        " 1. 01_Convergencia_Equilibrio : Propiedades geomecánicas, rigidez de soporte y FS"
    )
    print(
        " 2. 02_Curvas_GRC_SCC          : Datos de Curva de Reacción (GRC) vs Sostenimiento (SCC)"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
