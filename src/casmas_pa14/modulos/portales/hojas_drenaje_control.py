"""Hojas de drenaje pluvial Manning y control de tiempos por progresiva para 11_Portales.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Tabla


def construir_hoja_cunetas(resultados: dict[str, Any]) -> Hoja | None:
    """Construye la hoja de diseño y verificación hidráulica de cunetas pluviales."""
    drenaje = resultados.get("drenaje_cunetas")
    if not drenaje:
        return None

    cols_hidro = [
        "Parámetro Hidrológico / Hidráulico",
        "Símbolo",
        "Valor",
        "Unidad",
        "Norma / Criterio de Diseño",
    ]
    filas_hidro = [
        [
            "Periodo de Retorno de Diseño",
            "Tr",
            drenaje["periodo_retorno_anos"],
            "años",
            "Manual de Hidrología e Hidráulica MTC (Cunetas y Drenaje Superficial)",
        ],
        [
            "Intensidad Máxima de Precipitación",
            "I",
            drenaje["intensidad_lluvia_mm_h"],
            "mm/h",
            "Isoyeta horaria de diseño - Estación Huaraz / Cuenca Casmas",
        ],
        [
            "Coeficiente de Escorrentía Medio",
            "C",
            drenaje["coeficiente_escorrentia"],
            "-",
            "Calzada compactada y taludes rocosos de desmonte",
        ],
        [
            "Coeficiente de Rugosidad de Manning",
            "n",
            drenaje["rugosidad_manning"],
            "-",
            "Cuneta de concreto simple f'c=175 kg/cm2 frotachado",
        ],
        [
            "Velocidad Mínima Permisible",
            "V_min",
            drenaje["velocidad_min_m_s"],
            "m/s",
            "Velocidad no sedimentable para arenas y limos (MTC)",
        ],
        [
            "Velocidad Máxima Permisible",
            "V_max",
            drenaje["velocidad_max_m_s"],
            "m/s",
            "Límite para evitar abrasión y cavitación en concreto",
        ],
        [
            "Borde Libre / Revancha Mínima",
            "BL_min",
            drenaje["borde_libre_min_m"],
            "m",
            "Margen de seguridad contra olas y colmatación",
        ],
    ]

    cols_cunetas = [
        "Tipo / Tramo de Cuneta",
        "Ancho T (m)",
        "Prof. H (m)",
        "Pendiente S (%)",
        "Longitud L (m)",
        "Área Cuenca (ha)",
        "Caudal Diseño Qp (l/s)",
        "Capacidad Máx Qmax (l/s)",
        "Tirante Normal yn (cm)",
        "Borde Libre BL (cm)",
        "Velocidad V (m/s)",
        "Froude Fr",
        "Factor Seg. (Qmax/Qp)",
        "Estado Normativo",
    ]

    filas_cunetas = []
    for c in drenaje.get("cunetas", []):
        filas_cunetas.append(
            [
                c["nombre"],
                c["ancho_superior_m"],
                c["profundidad_total_m"],
                c["pendiente_pct"],
                c["longitud_m"],
                c["area_cuenca_ha"],
                c["caudal_diseno_l_s"],
                c["capacidad_max_l_s"],
                c["tirante_normal_cm"],
                c["borde_libre_cm"],
                c["velocidad_flujo_m_s"],
                c["froude"],
                c["factor_seguridad_hidraulico"],
                c["estado_normativo"],
            ]
        )

    return Hoja(
        nombre="Cunetas_Drenaje_Pluvial",
        titulo="Diseño y Verificación Hidráulica de Cunetas de Drenaje (Fórmula de Manning & Método Racional)",
        tablas=[
            Tabla(
                cols_hidro,
                filas_hidro,
                "Criterios Hidrológicos y Parámetros de Diseño MTC",
            ),
            Tabla(
                cols_cunetas,
                filas_cunetas,
                "Comprobación de Tirante Normal, Velocidad Límite y Borde Libre",
            ),
        ],
    )


def construir_hoja_control_progresivas(resultados: dict[str, Any]) -> Hoja | None:
    ctrl = resultados.get("control_progresivas")
    if not ctrl:
        return None

    cols = [
        "Sector de Obra Exterior",
        "Progresiva (Tramo)",
        "Longitud L (m)",
        "Vol. Banco (m³)",
        "Vol. Suelto (m³)",
        "N° Viajes (16m³)",
        "Dist. Botadero (m)",
        "Ciclo Volquete (min)",
        "Rend. Flota (m³b/h)",
        "Horas Acarreo (h)",
        "Horas Cunetas (h)",
        "Guardias (10.5h)",
        "Días (2 g/d)",
    ]

    filas = []
    fila_actual = 5

    for s in ctrl["sectores"]:
        fila_inicio_sec = fila_actual
        for t in s["tramos"]:
            filas.append(
                [
                    s["sector"],
                    t["progresiva"],
                    t["longitud_m"],
                    t["vol_banco_m3"],
                    t["vol_suelto_m3"],
                    t["viajes"],
                    t["distancia_botadero_m"],
                    t["ciclo_volquete_min"],
                    t["rendimiento_flota_m3_h"],
                    t["horas_acarreo"],
                    t["horas_cuneta"],
                    t["guardias"],
                    t["dias"],
                ]
            )
            fila_actual += 1

        fila_fin_sec = fila_actual - 1
        filas.append(
            [
                f"SUBTOTAL {s['sector'].upper()}",
                "Resumen Sector",
                f"=SUM(C{fila_inicio_sec}:C{fila_fin_sec})",
                f"=SUM(D{fila_inicio_sec}:D{fila_fin_sec})",
                f"=SUM(E{fila_inicio_sec}:E{fila_fin_sec})",
                f"=SUM(F{fila_inicio_sec}:F{fila_fin_sec})",
                f"=AVERAGE(G{fila_inicio_sec}:G{fila_fin_sec})",
                f"=AVERAGE(H{fila_inicio_sec}:H{fila_fin_sec})",
                f"=AVERAGE(I{fila_inicio_sec}:I{fila_fin_sec})",
                f"=SUM(J{fila_inicio_sec}:J{fila_fin_sec})",
                f"=SUM(K{fila_inicio_sec}:K{fila_fin_sec})",
                f"=SUM(L{fila_inicio_sec}:L{fila_fin_sec})",
                f"=SUM(M{fila_inicio_sec}:M{fila_fin_sec})",
            ]
        )
        fila_actual += 1

    filas.append(
        [
            "TOTAL GENERAL OBRAS EXTERIORES",
            "5 Alineamientos Civil 3D",
            f"{ctrl['total_vol_banco_m3']:.2f} m3 in-situ",
            ctrl["total_vol_banco_m3"],
            ctrl["total_vol_suelto_m3"],
            ctrl["total_viajes"],
            740.0,
            6.25,
            386.3,
            ctrl["total_horas"],
            45.0,
            ctrl["total_guardias"],
            ctrl["total_dias"],
        ]
    )

    cols_resumen = [
        "Fase de Obra Exterior",
        "Alineamiento Principal",
        "Volumen Banco (m³)",
        "Equipo Clave Asignado",
        "Guardias (10.5 h)",
        "Días Netos Acarreo",
        "Días Ciclo Completo (*)",
        "Precedencia Lógica",
    ]
    filas_resumen = [
        [
            "Fase 1: Vía al Botadero",
            "ALINEAMIENTO-BOTADERO-B",
            10191.80,
            "CAT 966H + 4 Volvo FMX + D8T",
            2.3,
            1.2,
            2.0,
            "Inicio Obra Exterior",
        ],
        [
            "Fase 2: Rampas a Banquetas",
            "ACCESO-BANQUETA-1 / 2",
            12461.12,
            "Epiroc T25 + CAT 966H + 4 Volvo",
            3.4,
            1.7,
            3.0,
            "Predecesora: Fase 1",
        ],
        [
            "Fase 3: Banqueo Frontón Túnel",
            "BANQUETAS-TUNEL (Frontón)",
            24245.14,
            "Epiroc T25 + CAT 966H + Shotcrete",
            5.7,
            2.9,
            6.0,
            "Predecesora: Fase 2",
        ],
        [
            "Fase 4: Acceso Túnel y Emboquille",
            "ACCESO-TUNEL-B",
            29059.78,
            "CAT 966H + CAT 336D + 4 Volvo FMX",
            7.4,
            3.7,
            4.5,
            "Predecesora: Fase 3",
        ],
        [
            "TOTAL ACTIVIDAD D (CRONOGRAMA)",
            "Obras Exteriores y Accesos",
            ctrl["total_vol_banco_m3"],
            "Tren Pesado Completo",
            ctrl["total_guardias"],
            ctrl["total_dias"],
            15.5,
            "Habilita Ingreso Jumbo (Act. E)",
        ],
    ]

    return Hoja(
        nombre="Control_Tiempos_Progresivas",
        titulo="Control de Tiempos Tramo a Tramo por Progresiva y Flota de Equipos (Civil 3D & Manning)",
        tablas=[
            Tabla(
                cols,
                filas,
                "Desglose por Progresiva (Corte, Acarreo Volvo FMX y Cunetas CAT 336D)",
            ),
            Tabla(
                cols_resumen,
                filas_resumen,
                "Resumen de Fases y Precedencias de Obras Exteriores (Actividad D)",
            ),
        ],
    )
