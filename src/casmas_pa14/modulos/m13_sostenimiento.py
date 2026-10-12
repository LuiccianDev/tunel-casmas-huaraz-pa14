"""13 · Sostenimiento: Sostenimiento Subterráneo Longitudinal del Túnel (Bieniawski 1989 y Q de Barton).

Calcula el diseño de soporte interno por tramo geomecánico a lo largo de los 5,556.08 m
del túnel (longitud empírica de pernos según Grimstad & Barton, espaciamiento de pernos,
espesor de shotcrete y cerchas metálicas).
"""

import math
from typing import Any

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "sostenimiento"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula el sostenimiento subterráneo longitudinal por tramo geomecánico."""
    s = p.get("sostenimiento", {})
    sec_p = p.get("seccion", {})
    sec_ctx = ctx.get("seccion", {})
    tramos_geo = ctx.get("geologia", {}).get("tramos", [])
    clases_rmr = s.get("clases_rmr", [])

    ancho_b = float(sec_ctx.get("ancho_m", sec_p.get("ancho_m", 13.30)))
    esr = float(s.get("esr", 1.0))
    diam_e = ancho_b / esr if esr > 0 else ancho_b

    # Longitud empírica de pernos subterráneos (Grimstad & Barton 1993)
    longitud_perno = 2.0 + 0.15 * ancho_b / esr
    longitud_perno = math.ceil(longitud_perno * 2.0) / 2.0

    tramos_sost = []
    for t in tramos_geo:
        rmr = t["rmr"]
        q = t["q_slope"]

        regla = next(
            (c for c in clases_rmr if rmr > c["rmr_min"]),
            {
                "clase": "V (Muy Mala)",
                "soporte": "Pernos sistemáticos + Shotcrete + Cerchas pesadas",
                "esp_pernos_m": 1.0,
                "shotcrete_mm": 200.0,
                "cerchas": "Pesadas @ 0.75m",
            },
        )

        tramos_sost.append(
            {
                "prog_ini": t["progresiva_inicio"],
                "prog_fin": t["progresiva_fin"],
                "longitud": t["progresiva_fin"] - t["progresiva_inicio"],
                "tipo_roca": t["tipo_roca"],
                "rmr": rmr,
                "q": q,
                "clase": regla["clase"],
                "soporte": regla["soporte"],
                "long_perno": longitud_perno if rmr <= 80 else 0.0,
                "esp_pernos": regla["esp_pernos_m"],
                "esp_shotcrete": regla["shotcrete_mm"],
                "cerchas": regla["cerchas"],
            }
        )

    return {
        "ancho_b": ancho_b,
        "esr": esr,
        "De": diam_e,
        "long_perno_teorico": longitud_perno,
        "tramos": tramos_sost,
    }


def libro(r: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 13_Sostenimiento.xlsx para el soporte subterráneo del túnel."""
    param_barton = tabla_parametros(
        [
            (
                "Ancho de excavación del túnel (03_Seccion)",
                "B_tun",
                r["ancho_b"],
                "m",
                "03_Seccion",
            ),
            (
                "Relación de soporte de excavación (ESR)",
                "ESR_tun",
                r["esr"],
                "-",
                "Grimstad & Barton (1993)",
            ),
            (
                "Diámetro equivalente de excavación",
                "De_tun",
                "={B_tun}/{ESR_tun}",
                "m",
                "De = B / ESR",
            ),
            (
                "Longitud teórica de perno sistemático",
                "L_perno",
                "=CEILING(2+0.15*{B_tun}/{ESR_tun}, 0.5)",
                "m",
                "L = 2 + 0.15 · B / ESR (redondeado a 0.5 m)",
            ),
        ],
        "Parámetros de Dimensionamiento de Pernos (Grimstad & Barton 1993)",
    )

    fila_ini = 12
    filas_tramos = []
    for i, t in enumerate(r["tramos"]):
        fa = fila_ini + i
        filas_tramos.append(
            [
                t["prog_ini"],
                t["prog_fin"],
                f"=B{fa}-A{fa}",
                t["tipo_roca"],
                t["rmr"],
                t["q"],
                f'=IF(E{fa}>80,"I (Muy Buena)",IF(E{fa}>60,"II (Buena)",IF(E{fa}>40,"III (Regular)",IF(E{fa}>20,"IV (Mala)","V (Muy Mala)"))))',
                t["soporte"],
                f"=IF(E{fa}>80, 0, $C$9)",
                f"=IF(E{fa}>80, 0, IF(E{fa}>60, 2.5, IF(E{fa}>40, 1.75, IF(E{fa}>20, 1.25, 1.0))))",
                f"=IF(E{fa}>80, 0, IF(E{fa}>60, 50, IF(E{fa}>40, 100, IF(E{fa}>20, 150, 200))))",
                t["cerchas"],
            ]
        )

    fila_fin = fila_ini + len(r["tramos"]) - 1
    filas_tramos.append(
        [
            "TOTAL",
            "",
            f"=SUM(C{fila_ini}:C{fila_fin})",
            "",
            f"=AVERAGE(E{fila_ini}:E{fila_fin})",
            f"=AVERAGE(F{fila_ini}:F{fila_fin})",
            "",
            "",
            "",
            "",
            "",
            "",
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
        filas_tramos,
        "Diseño de Sostenimiento Subterráneo por Tramo (Bieniawski 1989 & Barton Q)",
    )

    return Libro(
        "13_Sostenimiento.xlsx",
        [
            Hoja(
                "Sostenimiento",
                "Diseño de Sostenimiento Subterráneo por Tramo (Bieniawski 1989 & Barton Q)",
                [param_barton, tabla_sost],
            ),
        ],
    )


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 13_Sostenimiento.md del soporte subterráneo interior."""
    filas_tramos = [
        [
            f"{t['prog_ini']:.0f} - {t['prog_fin']:.0f}",
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
        for t in r["tramos"]
    ]
    t_sost_tunel = Tabla(
        [
            "Progresiva (m)",
            "Long. (m)",
            "Litología",
            "RMR",
            "Q",
            "Clase",
            "Soporte",
            "Perno (m)",
            "Esp. (m)",
            "Shotcrete (mm)",
            "Cerchas",
        ],
        filas_tramos,
        "Resumen de Sostenimiento Subterráneo a lo Largo de los 5,556.08 m",
    )

    return Memoria(
        archivo="13_Sostenimiento.md",
        titulo="13 · Memoria de Cálculo: Sostenimiento Subterráneo del Túnel (Bieniawski 1989 y Q de Barton)",
        secciones=[
            (
                "1. Sostenimiento Subterráneo Longitudinal (Bieniawski 1989 y Q de Barton)",
                [
                    f"Para el ancho de excavación subterránea $B = {r['ancho_b']:.2f}\\text{{ m}}$ y relación "
                    f"de soporte $\\text{{ESR}} = {r['esr']:.2f}$, la longitud teórica de los pernos sistemáticos "
                    f"en bóveda y hastiales según Grimstad & Barton (1993) es "
                    f"$L = 2.0 + 0.15 B / \\text{{ESR}} = {r['long_perno_teorico']:.2f}\\text{{ m}}$.",
                    t_sost_tunel,
                ],
            ),
        ],
    )
