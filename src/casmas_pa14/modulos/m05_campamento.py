"""05 · Campamento: edificaciones especializadas (EDIF-01 a EDIF-24), áreas y CAD."""

import math

from ..modelo import Hoja, Libro, Memoria, Tabla, redondear_arriba, tabla_parametros

CLAVE = "campamento"


def calcular(p: dict, ctx: dict) -> dict:
    per = ctx["personal"]
    c = p["campamento"]
    edificaciones = []

    for i, e in enumerate(c["edificaciones"], 1):
        cod_id = e.get("id", f"EDIF-{i:02d}")
        camp = e.get("campamento", "CAMP1")
        ancho = e.get("ancho_m", c["ancho_edificio_m"])
        grupo = e.get("grupo", "General")
        norma = e.get("norma", "RNE / D.S. 024-2016-EM")

        # Población aplicable según el campamento
        if camp == "CAMP1":
            pob_dict = {
                "total": per.get("camp1_total", per["total"]),
                "staff": per.get("camp1_staff", per["staff"]),
                "obrero": per.get("camp1_obreros", per["obreros"]),
            }
        elif camp == "CAMP2":
            pob_dict = {
                "total": per.get("camp2_total", per["total"]),
                "staff": per.get("camp2_staff", per["staff"]),
                "obrero": per.get("camp2_obreros", per["obreros"]),
            }
        else:
            pob_dict = {
                "total": per["total"],
                "staff": per["staff"],
                "obrero": per["obreros"],
            }

        if e["base"] == "fijo":
            personas, modulos, area = None, 1, e["area_m2"]
        else:
            personas = pob_dict[e["base"]]
            modulos = math.ceil(personas / e["turnos"] / e["personas_por_modulo"])
            area = modulos * e["area_modulo_m2"]

        largo = redondear_arriba(area / ancho, 0.5)

        edificaciones.append(
            {
                "id": cod_id,
                "nombre": e["nombre"],
                "grupo": grupo,
                "campamento": camp,
                "base": e["base"],
                "personas": personas,
                "modulos": modulos,
                "area_m2": area,
                "ancho_m": ancho,
                "largo_m": largo,
                "norma": norma,
            }
        )

    area_construida = sum(e["area_m2"] for e in edificaciones)
    area_camp1 = sum(e["area_m2"] for e in edificaciones if e["campamento"] == "CAMP1")
    area_camp2 = sum(e["area_m2"] for e in edificaciones if e["campamento"] == "CAMP2")
    area_terreno = area_construida * c["factor_terreno"]

    # Agrupación por Grupos Funcionales
    grupos_orden = [
        "Residencia y Habitabilidad",
        "Comedor y Alimentación",
        "Administración y Documentos",
        "Salud y Bienestar",
        "Maquinaria y Mantenimiento",
        "Almacenes y Logística",
        "Agua y Saneamiento",
        "Residuos y Ambiente",
        "Energía y Combustible",
        "Operación y Portales",
        "Seguridad y Explosivos",
        "Vigilancia y Transporte",
    ]
    por_grupo = []
    for g in grupos_orden:
        edifs_g = [e for e in edificaciones if e["grupo"] == g]
        if edifs_g:
            area_g = sum(e["area_m2"] for e in edifs_g)
            cods = ", ".join(e["id"] for e in edifs_g)
            por_grupo.append(
                {
                    "grupo": g,
                    "edificaciones": cods,
                    "cantidad_edif": len(edifs_g),
                    "area_m2": area_g,
                    "pct_area": (area_g / area_construida * 100)
                    if area_construida > 0
                    else 0.0,
                }
            )

    return {
        "edificaciones": edificaciones,
        "por_grupo": por_grupo,
        "area_construida_m2": area_construida,
        "area_camp1_m2": area_camp1,
        "area_camp2_m2": area_camp2,
        "area_terreno_m2": area_terreno,
        "lado_terreno_m": math.sqrt(area_terreno),
        "total_edificaciones": len(edificaciones),
        "edif01_detalle": c.get("edif01_detalle", {}),
    }


