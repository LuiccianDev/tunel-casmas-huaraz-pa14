"""Construcción de tablas y libro Excel para 09 · Electricidad."""

from ...modelo import Hoja, Libro, Tabla, tabla_parametros


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
                "=IF({z}<=1500,3,IF({z}<=3000,4,IF({z}<=4000,5,6)))",
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
            ("Caudal por personas", "Q1", "={n}*{qp}", "m³/min", "n · qp"),
            (
                "Potencia diésel en el frente (06_Maquinaria)",
                "HPf",
                r["hp_tunel_frente"],
                "HP",
                "06_Maquinaria",
            ),
            (
                "Caudal por equipos diésel",
                "Q2",
                f"={{HPf}}*{v['caudal_por_hp_m3_min']}*{v['simultaneidad_equipos']}",
                "m³/min",
                "HP en túnel · 3 · simultaneidad",
            ),
            (
                "Caudal requerido",
                "Qr",
                f"=({{Q1}}+{{Q2}})*{v['factor_fugas']}",
                "m³/min",
                "(Q1 + Q2) · f fugas",
            ),
            (
                "Área de la sección del túnel (03_Seccion)",
                "Asec",
                r["area_seccion_m2"],
                "m²",
                "03_Seccion",
            ),
            ("Velocidad del aire", "v", "={Qr}/{Asec}", "m/min", "Qr / A"),
            (
                "¿Velocidad dentro de límites?",
                "Cumple_v",
                f'=IF(AND({{v}}>={v["velocidad_min_m_min"]}, {{v}}<={v["velocidad_max_m_min"]}), "Sí", "No")',
                "-",
                f"{v['velocidad_min_m_min']:.0f} ≤ v ≤ {v['velocidad_max_m_min']:.0f}",
            ),
            (
                "Potencia del ventilador",
                "Pv",
                f"={{Qr}}/60*{v['presion_total_pa']}/{v['eficiencia_ventilador']}/1000",
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
                f"Σ {n_ilum} edificaciones especializadas",
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
