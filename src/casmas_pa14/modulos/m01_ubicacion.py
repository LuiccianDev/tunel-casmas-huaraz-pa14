"""01 · Ubicación: coordenadas, eje del túnel y distancias mínimas."""

import math

from ..modelo import Hoja, Libro, Tabla, tabla_parametros

CLAVE = "ubicacion"


def distancia(a: dict, b: dict) -> float:
    """Distancia horizontal entre dos puntos UTM."""
    return math.hypot(b["este"] - a["este"], b["norte"] - a["norte"])


def calcular(p: dict, ctx: dict) -> dict:
    u = p["ubicacion"]
    puntos = {pt["id"]: pt for pt in u["puntos"]}
    pe, ps = puntos[u["portal_entrada"]], puntos[u["portal_salida"]]
    d_este, d_norte = ps["este"] - pe["este"], ps["norte"] - pe["norte"]
    l_horizontal = math.hypot(d_este, d_norte)
    desnivel = ps["cota"] - pe["cota"]
    restricciones = []
    for r in u["restricciones"]:
        d = distancia(puntos[r["desde"]], puntos[r["hasta"]])
        restricciones.append({**r, "distancia_m": d, "cumple": d >= r["minimo_m"]})
    return {
        "puntos": puntos,
        "longitud_horizontal_m": l_horizontal,
        "desnivel_m": desnivel,
        "longitud_m": math.hypot(l_horizontal, desnivel),
        "pendiente_pct": desnivel / l_horizontal * 100,
        "azimut_deg": math.degrees(math.atan2(d_este, d_norte)) % 360,
        "restricciones": restricciones,
    }


def libro(r: dict, p: dict) -> Libro:
    u = p["ubicacion"]
    coordenadas = Tabla(
        [
            "Nombre",
            "Zona",
            "Coordenada Este (m E)",
            "Coordenada Norte (m S)",
            "Altitud (m)",
        ],
        [
            [
                x["nombre"],
                x.get("zona", u["zona_utm"]),
                x["este"],
                x["norte"],
                x["cota"],
            ]
            for x in r["puntos"].values()
        ],
        f"Sistema: UTM {u['datum']} — Zona {u['zona_utm']}",
    )
    eje = tabla_parametros(
        [
            (
                "Longitud horizontal",
                "Lh",
                r["longitud_horizontal_m"],
                "m",
                "√(ΔE² + ΔN²)",
            ),
            (
                "Desnivel entre portales",
                "Δz",
                r["desnivel_m"],
                "m",
                "Cota PS − Cota PE",
            ),
            ("Longitud del túnel (eje)", "L", r["longitud_m"], "m", "√(Lh² + Δz²)"),
            ("Pendiente", "i", r["pendiente_pct"], "%", "Δz / Lh × 100"),
            ("Azimut del eje", "Az", r["azimut_deg"], "°", "atan2(ΔE, ΔN)"),
        ]
    )
    distancias = Tabla(
        [
            "Desde",
            "Hasta",
            "Distancia (m)",
            "Mínimo (m)",
            "¿Cumple?",
            "Criterio / Fuente",
        ],
        [
            [
                r["puntos"][x["desde"]]["nombre"],
                r["puntos"][x["hasta"]]["nombre"],
                x["distancia_m"],
                x["minimo_m"],
                x["cumple"],
                x["fuente"],
            ]
            for x in r["restricciones"]
        ],
    )
    return Libro(
        "01_Ubicacion.xlsx",
        [
            Hoja(
                "Coordenadas", "Coordenadas de portales e instalaciones", [coordenadas]
            ),
            Hoja("Eje del tunel", "Geometría del eje del túnel", [eje]),
            Hoja("Distancias", "Verificación de distancias mínimas", [distancias]),
        ],
    )
