"""04 · Personal: relación de cargos y población del campamento."""

import math

from ..modelo import Hoja, Libro, Tabla, tabla_parametros

CLAVE = "personal"


def calcular(p: dict, ctx: dict) -> dict:
    frentes = p["perforacion"]["frentes"]
    filas = []
    for x in p["personal"]:
        multiplicador = frentes if x.get("por_frente", False) else 1
        total = x["por_guardia"] * x["guardias"] * multiplicador
        filas.append({**x, "multiplicador": multiplicador, "total": total})
    por_area: dict[str, int] = {}
    for x in filas:
        por_area[x["area"]] = por_area.get(x["area"], 0) + x["total"]
    total = sum(x["total"] for x in filas)
    staff = sum(x["total"] for x in filas if x["categoria"] == "staff")
    reg = p["regimen"]
    factor = (reg["dias_trabajo"] + reg["dias_descanso"]) / reg["dias_trabajo"]
    return {
        "filas": filas,
        "por_area": por_area,
        "total": total,
        "staff": staff,
        "obreros": total - staff,
        "frente_por_guardia": sum(
            x["por_guardia"] for x in p["personal"] if x["area"] == "Frente"
        ),
        "factor_regimen": factor,
        "planilla": math.ceil(total * factor),
    }


def libro(r: dict, p: dict) -> Libro:
    reg = p["regimen"]
    relacion = Tabla(
        ["Área", "Cargo", "Categoría", "Por guardia", "Guardias", "× Frentes", "Total"],
        [
            [
                x["area"],
                x["cargo"],
                x["categoria"],
                x["por_guardia"],
                x["guardias"],
                x["multiplicador"],
                x["total"],
            ]
            for x in r["filas"]
        ],
    )
    areas = Tabla(
        ["Área", "Personas"], [[a, n] for a, n in r["por_area"].items()], "Por área"
    )
    resumen = tabla_parametros(
        [
            ("Población en campamento", "Pob", r["total"], "personas", "Σ Total"),
            ("Staff", "Ps", r["staff"], "personas", "Σ categoría staff"),
            ("Obreros", "Po", r["obreros"], "personas", "Pob − Ps"),
            (
                "Personal de frente por guardia (1 frente)",
                "Pf",
                r["frente_por_guardia"],
                "personas",
                "Para ventilación",
            ),
            (
                "Régimen de trabajo",
                "",
                f"{reg['dias_trabajo']}x{reg['dias_descanso']}",
                "días",
                "Dato",
            ),
            (
                "Personal en planilla (con relevos)",
                "Pl",
                r["planilla"],
                "personas",
                "⌈Pob · (t + d) / t⌉",
            ),
        ],
        "Totales",
    )
    return Libro(
        "04_Personal.xlsx",
        [
            Hoja(
                "Relacion de personal",
                "Relación de personal por área y cargo",
                [relacion],
            ),
            Hoja("Resumen", "Resumen de personal", [areas, resumen]),
        ],
    )
