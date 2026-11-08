"""Generación de memoria técnica para 04 · Personal."""

from ...modelo import Memoria
from .hojas import (
    _tabla_cruce_campamentos,
    _tabla_macro_areas,
    _tabla_mano_obra,
)


def memoria(r: dict, p: dict) -> Memoria:
    reg = p["regimen"]
    resumen_ejecutivo = [
        "El presente informe documenta el dimensionamiento definitivo, la justificación "
        "técnico-operativa y la estructura jerárquica del personal para la construcción "
        f"del **Túnel Casmas Huaraz PA14**, infraestructura subterránea bidireccional "
        f"ubicada a una altitud de {p['proyecto']['altitud_msnm']:.0f} m s.n.m.",
        "La excavación se realiza mediante el método convencional de perforación y "
        "voladura mecanizada (*Drill & Blast*), atacando simultáneamente e ininterrumpidamente "
        "desde dos frentes: **Frente 1 (Portal A - Entrada, 3,900 msnm)** y **Frente 2 "
        "(Portal B - Salida, 3,800 msnm)**.",
    ]

    justificacion_regimen = [
        f"### 2.1 Justificación del Régimen {reg['dias_trabajo']}×{reg['dias_descanso']} "
        f"({reg['dias_trabajo']} días de trabajo por {reg['dias_descanso']} de descanso)\n"
        "1. **Condición Fisiológica y Mal de Montaña (Hipoxia a gran altitud):**\n"
        f"   El proyecto se sitúa a {p['proyecto']['altitud_msnm']:.0f} m s.n.m. bajo "
        "condiciones climáticas frías y reducida presión de oxígeno. Jornadas estándar "
        "de 6×1 o 5×2 obligarían a constantes traslados por vías de montaña, generando "
        "fatiga severa. El régimen atípico acumulativo permite que el personal labore "
        "aclimatado y descienda una semana continua a valles de menor cota para su "
        "recuperación biológica y psicológica.\n"
        "2. **Sustento Legal y Constitucional Peruano:**\n"
        "   - **D.S. N° 024-2016-EM (Reglamento de Seguridad Minera), Art. 201:** "
        "autoriza jornadas atípicas y acumulativas en obras subterráneas aisladas "
        "siempre que el promedio no exceda 48 horas semanales.\n"
        "   - **Sentencia del Tribunal Constitucional (STC N° 4635-2004-AA/TC):** "
        "convalida los regímenes acumulativos (como el 14×7) al garantizar el descanso "
        "profiláctico adecuado en altitud.\n\n"
        "### 2.2 Justificación de las Guardias de 12 Horas (Día y Noche)\n"
        "1. **Minimización de Tiempos Muertos:**\n"
        "   En túneles largos donde el frente avanza kilómetros hacia el interior, "
        "el tránsito toma entre 30 y 45 minutos. Con tres turnos de 8 h se perderían "
        "hasta 4.5 h diarias en relevos. Dos guardias de 12 h optimizan la utilización "
        "de maquinaria pesada mediante un único relevo en caliente.\n"
        "2. **Ciclo Completo de Perforación y Voladura (*Drill & Blast*):**\n"
        "   El ciclo típico por pase (perforación con Jumbo 2.5 h, cargado de explosivos "
        "1.5 h, disparo y ventilación 1.0 h, desate mecanizado y acarreo LHD/volquetes "
        "3.5 h, sostenimiento con robot de shotcrete y pernos 3.0 h) suma ~11.5 a 12.0 h. "
        "La guardia de 12 horas asegura exactamente un ciclo cerrado y sostenido por turno.\n"
        f"3. **Distribución de Cargas:** {r['dia_total']} pax ({r['dia_total'] / r['total'] * 100:.1f}%) "
        f"en Guardia Día y {r['noche_total']} pax ({r['noche_total'] / r['total'] * 100:.1f}%) "
        "en Guardia Noche.",
    ]

    justificacion_mano_obra = [
        "Para una asignación de costos y responsabilidades operativas transparente, "
        "la dotación se descompone en Mano de Obra Directa (MOD) y Mano de Obra Indirecta (MOI):\n\n"
        f"1. **Mano de Obra Directa (MOD — {r['directa']} pax · {r['directa'] / r['total'] * 100:.1f}%):**\n"
        "   Trabajadores que intervienen directamente en el ciclo de arranque, "
        "sostenimiento y acarreo de la roca en el túnel:\n"
        "   - **Perforación y Voladura (38 pax):** Jumboístas titulares y de relevo, "
        "perforistas de emboquillado, blasters certificados SUCAMEC (Ley N° 30299) "
        "y ayudantes de cargado de explosivos.\n"
        "   - **Sostenimiento Mecanizado (12 pax):** Operadores de robot lanzador de "
        "shotcrete vía húmeda y cuadrillas de empernado / malla electrosoldada.\n"
        "   - **Carguío y Acarreo a DME (24 pax):** Operadores de pala LHD (Scooptram) "
        "y choferes de volquetes roqueros hacia botaderos autorizados.\n"
        "   - **Servicios de Frente y Plantas (15 pax):** Operadores de planta de concreto, "
        "mixers, bombas de achique y ventilación principal.\n"
        "   - **Ingeniería Subterránea y Geomecánica (21 pax):** Jefes de frente, "
        "geólogos de mina (RMR / Q de Barton), geomecánicos, topógrafos láser de precisión, "
        "ingenieros de planeamiento y laboratoristas de concreto.\n\n"
        f"2. **Mano de Obra Indirecta (MOI — {r['indirecta']} pax · {r['indirecta'] / r['total'] * 100:.1f}%):**\n"
        "   Personal que asegura la continuidad logística, habitabilidad, seguridad, "
        "mantenimiento y soporte institucional:\n"
        "   - **Personal de Campamento (155 pax):** Alta Dirección, Contabilidad y Costos, "
        "Asesoría Legal, RR.HH., Asistencia Social, Relaciones Comunitarias, TI/Redes, "
        "Servicio Médico Ocupacional / Paramédicos 24h, y el equipo integral de Catering, "
        "Cuartelería, Lavandería Industrial y Plantas PTAP/PTAR (99 pax).\n"
        "   - **Personal de Servicio y Soporte (81 pax):** Jefatura y supervisores SSOMA "
        "subterráneos 24h, especialistas en ventilación/gases, logística y almaceneros, "
        "talleres de mantenimiento electromecánico (jumbos, scoops, volquetes, electricistas), "
        "control de polvorín SUCAMEC, garitas de vigilancia y la flota de conductores "
        "(buses interprovinciales, ambulancias tipo II 24h, cisternas diésel y agua).",
    ]

    justificacion_campamentos = [
        "El dimensionamiento de los campamentos responde estrictamente a la ubicación de los frentes:\n"
        f"- **Campamento Principal CAMP1 (Portal A - Entrada): {r['camp1_total']} pax "
        f"({r['camp1_total'] / r['total'] * 100:.1f}%):** Aloja la administración central, "
        "talleres electromecánicos principales, ingeniería y el Frente 1 de excavación.\n"
        f"- **Campamento Satélite CAMP2 (Portal B - Salida): {r['camp2_total']} pax "
        f"({r['camp2_total'] / r['total'] * 100:.1f}%):** Instalación satélite autónoma dedicada "
        "al Frente 2 de excavación, con cuadrillas operativas, tópico médico de guardia, "
        "mantenimiento de retén y servicio de comedor/dormitorios propio.\n"
        f"- **Población Total en Campamento:** {r['total']} personas.\n"
        f"- **Dotación en Planilla (con relevo 14×7):** {r['planilla']} personas "
        f"(= ⌈{r['total']} × {r['factor_regimen']:.3f}⌉).",
    ]

    return Memoria(
        "04_Personal.md",
        "04 · Personal, Organigrama y Gestión de Capital Humano",
        [
            ("1. Resumen ejecutivo y parámetros maestros", resumen_ejecutivo),
            (
                "2. Justificación del régimen laboral y guardias de 12 horas",
                justificacion_regimen,
            ),
            (
                "3. Clasificación de Mano de Obra Directa (MOD) e Indirecta (MOI)",
                [_tabla_mano_obra(r), "\n".join(justificacion_mano_obra)],
            ),
            ("4. Estructura y macro-áreas funcionales", [_tabla_macro_areas(r)]),
            (
                "5. Distribución espacial y cruce de guardias",
                [_tabla_cruce_campamentos(r), "\n".join(justificacion_campamentos)],
            ),
        ],
    )
