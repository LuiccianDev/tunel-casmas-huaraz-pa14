"""12 - Voladura (Metodo de C. Konya).

Calcula y formula dinamicamente los parametros de perforacion y voladura.
"""

from typing import Any

from ..modelo import Hoja, Libro, tabla_parametros

CLAVE = "voladura"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    vol = p["voladura"]
    sge = float(vol["densidad_explosivo_g_cm3"])
    sgr = float(vol["densidad_roca_g_cm3"])
    de_mm = float(vol["diametro_explosivo_mm"])
    h = float(vol["altura_banco_m"])
    th_factor = float(vol["constante_retardo_ms_m"])
    tr_factor = float(vol["factor_tiempo_filas_ms_m"])

    if "geologia" in ctx and ctx["geologia"]["tramos"]:
        primer_tramo = ctx["geologia"]["tramos"][0]
        if isinstance(primer_tramo, dict) and "densidad_t_m3" in primer_tramo:
            sgr = float(primer_tramo["densidad_t_m3"])

    # Formulas Konya en Python
    burden_m = 0.012 * ((2.0 * (sge / sgr)) + 1.5) * de_mm
    espaciamiento_m = 1.4 * burden_m
    sobre_perf_m = 0.3 * burden_m
    taco_m = 0.7 * burden_m
    rigidez = h / burden_m if burden_m > 0 else 0.0
    longitud_taladro_m = h + sobre_perf_m
    vol_romper_m3 = burden_m * espaciamiento_m * h
    de_cm = de_mm / 10.0
    qbk_kg_m = 0.078539 * sge * (de_cm**2)

    carga_fondo_m = 1.3 * burden_m
    carga_columna_m = max(0.0, longitud_taladro_m - (carga_fondo_m + taco_m))
    if carga_columna_m == 0:
        carga_fondo_m = max(0.0, longitud_taladro_m - taco_m)

    carga_total_kg = (carga_fondo_m + carga_columna_m) * qbk_kg_m
    factor_carga_kg_m3 = carga_total_kg / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    toneladas_romper = vol_romper_m3 * sgr
    factor_potencia_kg_tm = (
        carga_total_kg / toneladas_romper if toneladas_romper > 0 else 0.0
    )
    retardo_barrenos_ms = th_factor * espaciamiento_m
    retardo_filas_ms = tr_factor * burden_m
    perf_especifica_m_m3 = (
        longitud_taladro_m / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    )

    return {
        "inputs": {
            "sge": sge,
            "sgr": sgr,
            "de_mm": de_mm,
            "h": h,
            "th_factor": th_factor,
            "tr_factor": tr_factor,
        },
        "calculados": {
            "burden_m": burden_m,
            "espaciamiento_m": espaciamiento_m,
            "sobre_perf_m": sobre_perf_m,
            "taco_m": taco_m,
            "rigidez": rigidez,
            "longitud_taladro_m": longitud_taladro_m,
            "vol_romper_m3": vol_romper_m3,
            "qbk_kg_m": qbk_kg_m,
            "carga_fondo_m": carga_fondo_m,
            "carga_columna_m": carga_columna_m,
            "carga_total_kg": carga_total_kg,
            "factor_carga_kg_m3": factor_carga_kg_m3,
            "factor_potencia_kg_tm": factor_potencia_kg_tm,
            "retardo_barrenos_ms": retardo_barrenos_ms,
            "retardo_filas_ms": retardo_filas_ms,
            "perf_especifica_m_m3": perf_especifica_m_m3,
        },
    }


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    inp = resultados["inputs"]

    # Generamos la tabla estandar con formulas vivas de Excel usando simbolos {Simbolo}
    # excel.py se encarga de resolver automaticamente {Simbolo} a su celda real (ej. C6, C10, etc.)
    filas = [
        ("Densidad del explosivo", "Sge", inp["sge"], "g/cm³", "TOML [voladura]"),
        ("Densidad de la roca", "Sgr", inp["sgr"], "g/cm³", "02_Geologia / TOML"),
        ("Diámetro del explosivo", "De", inp["de_mm"], "mm", "TOML [voladura]"),
        ("Altura de banco", "H", inp["h"], "m", "Diseño de banco"),
        (
            "Burden de diseño",
            "B",
            "=0.012*((2*({Sge}/{Sgr}))+1.5)*{De}",
            "m",
            "B = 0.012 * [(2 * (Sge / Sgr)) + 1.5] * De",
        ),
        ("Espaciamiento", "S", "=1.4*{B}", "m", "S = 1.4 * B"),
        ("Sobreperforación (Pasadura)", "J", "=0.3*{B}", "m", "J = 0.3 * B"),
        ("Taco o retacado", "T", "=0.7*{B}", "m", "T = 0.7 * B"),
        ("Relación de rigidez", "H/B", "={H}/{B}", "-", "H / B (>= 4 óptimo)"),
        ("Longitud de taladro", "L", "={H}+{J}", "m", "L = H + J"),
        (
            "Volumen a romper por taladro",
            "V",
            "={B}*{S}*{H}",
            "m³/tal",
            "V = B * S * H",
        ),
        (
            "Concentración lineal de carga",
            "Qbk",
            "=0.078539*{Sge}*({De}/10)^2",
            "kg/m",
            "Qbk = 0.078539 * Sge * (De/10)²",
        ),
        ("Longitud carga de fondo", "Cf", "=1.3*{B}", "m", "Cf = 1.3 * B"),
        (
            "Longitud carga de columna",
            "Cc",
            "=MAX(0, {L}-({Cf}+{T}))",
            "m",
            "Cc = L - (Cf + T)",
        ),
        (
            "Carga total por taladro",
            "Qt",
            "=({Cf}+{Cc})*{Qbk}",
            "kg/tal",
            "Qt = (Cf + Cc) * Qbk",
        ),
        (
            "Factor de Carga",
            "FC",
            "={Qt}/{V}",
            "kg/m³",
            "FC = Qt / V",
        ),
        (
            "Factor de Potencia",
            "FP",
            "={Qt}/({V}*{Sgr})",
            "kg/TM",
            "FP = Qt / (V * Sgr)",
        ),
        (
            "Constante retardo barrenos",
            "Th",
            inp["th_factor"],
            "ms/m",
            "López Jimeno / Konya (Tabla Roca)",
        ),
        ("Retardo barreno a barreno", "th", "={Th}*{S}", "ms", "th = Th * S"),
        (
            "Factor tiempo entre filas",
            "TR",
            inp["tr_factor"],
            "ms/m",
            "Konya (Pila promedio)",
        ),
        ("Retardo entre filas", "tR", "={TR}*{B}", "ms", "tR = TR * B"),
        ("Perforación específica", "PE", "={L}/{V}", "m/m³", "PE = L / V"),
    ]

    return Libro(
        archivo="12_Voladura.xlsx",
        hojas=[
            Hoja(
                nombre="Voladura_Konya",
                titulo="Diseño de Voladura y Estimación de Cargas (Método C. Konya)",
                tablas=[tabla_parametros(filas, "Parámetros y Cálculos de Voladura")],
            )
        ],
    )
