"""09 · Electricidad: ventilación, cargas dinámicas, demanda y grupo electrógeno."""

import math

from ..modelo import Hoja, Libro, Tabla, tabla_parametros

CLAVE = "electricidad"
GRUPOS_KVA = [100, 150, 200, 250, 300, 400, 500, 625, 750, 1000, 1250, 1500, 2000, 2500]


def caudal_por_persona(altitud: float) -> float:
    """m³/min por persona según altitud (DS 024-2016-EM)."""
    if altitud <= 1500:
        return 3.0
    if altitud <= 3000:
        return 4.0
    if altitud <= 4000:
        return 5.0
    return 6.0


def grupo_comercial(kva: float) -> int:
    """Primer tamaño comercial de grupo electrógeno ≥ kva."""
    return next((g for g in GRUPOS_KVA if g >= kva), GRUPOS_KVA[-1])


def calcular(p: dict, ctx: dict) -> dict:
    v, e = p["ventilacion"], p["electricidad"]
    frentes = p["perforacion"]["frentes"]

    # Ventilación (por frente)
    q_persona = caudal_por_persona(p["proyecto"]["altitud_msnm"])
    personas = ctx["personal"]["frente_por_guardia"]
    q_personas = personas * q_persona
    q_equipos = (
        ctx["maquinaria"]["hp_tunel_frente"]
        * v["caudal_por_hp_m3_min"]
        * v["simultaneidad_equipos"]
    )
    q_total = (q_personas + q_equipos) * v["factor_fugas"]
    velocidad = q_total / ctx["seccion"]["area_m2"]
    p_vent = q_total / 60 * v["presion_total_pa"] / v["eficiencia_ventilador"] / 1000

    # 1. Iluminación interior dinámica por edificación según reglas del TOML
    reglas = e.get("iluminacion_reglas", {})
    regla_defecto = reglas.get(
        "Defecto",
        {
            "tipo": "Luminarias LED 20W",
            "potencia_kw": 0.020,
            "por_modulo": 0,
            "area_por_foco_m2": 15.0,
            "horas_dia": 12.0,
            "factor_demanda": 0.60,
            "norma": "RNE EM.010 (150 lux)",
        },
    )

    edifs = ctx["campamento"]["edificaciones"]
    detalle_iluminacion = []

    for edif in edifs:
        gid = edif.get("id", "")
        gnombre = edif.get("nombre", "")
        ggrupo = edif.get("grupo", "")
        area = edif.get("area_m2", 0.0)
        modulos = edif.get("modulos", 1)

        # Regla según grupo funcional configurado en TOML
        r = reglas.get(ggrupo, regla_defecto)
        por_mod = r.get("por_modulo", 0)

        if por_mod > 0:
            cant = modulos * por_mod
        else:
            area_foco = r.get("area_por_foco_m2", 15.0)
            cant = math.ceil(area / area_foco) if area_foco > 0 else 1

        tipo = r["tipo"]
        pot_unit = r["potencia_kw"]
        fd = r["factor_demanda"]
        horas = r["horas_dia"]
        norma = r["norma"]

        dem_kw = cant * pot_unit * fd
        detalle_iluminacion.append(
            {
                "id": gid,
                "nombre": gnombre,
                "campamento": edif["campamento"],
                "grupo": ggrupo,
                "area_m2": area,
                "tipo": tipo,
                "cantidad": cant,
                "kw": pot_unit,
                "fd": fd,
                "demanda_kw": dem_kw,
                "horas": horas,
                "kwh_dia": dem_kw * horas,
                "norma": norma,
            }
        )

    # 2. Luces de afueras (iluminación perimetral y accesos de campamentos)
    ext_cfg = e["exterior"]
    esp_ext = ext_cfg["espaciamiento_reflectores_m"]
    pot_reflector = ext_cfg["potencia_reflector_kw"]
    horas_ext = ext_cfg["horas_dia"]
    fd_ext = ext_cfg["factor_demanda"]

    lado_terr = ctx["campamento"]["lado_terreno_m"]
    perim_terr = 4 * lado_terr
    n_reflectores_ext = math.ceil(perim_terr / esp_ext)

    # Agrupación de iluminación interior por grupo funcional para el Cuadro de Cargas
    grupos_ilum: dict[str, dict] = {}
    for d in detalle_iluminacion:
        cat = d["grupo"]
        if cat not in grupos_ilum:
            grupos_ilum[cat] = {
                "cantidad": 0,
                "kw_total": 0.0,
                "demanda_kw": 0.0,
                "kwh_dia": 0.0,
                "horas": d["horas"],
            }
        grupos_ilum[cat]["cantidad"] += d["cantidad"]
        grupos_ilum[cat]["kw_total"] += d["cantidad"] * d["kw"]
        grupos_ilum[cat]["demanda_kw"] += d["demanda_kw"]
        grupos_ilum[cat]["kwh_dia"] += d["kwh_dia"]

    cargas_iluminacion_resumen = []
    for cat, gdata in grupos_ilum.items():
        kw_prom = (
            gdata["kw_total"] / gdata["cantidad"] if gdata["cantidad"] > 0 else 0.02
        )
        fd_prom = (
            gdata["demanda_kw"] / gdata["kw_total"] if gdata["kw_total"] > 0 else 0.70
        )
        cargas_iluminacion_resumen.append(
            (
                "Campamento - Iluminación",
                f"Alumbrado interior: {cat}",
                gdata["cantidad"],
                kw_prom,
                fd_prom,
                gdata["horas"],
            )
        )

    # 3. Cargas de fuerza dinámicas calculadas por ratios y dimensiones
    eq = e["ratios_equipos"]
    pob_total = ctx["personal"]["total"]
    area_techada_total = sum(edif.get("area_m2", 0.0) for edif in edifs)

    def area_de_grupo(nombre_grupo: str) -> float:
        return sum(ed["area_m2"] for ed in edifs if ed.get("grupo") == nombre_grupo)

    area_taller = area_de_grupo("Maquinaria y Mantenimiento")
    area_oficinas = area_de_grupo("Administración y Documentos")
    area_salud = area_de_grupo("Salud y Bienestar")
    l_tunel = ctx["ubicacion"]["longitud_m"]

    # Cargas dinámicas de Frente y Túnel
    cargas_frente = [
        (
            "Frente",
            "Ventilador principal túnel",
            1,
            True,
            round(p_vent, 2),
            24.0,
            1.00,
        ),
        (
            "Frente",
            "Jumbo electrohidráulico (perforación)",
            1,
            True,
            eq["kw_jumbo_frente"],
            eq["horas_jumbo"],
            eq["fd_jumbo"],
        ),
        (
            "Frente",
            "Compresora eléctrica estacionaria",
            1,
            True,
            eq["kw_compresora_frente"],
            eq["horas_compresora"],
            eq["fd_compresora"],
        ),
        (
            "Frente",
            "Electrobomba de drenaje y achique",
            1,
            True,
            eq["kw_bomba_drenaje_frente"],
            eq["horas_drenaje"],
            eq["fd_drenaje"],
        ),
        (
            "Frente",
            f"Iluminación continua túnel ({l_tunel:.0f} m)",
            1,
            False,
            round(l_tunel * eq["kw_iluminacion_tunel_por_m"], 2),
            eq["horas_ilum_tunel"],
            eq["fd_ilum_tunel"],
        ),
    ]

    # Cargas dinámicas de Exteriores y Botadero
    cargas_exteriores = [
        (
            "Botadero",
            "Torres móviles de iluminación LED en botadero",
            eq["torres_botadero_cant"],
            False,
            eq["kw_torre_botadero"],
            eq["horas_botadero"],
            eq["fd_botadero"],
        ),
        (
            "Campamento - Afueras",
            f"Alumbrado perimetral ({perim_terr:.0f} m perím., reflectores LED 100W)",
            n_reflectores_ext,
            False,
            pot_reflector,
            horas_ext,
            fd_ext,
        ),
    ]

    # Cargas dinámicas de Agua y Saneamiento
    cargas_agua = [
        (
            "Campamento - Servicios",
            "Bomba de pozo profundo (captación agua subterránea)",
            1,
            False,
            round(ctx["agua"]["p_bomba_kw"], 2),
            p["pozo"]["horas_bombeo"],
            1.00,
        ),
        (
            "Campamento - Servicios",
            "Equipos dosificadores y bombas de PTAP",
            1,
            False,
            round(ctx["agua"]["p_ptap_kw"], 2),
            24.0,
            0.80,
        ),
        (
            "Campamento - Servicios",
            "Sopladores de aireación y bombas de PTAR",
            1,
            False,
            round(ctx["agua"]["p_ptar_kw"], 2),
            24.0,
            0.80,
        ),
    ]

    # Cargas dinámicas de Campamento
    cargas_campamento = [
        (
            "Campamento - Equipos",
            f"Cocina industrial ({pob_total} personas)",
            1,
            False,
            round(pob_total * eq["kw_cocina_por_persona"], 2),
            eq["horas_cocina"],
            eq["fd_cocina"],
        ),
        (
            "Campamento - Equipos",
            f"Lavandería industrial ({pob_total} personas)",
            1,
            False,
            round(pob_total * eq["kw_lavanderia_por_persona"], 2),
            eq["horas_lavanderia"],
            eq["fd_lavanderia"],
        ),
        (
            "Campamento - Equipos",
            f"Fuerza menor y tomacorrientes ({area_techada_total:.0f} m² techados)",
            1,
            False,
            round(area_techada_total * eq["kw_tomacorrientes_m2"], 2),
            eq["horas_tomacorrientes"],
            eq["fd_tomacorrientes"],
        ),
        (
            "Campamento - Equipos",
            f"Taller de mantenimiento electromecánico ({area_taller:.0f} m²)",
            1,
            False,
            round(area_taller * eq["kw_taller_por_m2"], 2),
            eq["horas_taller"],
            eq["fd_taller"],
        ),
        (
            "Campamento - Equipos",
            f"Oficinas técnicas y servidores ({area_oficinas:.0f} m²)",
            1,
            False,
            round(area_oficinas * eq["kw_oficinas_por_m2"], 2),
            eq["horas_oficinas"],
            eq["fd_oficinas"],
        ),
        (
            "Campamento - Equipos",
            f"Tópico médico y salud ocupacional ({area_salud:.0f} m²)",
            1,
            False,
            round(area_salud * eq["kw_topico_por_m2"], 2),
            eq["horas_topico"],
            eq["fd_topico"],
        ),
    ]

    todas_cargas_fuerza = (
        cargas_frente + cargas_exteriores + cargas_agua + cargas_campamento
    )

    filas = []
    for zona, equipo, cant, por_frente, kw, horas, fd in todas_cargas_fuerza:
        n = cant * frentes if por_frente else cant
        demanda = round(n * kw * fd, 2)
        filas.append(
            {
                "zona": zona,
                "equipo": equipo,
                "cantidad": n,
                "kw": kw,
                "fd": fd,
                "demanda_kw": demanda,
                "horas": horas,
                "kwh_dia": round(demanda * horas, 2),
            }
        )

    # Añadir iluminación interior agrupada al cuadro de cargas
    for zona, equipo, cant, kw, fd, horas in cargas_iluminacion_resumen:
        demanda = round(cant * kw * fd, 2)
        filas.append(
            {
                "zona": zona,
                "equipo": equipo,
                "cantidad": cant,
                "kw": round(kw, 3),
                "fd": round(fd, 2),
                "demanda_kw": demanda,
                "horas": horas,
                "kwh_dia": round(demanda * horas, 2),
            }
        )

    demanda = sum(f["demanda_kw"] for f in filas)
    energia = sum(f["kwh_dia"] for f in filas)
    kva = demanda / e["factor_potencia"] * (1 + e["reserva"])
    return {
        "q_persona": q_persona,
        "personas": personas,
        "q_personas": q_personas,
        "q_equipos": q_equipos,
        "q_total": q_total,
        "velocidad": velocidad,
        "cumple_velocidad": v["velocidad_min_m_min"]
        <= velocidad
        <= v["velocidad_max_m_min"],
        "p_ventilador_kw": p_vent,
        "detalle_iluminacion": detalle_iluminacion,
        "total_focos_interiores": sum(d["cantidad"] for d in detalle_iluminacion),
        "reflectores_exteriores": n_reflectores_ext,
        "perimetro_terreno_m": perim_terr,
        "cargas": filas,
        "demanda_kw": demanda,
        "energia_kwh_dia": energia,
        "kva_requerido": kva,
        "grupo_kva": grupo_comercial(kva),
        "combustible_l_dia": energia * e["consumo_combustible_l_kwh"],
    }


