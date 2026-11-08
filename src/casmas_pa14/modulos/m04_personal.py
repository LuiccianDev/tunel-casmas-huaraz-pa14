"""04 · Personal: relación de cargos, organigrama y población del campamento."""

import math

from .personal_hojas import (
    _tabla_cruce_campamentos,
    _tabla_macro_areas,
    _tabla_mano_obra,
    libro,
    memoria,
)

CLAVE = "personal"

__all__ = [
    "CLAVE",
    "calcular",
    "libro",
    "memoria",
    "_tabla_macro_areas",
    "_tabla_cruce_campamentos",
    "_tabla_mano_obra",
]


def calcular(p: dict, ctx: dict) -> dict:
    frentes = p["perforacion"]["frentes"]
    filas = []
    for x in p["personal"]:
        macro_area = x.get("macro_area", "Personal de Servicio")
        sub_area = x.get("sub_area", x.get("area", "General"))
        cargo = x["cargo"]
        categoria = x["categoria"]
        tipo_labor = x.get("tipo_labor", "indirecta").capitalize()
        campamento = x.get("campamento", "CAMP1")
        turno = x.get("turno", "Dia")
        if "cantidad" in x:
            cantidad = x["cantidad"]
        else:
            mult = frentes if x.get("por_frente", False) else 1
            cantidad = x.get("por_guardia", 1) * x.get("guardias", 1) * mult

        filas.append(
            {
                "macro_area": macro_area,
                "sub_area": sub_area,
                "area": sub_area,  # compatibilidad
                "cargo": cargo,
                "categoria": categoria,
                "tipo_labor": tipo_labor,
                "campamento": campamento,
                "turno": turno,
                "cantidad": cantidad,
                "total": cantidad,  # compatibilidad
            }
        )

    total = sum(x["cantidad"] for x in filas)
    staff = sum(x["cantidad"] for x in filas if x["categoria"] == "staff")
    obreros = total - staff
    directa = sum(x["cantidad"] for x in filas if x["tipo_labor"].lower() == "directa")
    indirecta = sum(
        x["cantidad"] for x in filas if x["tipo_labor"].lower() == "indirecta"
    )

    por_macro_area: dict[str, int] = {}
    for m in [
        "Personal de Campamento",
        "Personal de Frente",
        "Personal de Servicio",
    ]:
        por_macro_area[m] = sum(x["cantidad"] for x in filas if x["macro_area"] == m)

    por_area: dict[str, int] = {}
    for x in filas:
        por_area[x["sub_area"]] = por_area.get(x["sub_area"], 0) + x["cantidad"]

    camp1_total = sum(x["cantidad"] for x in filas if x["campamento"] == "CAMP1")
    camp2_total = sum(x["cantidad"] for x in filas if x["campamento"] == "CAMP2")
    dia_total = sum(x["cantidad"] for x in filas if x["turno"] == "Dia")
    noche_total = sum(x["cantidad"] for x in filas if x["turno"] == "Noche")

    camp1_dia = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP1" and x["turno"] == "Dia"
    )
    camp1_noche = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP1" and x["turno"] == "Noche"
    )
    camp2_dia = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP2" and x["turno"] == "Dia"
    )
    camp2_noche = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP2" and x["turno"] == "Noche"
    )

    frente_por_guardia = sum(
        x["cantidad"]
        for x in filas
        if x["macro_area"] == "Personal de Frente"
        and x["campamento"] == "CAMP1"
        and x["turno"] == "Dia"
    )

    reg = p["regimen"]
    factor = (reg["dias_trabajo"] + reg["dias_descanso"]) / reg["dias_trabajo"]
    planilla = math.ceil(total * factor)

    camp1_staff = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP1" and x["categoria"] == "staff"
    )
    camp1_obreros = camp1_total - camp1_staff
    camp2_staff = sum(
        x["cantidad"]
        for x in filas
        if x["campamento"] == "CAMP2" and x["categoria"] == "staff"
    )
    camp2_obreros = camp2_total - camp2_staff

    return {
        "filas": filas,
        "por_macro_area": por_macro_area,
        "por_area": por_area,
        "total": total,
        "staff": staff,
        "obreros": obreros,
        "directa": directa,
        "indirecta": indirecta,
        "camp1_total": camp1_total,
        "camp2_total": camp2_total,
        "camp1_staff": camp1_staff,
        "camp1_obreros": camp1_obreros,
        "camp2_staff": camp2_staff,
        "camp2_obreros": camp2_obreros,
        "dia_total": dia_total,
        "noche_total": noche_total,
        "camp1_dia": camp1_dia,
        "camp1_noche": camp1_noche,
        "camp2_dia": camp2_dia,
        "camp2_noche": camp2_noche,
        "frente_por_guardia": frente_por_guardia,
        "factor_regimen": factor,
        "planilla": planilla,
    }
