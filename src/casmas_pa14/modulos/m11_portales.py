"""11 - Portales y Banquetas.

Calcula el volumen y geometria de excavacion para los portales de manera didactica y dinamica.
"""

import math
from typing import Any

from ..modelo import Hoja, Libro, Tabla

CLAVE = "portales"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    portales = p.get("portales", {})
    banquetas = portales.get("banquetas", [])
    factor_esponjamiento = portales.get("factor_esponjamiento", 1.30)
    resultados = []
    volumen_total_insitu = 0.0
    volumen_total_esponjado = 0.0

    for b in banquetas:
        h = float(b.get("altura_banco_m", 0.0))
        largo = float(b.get("largo_banco_m", 0.0))
        alpha = float(b.get("angulo_talud_deg", 90.0))
        beta = float(b.get("angulo_perfil_deg", 0.0))
        w = float(b.get("ancho_plataforma_m", b.get("lado_mayor_m", 5.0)))

        base_talud = (
            h / math.tan(math.radians(alpha)) if (alpha != 90 and alpha > 0) else 0.0
        )
        area_talud = 0.5 * h * base_talud
        area_rect = w * h
        area_excavacion = max(0.0, area_rect - area_talud)

        vol_insitu = area_excavacion * largo
        vol_esponjado = vol_insitu * factor_esponjamiento
        volumen_total_insitu += vol_insitu
        volumen_total_esponjado += vol_esponjado

        resultados.append(
            {
                "id": b.get("id", "Banqueta"),
                "largo": round(largo, 3),
                "altura": round(h, 3),
                "ancho": round(w, 3),
                "alpha": round(alpha, 1),
                "beta": round(beta, 1),
                "base_talud": round(base_talud, 4),
                "area_excavacion": round(area_excavacion, 4),
                "vol_insitu": round(vol_insitu, 2),
                "factor_esp": factor_esponjamiento,
                "vol_esponjado": round(vol_esponjado, 2),
            }
        )

    return {
        "banquetas": resultados,
        "factor_esponjamiento": factor_esponjamiento,
        "volumen_total_insitu_m3": round(volumen_total_insitu, 2),
        "volumen_total_esponjado_m3": round(volumen_total_esponjado, 2),
    }


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    cols = [
        "ID Banqueta",
        "Largo L (m)",
        "Altura H (m)",
        "Ancho W (m)",
        "Talud α (°)",
        "Perfil β (°)",
        "Base Cuña (m)",
        "Área Sección (m²)",
        "Volumen In-Situ (m³)",
        "Esponjamiento",
        "Volumen Esponjado (m³)",
    ]

    filas = []
    fila_inicio = 5
    fila_actual = fila_inicio

    for b in resultados["banquetas"]:
        # Columnas Excel:
        # A: ID, B: Largo (L), C: Altura (H), D: Ancho (W), E: Alpha, F: Beta
        # G: Base Cuña = C / TAN(RADIANS(E))
        # H: Area = (D*C) - (0.5*C*G)
        # I: Vol In-situ = H * B
        # J: Factor Esponjamiento
        # K: Vol Esponjado = I * J
        f_base = (
            f"=IF(E{fila_actual}=90, 0, C{fila_actual}/TAN(RADIANS(E{fila_actual})))"
        )
        f_area = f"=(D{fila_actual}*C{fila_actual})-(0.5*C{fila_actual}*G{fila_actual})"
        f_vol_insitu = f"=H{fila_actual}*B{fila_actual}"
        f_vol_esp = f"=I{fila_actual}*J{fila_actual}"

        filas.append(
            [
                b["id"],
                b["largo"],
                b["altura"],
                b["ancho"],
                b["alpha"],
                b["beta"],
                f_base,
                f_area,
                f_vol_insitu,
                b["factor_esp"],
                f_vol_esp,
            ]
        )
        fila_actual += 1

    if resultados["banquetas"]:
        fila_fin = fila_actual - 1
        filas.append(
            [
                "TOTAL PORTAL",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                f"=SUM(I{fila_inicio}:I{fila_fin})",
                "",
                f"=SUM(K{fila_inicio}:K{fila_fin})",
            ]
        )
    else:
        filas = [["No hay banquetas configuradas"] + [""] * 10]

    return Libro(
        archivo="11_Portales.xlsx",
        hojas=[
            Hoja(
                nombre="Banquetas_Portales",
                titulo="Cálculo Geométrico y Volumétrico de Banquetas de Portal",
                tablas=[Tabla(cols, filas)],
            )
        ],
    )
