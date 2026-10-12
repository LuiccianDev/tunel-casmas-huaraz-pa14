"""02 - Geologia y Q-Slope.

Calcula la clasificacion geomecanica y estabilidad de taludes mediante Q-Slope.
Formula: Q_slope = (RQD / Jn) * (Jr / Ja) * (Jw / SRF)
"""

from typing import Any

from ..modelo import Hoja, Libro, Tabla

CLAVE = "geologia"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    tramos_raw = p["geologia"]["tramos"]
    tramos_calculados = []

    for t in tramos_raw:
        rqd = float(t["rqd"])
        jn = float(t["jn"])
        jr = float(t["jr"])
        ja = float(t["ja"])
        jw = float(t["jw"])
        srf = float(t["srf"])

        q_slope = (
            (rqd / jn) * (jr / ja) * (jw / srf)
            if (jn > 0 and ja > 0 and srf > 0)
            else 0.0
        )

        tramos_calculados.append(
            {
                "progresiva_inicio": float(t["progresiva_inicio"]),
                "progresiva_fin": float(t["progresiva_fin"]),
                "longitud_m": float(t["progresiva_fin"])
                - float(t["progresiva_inicio"]),
                "tipo_roca": str(t["tipo_roca"]),
                "densidad_t_m3": float(t["densidad_t_m3"]),
                "esponjamiento": float(t["esponjamiento"]),
                "rmr": int(t["rmr"]),
                "rqd": rqd,
                "jn": jn,
                "jr": jr,
                "ja": ja,
                "jw": jw,
                "srf": srf,
                "q_slope": round(q_slope, 4),
                "descripcion": str(t["descripcion"]),
            }
        )

    return {"tramos": tramos_calculados}


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    cols = [
        "Prog. Inicio (m)",
        "Prog. Fin (m)",
        "Longitud (m)",
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
        "Q-Slope",
        "Descripción",
    ]
    filas = []
    # Tabla sin subtítulo: encabezado en fila 4, primer dato en fila 5
    fila_ini = 5
    fila_actual = fila_ini
    for t in resultados["tramos"]:
        f_long = f"=B{fila_actual}-A{fila_actual}"
        f_q = f"=(H{fila_actual}/I{fila_actual})*(J{fila_actual}/K{fila_actual})*(L{fila_actual}/M{fila_actual})"
        filas.append(
            [
                t["progresiva_inicio"],
                t["progresiva_fin"],
                f_long,
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
                f_q,
                t["descripcion"],
            ]
        )
        fila_actual += 1

    if resultados["tramos"]:
        fila_fin = fila_actual - 1
        filas.append(
            [
                "TOTAL LONGITUD",
                "",
                f"=SUM(C{fila_ini}:C{fila_fin})",
                "",
                f"=AVERAGE(E{fila_ini}:E{fila_fin})",
                f"=AVERAGE(F{fila_ini}:F{fila_fin})",
                f"=AVERAGE(G{fila_ini}:G{fila_fin})",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "Longitud total y promedios ponderables del perfil",
            ]
        )
    else:
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