def libro(r: dict, p: dict) -> Libro:
    v, e = p["ventilacion"], p["electricidad"]
    ext_cfg = e["exterior"]
    esp_ext = ext_cfg["espaciamiento_reflectores_m"]

    ventilacion = tabla_parametros(
        [
            ("Altitud", "z", p["proyecto"]["altitud_msnm"], "msnm", "Dato"),
            (
                "Caudal por persona",
                "qp",
                r["q_persona"],
                "m³/min",
                "DS 024-2016-EM según altitud",
            ),
            (
                "Personas en el frente (por guardia)",
                "n",
                r["personas"],
                "und",
                "04_Personal",
            ),
            ("Caudal por personas", "Q1", "=C8*C7", "m³/min", "n · qp"),
            (
                "Caudal por equipos diésel",
                "Q2",
                r["q_equipos"],
                "m³/min",
                "HP en túnel · 3 · simultaneidad",
            ),
            (
                "Caudal requerido",
                "Qr",
                f"=(C9+C10)*{v['factor_fugas']}",
                "m³/min",
                "(Q1 + Q2) · f fugas",
            ),
            ("Velocidad del aire", "v", "=C11/108.43", "m/min", "Qr / A"),
            (
                "¿Velocidad dentro de límites?",
                "",
                r["cumple_velocidad"],
                "",
                f"{v['velocidad_min_m_min']:.0f} ≤ v ≤ {v['velocidad_max_m_min']:.0f}",
            ),
            (
                "Potencia del ventilador",
                "Pv",
                f"=C11/60*{v['presion_total_pa']}/{v['eficiencia_ventilador']}/1000",
                "kW",
                "Qr/60 · ΔP / η / 1000",
            ),
        ],
        "Por frente",
    )

    n_ilum = len(r["detalle_iluminacion"])
    filas_ilum = []
    for i, d in enumerate(r["detalle_iluminacion"]):
        fila_excel = 6 + i
        filas_ilum.append(
            [
                d["id"],
                d["nombre"],
                d["campamento"],
                d["grupo"],
                round(d["area_m2"], 1),
                d["tipo"],
                d["cantidad"],
                d["kw"],
                f"=G{fila_excel}*H{fila_excel}*{d['fd']:.2f}",
                d["norma"],
            ]
        )

    fila_total_ilum = 6 + n_ilum
    filas_ilum.append(
        [
            "TOTAL",
            "Total iluminación campamento",
            "",
            "",
            f"=SUM(E6:E{fila_total_ilum - 1})",
            "",
            f"=SUM(G6:G{fila_total_ilum - 1})",
            "",
            f"=SUM(I6:I{fila_total_ilum - 1})",
            "",
        ]
    )

    tabla_iluminacion = Tabla(
        [
            "Código",
            "Edificación / Ambiente",
            "Campamento",
            "Grupo Funcional",
            "Área (m²)",
            "Tipo Luminaria",
            "Focos / Lámparas",
            "Potencia (kW)",
            "Demanda (kW)",
            "Norma / Criterio",
        ],
        filas_ilum,
        "Cálculo dinámico ambiente por ambiente según RNE EM.010 / DS 024-2016-EM",
    )

    resumen_ilum = tabla_parametros(
        [
            (
                "Total focos interiores en campamento",
                "Nfi",
                f"='Iluminacion'!G{fila_total_ilum}",
                "und",
                "Σ 24 edificaciones especializadas",
            ),
            (
                "Perímetro de terreno de campamentos",
                "P",
                r["perimetro_terreno_m"],
                "m",
                "4 · lado del terreno",
            ),
            (
                "Reflectores exteriores (luces de afueras)",
                "Next",
                f"=ROUNDUP(C{fila_total_ilum + 5}/{esp_ext}, 0)",
                "und",
                f"P / {esp_ext:.0f} m (Reflectores LED 100W IP65)",
            ),
        ],
        "Resumen del sistema de iluminación",
    )

    n_cargas = len(r["cargas"])
    filas_cargas = []
    for i, c in enumerate(r["cargas"]):
        fila_excel = 6 + i
        filas_cargas.append(
            [
                c["zona"],
                c["equipo"],
                c["cantidad"],
                c["kw"],
                c["fd"],
                f"=C{fila_excel}*D{fila_excel}*E{fila_excel}",
                c["horas"],
                f"=F{fila_excel}*G{fila_excel}",
            ]
        )

    fila_total_cargas = 6 + n_cargas
    filas_cargas.append(
        [
            "TOTAL",
            "Máxima Demanda y Consumo Total",
            "",
            "",
            "",
            f"=SUM(F6:F{fila_total_cargas - 1})",
            "",
            f"=SUM(H6:H{fila_total_cargas - 1})",
        ]
    )

    cargas = Tabla(
        [
            "Zona",
            "Equipo / carga",
            "Cantidad",
            "Potencia unit. (kW)",
            "F. demanda",
            "Demanda (kW)",
            "Horas/día",
            "Energía (kWh/día)",
        ],
        filas_cargas,
        "Demanda = cantidad · potencia · f. demanda · Energía = demanda · horas (CNE Utilización Sección 050)",
    )

    resumen = tabla_parametros(
        [
            (
                "Máxima demanda",
                "MD",
                f"='Cargas'!F{fila_total_cargas}",
                "kW",
                "Σ demandas (CNE Sección 050)",
            ),
            (
                "Consumo de energía diario",
                "E",
                f"='Cargas'!H{fila_total_cargas}",
                "kWh/día",
                "Σ energías (kWh/día)",
            ),
            (
                "Consumo de energía mensual",
                "Em",
                "=C7*30",
                "kWh/mes",
                "E · 30 días",
            ),
            (
                "Potencia aparente requerida",
                "S",
                f"=C6/{e['factor_potencia']}*(1+{e['reserva']})",
                "kVA",
                f"MD / {e['factor_potencia']} · (1 + {e['reserva']}) (CNE)",
            ),
            (
                "Grupo electrógeno comercial",
                "G",
                r["grupo_kva"],
                "kVA",
                "Tamaño comercial normalizado ≥ S (ISO 8528)",
            ),
            (
                "Consumo de combustible",
                "Cc",
                f"=C7*{e['consumo_combustible_l_kwh']}",
                "L/día",
                "E · consumo específico diésel",
            ),
        ],
        "Balance de potencia y grupo electrógeno (CNE Utilización / ISO 8528)",
    )
    return Libro(
        "09_Electricidad.xlsx",
        [
            Hoja("Ventilacion", "Ventilación del túnel", [ventilacion]),
            Hoja(
                "Iluminacion",
                "Iluminación detallada por edificación",
                [tabla_iluminacion, resumen_ilum],
            ),
            Hoja("Cargas", "Cuadro de cargas dinámicas y fuerza", [cargas]),
            Hoja("Resumen", "Consumo eléctrico y grupo electrógeno", [resumen]),
        ],
    )
