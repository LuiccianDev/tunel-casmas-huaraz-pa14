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
        "pendiente_pct": (desnivel / l_horizontal) * 100,
        "azimut_deg": math.degrees(math.atan2(d_este, d_norte)) % 360,
        "restricciones": restricciones,
    }


def libro(r: dict, p: dict) -> Libro:
    u = p["ubicacion"]
    filas_puntos = {punto_id: 6 + indice for indice, punto_id in enumerate(r["puntos"])}
    pe = filas_puntos[u["portal_entrada"]]
    ps = filas_puntos[u["portal_salida"]]
    este_pe, norte_pe, cota_pe = (
        f"Coordenadas!C{pe}",
        f"Coordenadas!D{pe}",
        f"Coordenadas!E{pe}",
    )
    este_ps, norte_ps, cota_ps = (
        f"Coordenadas!C{ps}",
        f"Coordenadas!D{ps}",
        f"Coordenadas!E{ps}",
    )
    formula_lh = f"=SQRT(({este_ps}-{este_pe})^2+({norte_ps}-{norte_pe})^2)"
    formula_dz = f"={cota_ps}-{cota_pe}"
    formula_l = "=SQRT(C5^2+C6^2)"
    formula_pendiente = "=C6/C5"
    formula_azimut = (
        f"=MOD(DEGREES(ATAN2({este_ps}-{este_pe},{norte_ps}-{norte_pe})),360)"
    )
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
        f"ENTRADAS EDITABLES | Sistema: UTM {u['datum']} — Zona {u['zona_utm']}",
    )
    eje = tabla_parametros(
        [
            (
                "Longitud horizontal",
                "Lh",
                formula_lh,
                "m",
                "√(ΔE² + ΔN²)",
            ),
            (
                "Desnivel entre portales",
                "Δz",
                formula_dz,
                "m",
                "Cota PS − Cota PE",
            ),
            ("Longitud del túnel (eje)", "L", formula_l, "m", "√(Lh² + Δz²)"),
            ("Pendiente", "i", formula_pendiente, "%", "Δz / Lh"),
            (
                "Azimut del eje",
                "Az",
                formula_azimut,
                "°",
                "MOD(DEGREES(ATAN2(ΔE, ΔN)),360)",
            ),
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
            _fila_distancia(x, r["puntos"], filas_puntos, fila_excel=5 + indice)
            for indice, x in enumerate(r["restricciones"])
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


def _fila_distancia(
    restriccion: dict,
    puntos: dict,
    filas_puntos: dict[str, int],
    fila_excel: int,
) -> list:
    """Crea una fila de distancias con cálculo nativo de Excel."""
    desde = filas_puntos[restriccion["desde"]]
    hasta = filas_puntos[restriccion["hasta"]]
    formula_distancia = (
        f"=SQRT((Coordenadas!C{hasta}-Coordenadas!C{desde})^2+"
        f"(Coordenadas!D{hasta}-Coordenadas!D{desde})^2)"
    )
    return [
        puntos[restriccion["desde"]]["nombre"],
        puntos[restriccion["hasta"]]["nombre"],
        formula_distancia,
        restriccion["minimo_m"],
        f"=C{fila_excel}>=D{fila_excel}",
        restriccion["fuente"],
    ]
