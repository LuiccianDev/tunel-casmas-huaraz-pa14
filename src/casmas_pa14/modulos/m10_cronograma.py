"""10 · Cronograma: actividades con dependencias y diagrama de Gantt."""

import math
from datetime import timedelta

from ..modelo import Gantt, Hoja, Libro, Tabla, tabla_parametros

CLAVE = "cronograma"


def _duracion(a: dict, ctx: dict) -> int:
    if "duracion_dias" in a:
        return int(a["duracion_dias"])
    if a.get("rendimiento") == "excavacion":
        return ctx["seccion"]["dias_excavacion"]
    if "rendimiento_m_dia" in a:
        return math.ceil(ctx["ubicacion"]["longitud_m"] / a["rendimiento_m_dia"])
    raise ValueError(f"Actividad {a['id']}: falta duracion_dias o rendimiento.")


def calcular(p: dict, ctx: dict) -> dict:
    inicio_obra = p["proyecto"]["fecha_inicio"]
    actividades: dict[str, dict] = {}
    for a in p["cronograma"]["actividades"]:
        duracion = _duracion(a, ctx)
        preds = a.get("predecesoras", [])
        desfase = timedelta(days=a.get("desfase_dias", 0))
        faltantes = [x for x in preds if x not in actividades]
        if faltantes:
            raise ValueError(
                f"Actividad {a['id']}: predecesoras no definidas antes: {faltantes}"
            )
        if not preds:
            inicio = inicio_obra + desfase
        elif a.get("tipo", "FC") == "CC":
            inicio = max(actividades[x]["inicio"] for x in preds) + desfase
        else:
            inicio = (
                max(actividades[x]["fin"] for x in preds) + timedelta(days=1) + desfase
            )
        actividades[a["id"]] = {
            "id": a["id"],
            "nombre": a["nombre"],
            "duracion": duracion,
            "predecesoras": preds,
            "tipo": a.get("tipo", "FC") if preds else "",
            "desfase": a.get("desfase_dias", 0),
            "inicio": inicio,
            "fin": inicio + timedelta(days=duracion - 1),
        }
    fin_obra = max(x["fin"] for x in actividades.values())
    return {
        "actividades": list(actividades.values()),
        "inicio": inicio_obra,
        "fin": fin_obra,
        "plazo_dias": (fin_obra - inicio_obra).days + 1,
    }


def libro(r: dict, p: dict) -> Libro:
    acts = r["actividades"]
    tabla = Tabla(
        [
            "ID",
            "Actividad",
            "Duración (días)",
            "Predecesoras",
            "Relación",
            "Desfase (días)",
            "Inicio",
            "Fin",
        ],
        [
            [
                x["id"],
                x["nombre"],
                x["duracion"],
                ", ".join(x["predecesoras"]),
                x["tipo"],
                x["desfase"],
                x["inicio"],
                x["fin"],
            ]
            for x in acts
        ],
        "FC = fin-comienzo · CC = comienzo-comienzo",
    )
    plazo = tabla_parametros(
        [
            ("Inicio de obra", "", r["inicio"], "", "Dato"),
            ("Fin de obra", "", r["fin"], "", "Máx. fin"),
            ("Plazo total", "T", r["plazo_dias"], "días", "Fin − Inicio + 1"),
            ("Plazo total", "T", r["plazo_dias"] / 30, "meses", "T / 30"),
        ],
        "Plazo",
    )
    gantt = Gantt(
        r["inicio"],
        [(f"{x['id']}. {x['nombre']}", x["inicio"], x["fin"]) for x in acts],
    )
    return Libro(
        "10_Cronograma.xlsx",
        [
            Hoja("Actividades", "Programación de actividades", [tabla, plazo]),
            Hoja("Gantt", "Diagrama de Gantt (semanas)", gantt=gantt),
        ],
    )
