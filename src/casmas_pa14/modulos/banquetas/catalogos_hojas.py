"""Catálogos y tablas de referencia para el libro 15_Voladura_Banquetas.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Tabla


def construir_tablas_catalogos_banquetas(
    vol_p: dict[str, Any], vb_p: dict[str, Any]
) -> tuple[Tabla, Tabla, Tabla, Tabla, Tabla, Tabla]:
    """Construye las tablas de fichas técnicas, explosivos, rocas, brocas y criterios Konya."""
    ft = vb_p.get("ficha_powerroc_t25", {})
    filas_ficha_t25 = [
        ["Equipo de Superficie", ft.get("equipo", "")],
        ["Marca y Modelo", ft.get("marca_modelo", "Epiroc PowerROC T25")],
        ["Aplicación en Obra PA14", ft.get("aplicacion", "")],
        ["Motor Diésel", ft.get("motor", "")],
        ["Potencia Nominal", ft.get("potencia_nominal", "")],
        ["Martillo de Perforación", ft.get("martillo", "")],
        ["Compresor de Barrido", ft.get("compresor", "")],
        ["Rango de Diámetro Recomendado", ft.get("rango_diametro", "")],
        ["Sistema de Aceros / Varillaje", ft.get("sistema_varillaje", "")],
        ["Longitud de Pasada Simple", ft.get("longitud_pasada", "")],
        ["Profundidad Máxima de Perforación", ft.get("profundidad_max", "")],
        ["Broca Base Especificada en Banquetas", ft.get("broca_base", "")],
        ["Velocidad Neta de Penetración", ft.get("velocidad_penetracion", "")],
        ["Vida Útil Estimada de la Broca", ft.get("vida_util_broca", "")],
        ["Consumo Diésel Estimado", ft.get("consumo_diesel", "")],
        ["Archivo PDF Oficial (Drive)", ft.get("archivo_ficha", "")],
        ["Enlace Directo a Ficha Técnica (Google Drive)", ft.get("link_ficha", "")],
    ]
    tabla_ficha_t25 = Tabla(
        ["Característica Técnica", "Especificación Oficial (Epiroc PowerROC T25)"],
        filas_ficha_t25,
        "Ficha Técnica de la Perforadora Hidráulica sobre Orugas Epiroc PowerROC T25",
    )

    filas_exp = [
        [
            e["nombre"],
            e["fabricante"],
            e["tipo"],
            e["densidad_g_cm3"],
            e["vod_m_s"],
            e["resistencia_agua"],
            e["pd_kbar"],
            e["energia_kcal_kg"],
            e["rws_pct"],
        ]
        for e in vol_p.get("catalogo_explosivos", [])
    ]
    tabla_bd_exp = Tabla(
        [
            "Nombre de Explosivo",
            "Fabricante",
            "Tipo / Familia",
            "Densidad (g/cm³)",
            "VOD (m/s)",
            "Resistencia al Agua",
            "Presión Detonación Pd (kbar)",
            "Energía Específica (kcal/kg)",
            "Potencia Relativa RWS (%)",
        ],
        filas_exp,
        "Catálogo Comercial de Explosivos Industriales (EXSA, Enaex, Orica)",
    )

    filas_rocas = [
        [
            r_item["nombre"],
            r_item["densidad_g_cm3"],
            r_item["ucs_mpa"],
            r_item["esponjamiento"],
            r_item["comportamiento"],
        ]
        for r_item in vol_p.get("rocas_geomecanica", [])
    ]
    tabla_rocas = Tabla(
        [
            "Macizo Rocoso",
            "Densidad (g/cm³)",
            "Resistencia Compresiva Uniaxial Rc (MPa)",
            "Factor de Esponjamiento (Fe)",
            "Comportamiento en Voladura",
        ],
        filas_rocas,
        "Base de Datos Geomecánica de Macizos Rocosos (Caso Base: Diorita PA14)",
    )

    filas_brocas = [
        [
            b["diametro_mm"],
            b["diametro_pulg"],
            b["tecnologia"],
            b["tipo_cortador"],
            b["sistema_rosca"],
            b["rango_roca"],
            b["modelos_referencia"],
            b["equipos_compatibles"],
            b["fabricantes"],
            b["compatible_t25"],
        ]
        for b in vol_p.get("brocas_equipos", [])
    ]
    tabla_brocas = Tabla(
        [
            "Diámetro (mm)",
            "Diámetro (pulg)",
            "Tecnología",
            "Tipo de Cortador",
            "Sistema de Rosca / Martillo",
            "Rango de Roca Recomendado",
            "Modelos de Referencia",
            "Equipos Compatibles",
            "Fabricantes",
            "Compatible con Epiroc PowerROC T25",
        ],
        filas_brocas,
        "Catálogo de Brocas de Perforación y Compatibilidad con Epiroc PowerROC T25",
    )

    filas_criterios = [
        [
            "Diámetro Óptimo y Máximo en Banco",
            "D_opt = 8 * H ; D_max = 15 * H",
            "Relación entre altura de banco H (m) y diámetro de broca D (mm) según Konya / UNT.",
        ],
        [
            "Burden Máximo Teórico (Konya 1983/1990)",
            "B_max (pies) = 3.15 * D_e(pulg) * (rho_e / rho_r)^(1/3)",
            "Función del diámetro de carga y la raíz cúbica de la relación de densidades.",
        ],
        [
            "Error de Perforación (e)",
            "e = 0.05 + 0.03 * L",
            "Suma del error de emboquille (0.05 m) y desviación angular (0.03 m/m).",
        ],
        [
            "Burden Práctico Ajustado (B_p)",
            "B_p = (B_max * Kd * Ks * Ke) - e",
            "Distancia efectiva desde el eje del barreno hasta la cara libre del banco.",
        ],
        [
            "Sobreperforación / Pasadura (J)",
            "J = 0.30 * B_max",
            "Perforación bajo la cota de banqueta para evitar lomos o repiés.",
        ],
        [
            "Taco / Retacado Inerte (T)",
            "T = kt * B_p (kt = 0.85)",
            "Confinamiento con detrito angular para evitar cráteres, airblast y flyrock.",
        ],
        [
            "Espaciamiento Práctico (S_p)",
            "S_p = 1.15 * B_p (roca dura)",
            "Distancia entre taladros de una misma fila en banqueo de portal.",
        ],
        [
            "Pozos de Buffer y Precorte de Taludes",
            "B_buf = [W*1000/(FP*KBP*H*rho_r*SBR)]^0.5 ; E_pre = D_in*(Pb+RT)/RT",
            "Control de sobrerrotura (backbreak) en los taludes finales de las banquetas.",
        ],
    ]
    tabla_criterios = Tabla(
        [
            "Parámetro de Diseño",
            "Fórmula (Modelo Matemático de Bancos de C.J. Konya)",
            "Justificación Técnica y Criterio de Control en Banquetas",
        ],
        filas_criterios,
        "1. Formulario Técnico del Modelo Matemático de Bancos de C.J. Konya",
    )
    filas_fuentes = [
        [f["categoria"], f["fuente"], f["justificacion"], f["enlace"]]
        for f in vol_p.get("fuentes_bibliograficas", [])
    ]
    tabla_fuentes = Tabla(
        [
            "Categoría",
            "Documento / Fuente Oficial",
            "Justificación en el Proyecto PA14",
            "Enlace Google Drive",
        ],
        filas_fuentes,
        "2. Fuentes Bibliográficas y Documentación Verificada en Google Drive (Unidad 2)",
    )

    return (
        tabla_ficha_t25,
        tabla_bd_exp,
        tabla_rocas,
        tabla_brocas,
        tabla_criterios,
        tabla_fuentes,
    )
