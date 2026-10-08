"""13 · Sostenimiento: Cálculo de pernos, shotcrete y cerchas según RMR y Q-Barton."""

import math

from ..modelo import Hoja, Libro, Tabla

CLAVE = "sostenimiento"


def calcular(p: dict, ctx: dict) -> dict:
    s = p["sostenimiento"]
    sec = p["seccion"]
    tramos_geo = ctx["geologia"]["tramos"]

    ancho_b = sec["ancho_m"]
    esr = s["esr"]
    diam_e = ancho_b / esr

    # Longitud empírica de pernos (Grimstad & Barton)
    longitud_perno = 2.0 + 0.15 * ancho_b / esr
    # Redondear a medio metro más cercano
    longitud_perno = math.ceil(longitud_perno * 2) / 2

    tramos_sost = []

    for t in tramos_geo:
        rmr = t["rmr"]
        q = t["q_slope"]

        # Bieniawski (1989) simplificado para túnel B ~ 10-13m
        if rmr > 80:
            clase = "I (Muy Buena)"
            tipo_soporte = "Ninguno / Desate localizado"
            esp_pernos = 0.0
            esp_shotcrete = 0.0
            cerchas = "No"
        elif rmr > 60:
            clase = "II (Buena)"
            tipo_soporte = "Pernos puntuales"
            esp_pernos = 2.5
            esp_shotcrete = 50.0
            cerchas = "No"
        elif rmr > 40:
            clase = "III (Regular)"
            tipo_soporte = "Pernos sistemáticos + Shotcrete"
            esp_pernos = 1.75
            esp_shotcrete = 100.0
            cerchas = "No"
        elif rmr > 20:
            clase = "IV (Mala)"
            tipo_soporte = "Pernos sistemáticos + Shotcrete + Cerchas ligeras"
            esp_pernos = 1.25
            esp_shotcrete = 150.0
            cerchas = "Ligeras @ 1.5m"
        else:
            clase = "V (Muy Mala)"
            tipo_soporte = "Pernos sistemáticos + Shotcrete + Cerchas pesadas"
            esp_pernos = 1.0
            esp_shotcrete = 200.0
            cerchas = "Pesadas @ 0.75m"

        tramos_sost.append(
            {
                "prog_ini": t["progresiva_inicio"],
                "prog_fin": t["progresiva_fin"],
                "longitud": t["progresiva_fin"] - t["progresiva_inicio"],
                "tipo_roca": t["tipo_roca"],
                "rmr": rmr,
                "q": q,
                "clase": clase,
                "soporte": tipo_soporte,
                "long_perno": longitud_perno if rmr <= 80 else 0.0,
                "esp_pernos": esp_pernos,
                "esp_shotcrete": esp_shotcrete,
                "cerchas": cerchas,
            }
        )

    return {
        "esr": esr,
        "De": diam_e,
        "long_perno_teorico": longitud_perno,
        "tramos": tramos_sost,
    }


def libro(r: dict, p: dict) -> Libro:
    filas = []
    for t in r["tramos"]:
        filas.append(
            [
                t["prog_ini"],
                t["prog_fin"],
                t["longitud"],
                t["tipo_roca"],
                t["rmr"],
                t["q"],
                t["clase"],
                t["soporte"],
                t["long_perno"],
                t["esp_pernos"],
                t["esp_shotcrete"],
                t["cerchas"],
            ]
        )

    tabla_sost = Tabla(
        [
            "Prog. Ini (m)",
            "Prog. Fin (m)",
            "Longitud (m)",
            "Litología",
            "RMR",
            "Q-Barton",
            "Clase Geomecánica",
            "Tipo de Soporte",
            "Long. Perno (m)",
            "Espaciado Pernos (m)",
            "Shotcrete (mm)",
            "Cerchas Metálicas",
        ],
        filas,
        "Diseño de Sostenimiento por Tramo (Bieniawski & Barton)",
    )

    return Libro(
        "13_Sostenimiento.xlsx",
        [Hoja("Sostenimiento", "Cálculo de Sostenimiento", [tabla_sost])],
    )
