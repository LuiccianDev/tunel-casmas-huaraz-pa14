"""02 - Geologia y Q-Slope.

Calcula la clasificacion geomecanica y estabilidad de taludes mediante Q-Slope.
Formula: Q_slope = (RQD / Jn) * (Jr / Ja) * (Jw / SRF)
"""

from typing import Any

from ..modelo import Hoja, Libro, Tabla

CLAVE = "geologia"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    tramos_raw = p.get("geologia", {}).get("tramos", [])
    tramos_calculados = []

    for t in tramos_raw:
        rqd = float(t.get("rqd", 50.0))
        jn = float(t.get("jn", 9.0))
        jr = float(t.get("jr", 1.5))
        ja = float(t.get("ja", 3.0))
        jw = float(t.get("jw", 1.0))
        srf = float(t.get("srf", 2.5))

        q_slope = (
            (rqd / jn) * (jr / ja) * (jw / srf)
            if (jn > 0 and ja > 0 and srf > 0)
            else 0.0
        )

        tramos_calculados.append(
            {
                "progresiva_inicio": t.get("progresiva_inicio", 0.0),
                "progresiva_fin": t.get("progresiva_fin", 0.0),
                "tipo_roca": t.get("tipo_roca", ""),
                "densidad_t_m3": t.get("densidad_t_m3", 2.5),
                "esponjamiento": t.get("esponjamiento", 1.3),
                "rmr": t.get("rmr", 50),
                "rqd": rqd,
                "jn": jn,
                "jr": jr,
                "ja": ja,
                "jw": jw,
                "srf": srf,
                "q_slope": round(q_slope, 4),
                "descripcion": t.get("descripcion", ""),
            }
        )

    return {"tramos": tramos_calculados}


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    cols = [
        "Prog. Inicio (m)",
        "Prog. Fin (m)",
        "Tipo de Roca",
        "Densidad (t/m³)",
        "Esponjamiento",
        "RMR",
        "RQD (%)",
        "Jn",
        "Jr",
        "Ja",
        "Jw",
        "SRF",
        "Q-Slope (Calc)",
        "Q-Slope (Fórmula Excel)",
        "Descripción",
    ]
    filas = []
    # Fila inicial de datos en Excel: Tabla inicia en fila 4 (fila 4 = encabezado, fila 5 = primer dato)
    fila_actual = 5
    for t in resultados["tramos"]:
        # Columnas en Excel:
        # A: Prog. Inicio, B: Prog. Fin, C: Tipo Roca, D: Densidad, E: Esponjamiento, F: RMR
        # G: RQD, H: Jn, I: Jr, J: Ja, K: Jw, L: SRF, M: Q-Slope valor, N: Q-Slope Formula
        formula_excel = f"=(G{fila_actual}/H{fila_actual})*(I{fila_actual}/J{fila_actual})*(K{fila_actual}/L{fila_actual})"
        filas.append(
            [
                t["progresiva_inicio"],
                t["progresiva_fin"],
                t["tipo_roca"],
                t["densidad_t_m3"],
                t["esponjamiento"],
                t["rmr"],
                t["rqd"],
                t["jn"],
                t["jr"],
                t["ja"],
                t["jw"],
                t["srf"],
                t["q_slope"],
                formula_excel,
                t["descripcion"],
            ]
        )
        fila_actual += 1

    if not filas:
        filas = [["No hay datos"] + [""] * 14]

    return Libro(
        archivo="02_Geologia.xlsx",
        hojas=[
            Hoja(
                nombre="Tramos_Geologicos",
                titulo="Zonificación Geomecánica y Q-Slope (5.6 km)",
                tablas=[Tabla(cols, filas)],
            )
        ],
    )
