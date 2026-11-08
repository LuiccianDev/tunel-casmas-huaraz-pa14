"""Generación de memoria técnica para 06 · Maquinaria."""

from ...catalogos import FICHAS_TECNICAS
from ...modelo import Memoria
from .hojas import _tabla_resumen_fichas


def memoria(r: dict, p: dict) -> Memoria:
    """Genera la memoria técnica de dimensionamiento y selección de maquinaria en Markdown."""
    fichas = r.get("fichas", FICHAS_TECNICAS)
    secciones = [
        (
            "1. Criterios de Selección y Dimensionamiento de Flota",
            [
                "La selección de la flota de maquinaria pesada responde a los requerimientos "
                f"de excavación mecanizada a sección completa ({p['seccion']['ancho_m']:.2f} m × "
                f"{p['seccion']['altura_m']:.2f} m) y a la necesidad de evacuar el material "
                "con camiones volquetes convencionales de alta potencia y capacidad.",
                "Se garantiza la compatibilidad de gálibos entre los equipos seleccionados y la sección "
                "del túnel, así como el cumplimiento normativo D.S. 024-2016-EM en cuanto a ventilación "
                "por potencia diésel en interior mina.",
            ],
        ),
        (
            "2. Ciclos Operativos de Perforación, Carguío y Evacuación",
            [
                f"- **Tiempo de perforación de barreno ({r['taladros_frente']} taladros perforados):** "
                f"{r['t_perforacion_h']:.2f} h por disparo.",
                f"- **Productividad del cargador en frente:** {r['prod_cargador_m3_h']:.2f} m³/h.",
                f"- **Ciclo de acarreo a botadero:** {r['ciclo_volquete_min']:.2f} min por viaje.",
                f"- **Área requerida de botadero:** {r['area_botadero_m2']:,.0f} m².",
            ],
        ),
        (
            "3. Tabla Consolidada de Fichas Técnicas de Maquinaria",
            [_tabla_resumen_fichas(fichas)],
        ),
    ]
    return Memoria(
        "06_Maquinaria.md",
        "Memoria Técnica: Gestión y Asignación de Flota de Maquinaria",
        secciones,
    )