def _tabla_edificaciones(edifs: list[dict], nota: str = "") -> Tabla:
    cols = [
        "Cód.",
        "Edificación",
        "Grupo Funcional",
        "Campamento",
        "Personas",
        "Módulos / Puestos",
        "Área (m²)",
        "Ancho (m)",
        "Largo (m)",
        "Norma / Criterio Aplicable",
    ]
    filas = [
        [
            e["id"],
            e["nombre"],
            e["grupo"],
            e["campamento"],
            e["personas"] if e["personas"] is not None else "N/A",
            e["modulos"],
            e["area_m2"],
            e["ancho_m"],
            e["largo_m"],
            e["norma"],
        ]
        for e in edifs
    ]
    tot_area = sum(e["area_m2"] for e in edifs)
    filas.append(
        [
            "TOTAL",
            f"Total {len(edifs)} edificaciones",
            "",
            "",
            "",
            "",
            tot_area,
            "",
            "",
            "Σ áreas construidas",
        ]
    )
    return Tabla(cols, filas, nota)


def libro(r: dict, p: dict) -> Libro:
    todas = _tabla_edificaciones(
        r["edificaciones"],
        "Catálogo completo de las 24 edificaciones del Proyecto Túnel Casmas Huaraz PA14.",
    )
    camp1 = _tabla_edificaciones(
        [e for e in r["edificaciones"] if e["campamento"] == "CAMP1"],
        "Edificaciones e instalaciones del Campamento 1 — Principal (Portal Entrada / Portal A - 248 pax).",
    )
    camp2 = _tabla_edificaciones(
        [e for e in r["edificaciones"] if e["campamento"] == "CAMP2"],
        "Edificaciones e instalaciones del Campamento 2 — Satélite (Portal Salida / Portal B - 98 pax).",
    )

    # Tabla de Grupos Funcionales
    cols_g = [
        "Grupo Funcional",
        "Edificaciones (Cód.)",
        "Cant. Edif.",
        "Área Total (m²)",
        "% del Total",
    ]
    filas_g = [
        [
            g["grupo"],
            g["edificaciones"],
            g["cantidad_edif"],
            g["area_m2"],
            f"{g['pct_area']:.1f} %",
        ]
        for g in r["por_grupo"]
    ]
    filas_g.append(
        [
            "TOTAL GENERAL",
            "EDIF-01 a EDIF-24",
            r["total_edificaciones"],
            r["area_construida_m2"],
            "100.0 %",
        ]
    )
    tabla_g = Tabla(
        cols_g,
        filas_g,
        "Consolidado de áreas techadas por grupo funcional de acuerdo al marco normativo RNE y D.S. 024-2016-EM.",
    )

    resumen = tabla_parametros(
        [
            (
                "Área construida total",
                "Ac",
                r["area_construida_m2"],
                "m²",
                "Σ de las 24 edificaciones",
            ),
            (
                "Área construida Campamento 1 (Principal)",
                "Ac1",
                r["area_camp1_m2"],
                "m²",
                "Portal A (248 pax)",
            ),
            (
                "Área construida Campamento 2 (Satélite)",
                "Ac2",
                r["area_camp2_m2"],
                "m²",
                "Portal B (98 pax)",
            ),
            (
                "Factor de terreno (vías, retiros, accesos)",
                "ft",
                p["campamento"]["factor_terreno"],
                "",
                "Dato normativo MTC EG-2013",
            ),
            (
                "Área de terreno requerida",
                "At",
                r["area_terreno_m2"],
                "m²",
                "Ac · ft",
            ),
            (
                "Lado equivalente de terreno (cuadrado)",
                "Lt",
                r["lado_terreno_m"],
                "m",
                "√At",
            ),
        ]
    )

    return Libro(
        "05_Campamento.xlsx",
        [
            Hoja(
                "Todas_Edificaciones",
                "Catálogo General de 24 Edificaciones",
                [todas],
            ),
            Hoja(
                "Campamento_1_Principal",
                "Campamento Principal Portal A (248 pax)",
                [camp1],
            ),
            Hoja(
                "Campamento_2_Satelite",
                "Campamento Satélite Portal B (98 pax)",
                [camp2],
            ),
            Hoja(
                "Resumen_Grupos",
                "Resumen por Grupos Funcionales y Terreno",
                [tabla_g, resumen],
            ),
        ],
    )


