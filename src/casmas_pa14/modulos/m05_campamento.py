"""05 · Campamento: edificaciones, áreas y dimensiones."""

import math

from ..modelo import Hoja, Libro, Tabla, redondear_arriba, tabla_parametros

CLAVE = "campamento"


def calcular(p: dict, ctx: dict) -> dict:
    per = ctx["personal"]
    poblacion = {"total": per["total"], "staff": per["staff"], "obrero": per["obreros"]}
    c = p["campamento"]
    edificaciones = []
    for e in c["edificaciones"]:
        ancho = e.get("ancho_m", c["ancho_edificio_m"])
        if e["base"] == "fijo":
            personas, modulos, area = None, 1, e["area_m2"]
        else:
            personas = poblacion[e["base"]]
            modulos = math.ceil(
                personas / e.get("turnos", 1) / e["personas_por_modulo"]
            )
            area = modulos * e["area_modulo_m2"]
        largo = redondear_arriba(area / ancho, 0.5)
        edificaciones.append(
            {
                "nombre": e["nombre"],
                "base": e["base"],
                "personas": personas,
                "modulos": modulos,
                "area_m2": area,
                "ancho_m": ancho,
                "largo_m": largo,
            }
        )
    area_construida = sum(e["area_m2"] for e in edificaciones)
    area_terreno = area_construida * c["factor_terreno"]
    return {
        "edificaciones": edificaciones,
        "area_construida_m2": area_construida,
        "area_terreno_m2": area_terreno,
        "lado_terreno_m": math.sqrt(area_terreno),
    }


def libro(r: dict, p: dict) -> Libro:
    edificaciones = Tabla(
        [
            "Edificación",
            "Base de cálculo",
            "Personas",
            "Módulos / puestos",
            "Área (m²)",
            "Ancho (m)",
            "Largo (m)",
        ],
        [
            [
                e["nombre"],
                e["base"],
                e["personas"],
                e["modulos"],
                e["area_m2"],
                e["ancho_m"],
                e["largo_m"],
            ]
            for e in r["edificaciones"]
        ],
        "Módulos = ⌈personas / turnos / personas por módulo⌉ · Largo = área / ancho (redondeado a 0.5 m)",
    )
    resumen = tabla_parametros(
        [
            ("Área construida", "Ac", r["area_construida_m2"], "m²", "Σ áreas"),
            (
                "Factor de terreno",
                "ft",
                p["campamento"]["factor_terreno"],
                "",
                "Dato (vías, retiros)",
            ),
            ("Área de terreno", "At", r["area_terreno_m2"], "m²", "Ac · ft"),
            ("Lado equivalente (cuadrado)", "Lt", r["lado_terreno_m"], "m", "√At"),
        ]
    )
    return Libro(
        "05_Campamento.xlsx",
        [
            Hoja("Edificaciones", "Edificaciones del campamento", [edificaciones]),
            Hoja("Resumen", "Áreas del campamento", [resumen]),
        ],
    )