def memoria(r: dict, p: dict) -> Memoria:
    secciones = [
        (
            "1. Criterios Generales y Marco Normativo de Edificaciones",
            [
                "El campamento base y satélite del proyecto **Túnel Casmas Huaraz PA14** (5.538 km a 3,850 m s.n.m.) "
                f"han sido dimensionados para alojar a **346 trabajadores** en operación continua 24/7 (régimen 14×7), "
                f"cubriendo un área edificada total de **{r['area_construida_m2']:,.1f} m²** y un área de terreno proyectada "
                f"de **{r['area_terreno_m2']:,.1f} m²** a través de **38 edificaciones y áreas operativas especializadas (EDIF-01 a EDIF-38)**.",
                "### 1.1 Normativa Técnica Aplicable\n"
                "- **Reglamento Nacional de Edificaciones (RNE - Perú):**\n"
                "  - **Norma G.050 (Seguridad durante la Construcción):** Instalaciones provisionales, servicios higiénicos, vestuarios y comedores.\n"
                "  - **Norma A.010 (Condiciones Generales de Diseño y Cap. X Estacionamientos):** Alturas libres mínimas ($H \\ge 2.30\\text{ m}$), ventilación e iluminación; dimensionamiento y radios de giro para camionetas ($2.50 \\times 5.00\\text{ m}$) y buses ($3.50 \\times 12.00\\text{ m}$).\n"
                "  - **Norma A.060 (Industria y Almacenes):** Aplicable a la Nave Taller (EDIF-10 y EDIF-29), Bodegas de Repuestos (EDIF-11 y EDIF-33) y Patio de Maquinaria Pesada (EDIF-26), con altura libre de $7.0\\text{ m}$, tecle de 15 Tn y radios de giro $\\ge 15.0\\text{ m}$.\n"
                "  - **Norma A.070 (Hospedaje y Comedores):** Ratios de $1.20\\text{ m}^2/\\text{cama}$ (+ 20% circulación) en dormitorios y $1.50\\text{ m}^2/\\text{comensal pico}$ en comedores.\n"
                "  - **Norma A.080 (Oficinas):** Ratio de $8.0\\text{ m}^2/\\text{puesto de trabajo}$ para gerencia y supervisión técnica.\n"
                "  - **Norma IS.010 (Instalaciones Sanitarias):** Dotación de $129\\text{ L/pax/día}$ en sierra y 1 aparato sanitario cada 10 trabajadores.\n"
                "  - **Norma EM.010 (Instalaciones Eléctricas):** Iluminación (300 lux oficinas, 500 lux talleres) y tableros IP65.\n"
                "- **D.S. N° 024-2016-EM / D.S. N° 023-2017-EM (Seguridad Minera a 3,850 m s.n.m.):**\n"
                "  - Aislamiento térmico obligatorio (paneles termoacústicos con alma de poliuretano) y calefacción limpia.\n"
                "  - En el Campamento Satélite (CAMP2), los dormitorios (EDIF-03) integran directamente los servicios higiénicos, duchas calientes y casilleros (lockers) por módulo para evitar exposición a la intemperie a 3,850 msnm.\n"
                "  - Tópico médico de atención 24/7 (Art. 157) con camillas de reposo, balones de oxígeno medicinal y ambulancia Tipo II.\n"
                "  - Lampistería central en Portal A (EDIF-22) y lampistería satélite en garita Portal B (EDIF-36) con autorrescatadores (Art. 97).\n"
                "- **Ley N° 30299 / SUCAMEC:** Polvorines de superficie independientes (EDIF-23 en Portal A y EDIF-28 en Portal B) con parapetos de tierra, radio de seguridad de 300 m y casetas de vigilancia armada exclusiva 24/7 (EDIF-37 y EDIF-38).\n"
                "- **D.Leg. 1278 (Gestión Integral de Residuos Sólidos):** Centros CAT de acopio (EDIF-18 y EDIF-33) y compostaje (EDIF-19).\n"
                "- **MTC EG-2013 (Sección 104 - Campamentos y Patios de Maquinaria):** Emplazamiento seguro, estabilización de plataformas y drenaje pluvial perimetral.",
            ],
        ),
        (
            "2. Clasificación por Grupos Funcionales (EDIF-01 a EDIF-38)",
            [
                "| Grupo Funcional | Recintos (EDIF) | Cant. | Área Techada (m²) | % del Total | Alcance Normativo y Operativo |\n"
                "|---|---|---|---|---|---|\n"
                + "\n".join(
                    f"| **{g['grupo']}** | `{g['edificaciones']}` | {g['cantidad_edif']} | **{g['area_m2']:,.1f} m²** | {g['pct_area']:.1f} % | {g['grupo']} normativo RNE / DS 024 / MTC / SUCAMEC. |"
                    for g in r["por_grupo"]
                )
                + f"\n| **TOTAL CONSTRUIDO** | **EDIF-01 a EDIF-38** | **{r['total_edificaciones']}** | **{r['area_construida_m2']:,.1f} m²** | **100.0 %** | **Infraestructura total en ambos campamentos.** |"
            ],
        ),
        (
            "3. Distribución Geográfica por Campamentos",
            [
                "### 3.1 Campamento 1 — Principal (Portal A / Entrada — 248 personas)\n"
                f"- **Área construida:** **{r['area_camp1_m2']:,.1f} m²**\n"
                "- **Infraestructura centralizada:**\n"
                "  - **EDIF-01:** Pabellón de Dormitorios Staff e Ingeniería (73 pax).\n"
                "  - **EDIF-02:** Pabellón de Dormitorios Obreros A y B (175 pax).\n"
                "  - **EDIF-04:** Comedor Principal y Cocina Central (248 comensales en 2 turnos).\n"
                "  - **EDIF-06:** Oficinas Administrativas, Gerencia y Auditorio SSOMA.\n"
                "  - **EDIF-08:** Tópico Médico Central 24/7 y Ambulancia Tipo II.\n"
                "  - **EDIF-10:** Nave Taller Mecánico Principal (3 bahías para jumbos, scoops y volquetes).\n"
                "  - **EDIF-11:** Almacén Central de Repuestos e Insumos Críticos.\n"
                "  - **EDIF-12:** Lavandería Industrial y Ropería.\n"
                "  - **EDIF-13:** Módulo Recreativo, SUM y Gimnasio.\n"
                "  - **EDIF-14 / 15 / 16 / 17:** Planta de Saneamiento Completa (Pozo profundo 5 L/s, PTAP con reservorio 120 m³, PTAR MBBR y Trampas de grasa).\n"
                "  - **EDIF-18 / 19:** Manejo Ambiental (Centro CAT de residuos y Trincheras de compostaje).\n"
                "  - **EDIF-20 / 21:** Energía y Combustible (Casa de fuerza 2500 kVA y Estación de diésel 20,000 gal).\n"
                "  - **EDIF-22:** Change-House y Lampistería Portal A.\n"
                "  - **EDIF-23:** Polvorín de Superficie SUCAMEC Portal A.\n"
                "  - **EDIF-24:** Garita de Control y Balanza de Pesaje 80 Tn.\n"
                "  - **EDIF-25:** Playa de Estacionamiento de Vehículos Livianos y Buses (800 m²).\n"
                "  - **EDIF-26:** Patio de Parqueo y Maniobras de Maquinaria Pesada (1,500 m²).\n"
                "  - **EDIF-37:** Caseta de Seguridad y Custodia de Polvorín Principal (12 m²).\n\n"
                "### 3.2 Campamento 2 — Satélite Autónomo (Portal B / Salida — 98 personas)\n"
                f"- **Área construida:** **{r['area_camp2_m2']:,.1f} m²**\n"
                "- **Infraestructura satélite de total autonomía operativa:**\n"
                "  - **EDIF-03:** Pabellón de Dormitorios Satélite con duchas/servicios integrados (98 pax).\n"
                "  - **EDIF-05:** Comedor y Cocina Satélite (98 comensales en 2 turnos).\n"
                "  - **EDIF-07:** Oficinas Técnicas de Frente y Supervisión Portal B.\n"
                "  - **EDIF-09:** Puesto de Primeros Auxilios Satélite y Ambulancia de Respaldo.\n"
                "  - **EDIF-27:** Playa de Estacionamiento y Parqueo Auxiliar Portal B (400 m²).\n"
                "  - **EDIF-28:** Polvorín Satélite Certificado SUCAMEC (100 m² con parapetos).\n"
                "  - **EDIF-29:** Nave Taller Mecánico Auxiliar y Lubricación (200 m²).\n"
                "  - **EDIF-30:** Estación de Combustible Satélite (200 m², tanque 10,000 gal).\n"
                "  - **EDIF-31:** Casa de Fuerza Satélite y Generadores (120 m², grupo 1000 kVA).\n"
                "  - **EDIF-32:** Planta Compacta de Saneamiento Modular PTAP/PTAR (180 m²).\n"
                "  - **EDIF-33:** Bodega de Insumos Críticos y Acopio de Residuos CAT Satélite (120 m²).\n"
                "  - **EDIF-34:** Lavandería Satélite y Ropería (40 m²).\n"
                "  - **EDIF-35:** Módulo Recreativo y Sala de Usos Múltiples (120 m²).\n"
                "  - **EDIF-36:** Garita de Control de Acceso y Lampistería Satélite (30 m²).\n"
                "  - **EDIF-38:** Caseta de Seguridad y Custodia de Polvorín Satélite (12 m²).",
            ],
        ),
        (
            "4. Dimensionamiento Sanitario y Ambiental (Pozo, PTAP, PTAR y Trampas de Grasa)",
            [
                "- **EDIF-14 (Caseta de Pozo Profundo - CAMP1):** Captación subterránea con caudal de diseño de $5.0\\text{ L/s}$, electrobomba sumergible y tubería de impulsión de $\\varnothing 3''$.\n"
                "- **EDIF-15 (Planta PTAP y Reservorio 120 m³ - CAMP1):** Tratamiento mediante filtración multimedia y cloración por inyección dosificada; reservorio de concreto armado de $120\\text{ m}^3$ que garantiza regulación horaria y reserva contra incendios.\n"
                "- **EDIF-16 (Planta PTAR MBBR - CAMP1):** Sistema de lodos activados con bioportadores de lecho móvil (MBBR), sedimentador secundario y cámara de desinfección UV/cloro, con efluente cumpliendo los Estándares de Calidad Ambiental (ECA) para agua (D.S. 004-2017-MINAM).\n"
                "- **EDIF-17 (Trampas de Grasa - CAMP1):** Unidades de retención gravimétrica de grasas y aceites provenientes de la cocina industrial antes del ingreso al colector biológico.\n"
                "- **EDIF-32 (Saneamiento Compacto - CAMP2):** Módulos compactos contenerizados de potabilización (PTAP 2 L/s) y tratamiento biológico compacto (PTAR MBBR 1.5 L/s) para los 98 ocupantes del Portal B.",
            ],
        ),
        (
            "5. Dimensionamiento de Estacionamientos y Patios de Maniobra de Maquinaria",
            [
                "- **EDIF-25 (Playa de Estacionamiento Livianos y Buses - CAMP1, 800 m²):** Diseñado conforme a la norma RNE A.010 (Cap. X). Incluye 20 cajones de $2.50 \\times 5.00\\text{ m}$ para camionetas 4x4 de staff, supervisión y visitas, más 4 bahías de $3.50 \\times 12.00\\text{ m}$ para buses interurbanos de cambio de guardia (14x7) con calles de circulación de $6.00\\text{ m}$ y radio de giro adecuado.\n"
                "- **EDIF-26 (Patio de Parqueo de Maquinaria Pesada - CAMP1, 1,500 m²):** Ubicado estratégicamente contiguo a la Nave Taller (EDIF-10) y la Estación de Combustible (EDIF-21). Plataforma estabilizada con subbase granular de $0.30\\text{ m}$ y losa/afirmado para soportar cargas por eje de volquetes de 20 m³, Jumbos electrohidráulicos y Scooptrams LHD, con radio libre de giro $\\ge 15.00\\text{ m}$ y canaletas perimetrales conectadas a trampa de hidrocarburos.\n"
                "- **EDIF-27 (Playa de Estacionamiento y Parqueo Auxiliar - CAMP2, 400 m²):** Destinado al Frente 2 (Portal B). Cuenta con 8 cajones para camionetas técnicas, 2 bahías para minibuses de traslado de guardia y zona de parqueo transitorio para 2 volquetes y cargador frontal.",
            ],
        ),
        (
            "6. Autonomía Logística y Polvorín Satélite del Frente 2 (Portal B)",
            [
                "Debido a la longitud del túnel ($L = 5.538\\text{ km}$) a través de un macizo cordillerano escarpado, la comunicación vial superficial entre el Portal A y el Portal B tomaría más de 2.5 horas por trocha carrozable de alta montaña. Por tanto, conforme a las mejores prácticas de ingeniería de túneles y normativas SUCAMEC / D.S. 024-2016-EM:",
                "- **Polvorín Satélite (EDIF-28, 100 m²) y Caseta de Custodia (EDIF-38, 12 m²):** Almacenamiento directo de emulsión encartuchada, dinamita y accesorios de voladura con parapetos perimetrales de tierra, distanciamiento de seguridad normativo de 300 m y vigilancia armada permanente in situ.\n"
                "- **Mantenimiento y Combustible Local (EDIF-29 y EDIF-30):** Permite el mantenimiento preventivo diario (cambio de brocas, mangueras hidráulicas, lubricación) y repostaje de diésel sin desplazar la maquinaria pesada al Portal A, evitando tiempos muertos y sobrecostos de traslado.\n"
                "- **Energía Continua Satélite (EDIF-31):** Generador diésel de 1000 kVA insonorizado que garantiza bombeo de achique, iluminación del frente y habitabilidad continua en el Campamento 2.",
            ],
        ),
        (
            "7. Servicios de Habitabilidad y Bienestar en Campamento 2",
            [
                "Con el fin de asegurar el confort térmico y la salud de los trabajadores en condiciones de alta montaña (3,850 msnm), el diseño de habitabilidad del Campamento 2 contempla:",
                "- **Duchas y Cambio Térmico Integrado en Dormitorios (EDIF-03):** Los trabajadores se cambian y asean dentro de los mismos módulos climatizados de dormitorios, evitando el choque térmico de desplazarse a la intemperie hacia una nave change-house desvinculada.\n"
                "- **Lavandería Satélite (EDIF-34, 40 m²):** Equipamiento industrial de lavado y secado continuo para la ropa térmica y de trabajo de los 98 ocupantes.\n"
                "- **Módulo Recreativo y SUM (EDIF-35, 120 m²):** Espacio de relajación y esparcimiento con televisor satelital, internet y área de lectura para prevenir el estrés por aislamiento en régimen 14×7.\n"
                "- **Garita y Lampistería Satélite (EDIF-36, 30 m²):** Módulo de control de accesos al Portal B que aloja el rack de carga para 40 lámparas mineras y entrega de autorrescatadores.",
            ],
        ),
        (
            "8. Sistema de Seguridad Integral y Custodia de Polvorines",
            [
                "Conforme a la Ley N° 30299 (SUCAMEC) y el D.S. 024-2016-EM, la seguridad patrimonial y de explosivos se estructura en dos niveles:",
                "- **Control de Accesos a Campamentos (EDIF-24 y EDIF-36):** Garitas en los ingresos vehiculares con control biométrico, registro de visitas y pesaje de camiones en balanza de 80 t en el Portal A.\n"
                "- **Custodia Exclusiva 24/7 de Polvorines (EDIF-37 y EDIF-38):** Casetas de vigilancia blindadas ubicadas a pie de parapeto de los polvorines (aislados a 300 m del campamento), dotadas de radio troncalizado, reflector perimetral y guardia armado continuo.",
            ],
        ),
    ]
    return Memoria(
        "05_Campamento.md", "Campamento y Edificaciones Especializadas", secciones
    )
