"""Catálogos y tablas de referencia para el libro 12_Voladura.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Tabla


def tablas_bd_explosivos_rocas_brocas(
    vol_p: dict[str, Any],
    *,
    titulo_rocas: str = "Base de Datos Geomecánica de Macizos Rocosos",
    col_t25: str = "Compatible con PowerROC T25 (Superficie)",
    titulo_brocas: str = (
        "Catálogo de Brocas de Perforación Subterránea (Jumbo DT1131) y Superficie"
    ),
) -> tuple[Tabla, Tabla, Tabla]:
    """Construye las tres tablas compartidas de explosivos, rocas y brocas desde voladura."""
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
        titulo_rocas,
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
            col_t25,
        ],
        filas_brocas,
        titulo_brocas,
    )
    return tabla_bd_exp, tabla_rocas, tabla_brocas


def construir_tablas_catalogos_voladura(
    vol_p: dict[str, Any],
) -> tuple[Tabla, Tabla, Tabla, Tabla, Tabla, Tabla, Tabla]:
    """Construye las tablas de fichas técnicas, explosivos, detonación, rocas y brocas."""
    fj = vol_p.get("ficha_jumbo_dt1131", {})
    filas_ficha_jumbo = [
        ["Equipo Subterráneo", fj.get("equipo", "")],
        ["Marca y Modelo", fj.get("marca_modelo", "Sandvik DT1131 / XE3C (iDATA)")],
        ["Aplicación en el Proyecto PA14", fj.get("aplicacion", "")],
        ["Configuración de Brazos", fj.get("numero_brazos", "")],
        ["Área de Cobertura Transversal", fj.get("cobertura_max", "")],
        ["Potencia Nominal Instalada", fj.get("potencia_nominal", "")],
        ["Consumo Energético y Combustible", fj.get("consumo_electrico", "")],
        ["Dimensiones Generales", fj.get("dimensiones", "")],
        ["Peso Operativo", fj.get("peso_operativo", "")],
        ["Viga de Avance y Longitud de Barra", fj.get("viga_avance", "")],
        ["Diámetros de Broca en el Frente", fj.get("brocas_frente", "")],
        ["Velocidad Neta de Penetración", fj.get("velocidad_penetracion", "")],
        ["Dotación Operativa", fj.get("dotacion", "")],
        ["Archivo PDF Oficial (Drive)", fj.get("archivo_ficha", "")],
        ["Enlace Directo a Ficha Técnica (Google Drive)", fj.get("link_ficha", "")],
    ]
    tabla_ficha_jumbo = Tabla(
        [
            "Característica Técnica",
            "Especificación Oficial (Jumbo 3 Brazos Sandvik DT1131)",
        ],
        filas_ficha_jumbo,
        "Ficha Técnica del Jumbo Frontal Computarizado de 3 Brazos Sandvik DT1131 / XE3C",
    )

    tabla_bd_exp, tabla_rocas, tabla_brocas = tablas_bd_explosivos_rocas_brocas(vol_p)

    tabla_termo = Tabla(
        [
            "Parámetro Termodinámico",
            "Fórmula / Expresión",
            "Unidad",
            "Efecto en la Voladura Subterránea (Manual EXSA)",
        ],
        [
            [
                "Presión de Detonación (Pd)",
                "Pd = 0.25 * rho_e * VOD² * 10^-6",
                "GPa (1 GPa = 10 kbar)",
                "Gobierna el efecto de impacto o brisance en el arranque (cuele quemado).",
            ],
            [
                "Presión de Explosión (Pe)",
                "Pe = 0.50 * Pd",
                "GPa / kbar",
                "Presión isentrópica de gases en expansión hacia las caras libres del cuele.",
            ],
            [
                "Reducción de Presión (Taladro Seco)",
                "% Red = 1 - (d_exp / d_taladro)^2.6",
                "%",
                "Amortiguamiento de onda de choque en recorte perimetral de bóveda y hastiales.",
            ],
            [
                "Reducción de Presión (Taladro Húmedo)",
                "% Red = 1 - (d_exp / d_taladro)^1.8",
                "%",
                "Transmisión hidrodinámica superior en zapateras/arrastres con agua.",
            ],
        ],
        "1. Parámetros Termodinámicos de Detonación y Desacoplamiento",
    )
    tabla_familias = Tabla(
        [
            "Familia de Explosivo",
            "Densidad (g/cm³)",
            "VOD (m/s)",
            "Resistencia al Agua",
            "Categoría de Humos",
            "Aplicación en el Frente Subterráneo PA14",
        ],
        [
            [
                "Emulsiones Encartuchadas (Emulnor / Slurrex-E)",
                "1.14 - 1.22",
                "5,000 - 5,800",
                "Excelente",
                "Clase I (Subterráneo)",
                "Arranque (cuele quemado), ayudas y arrastres/zapateras inundadas.",
            ],
            [
                "Dinamitas Semigelatinas / Gelatinas (Semexsa / Exagel)",
                "1.12 - 1.38",
                "4,200 - 5,800",
                "Buena a Excelente",
                "Clase I",
                "Carga de fondo y destroza en roca andesítica/diorítica tenaz.",
            ],
            [
                "Explosivos de Contorno (Exsablock / Exsacorte / Enaline)",
                "0.81 - 1.21",
                "3,500 - 4,800",
                "Buena a Excelente",
                "Clase I",
                "Recorte perimetral amortiguado (Smooth Blasting) en bóveda y hastiales.",
            ],
            [
                "Agentes Granulares / ANFO Pesado",
                "0.80 - 1.25",
                "3,800 - 4,900",
                "Nula a Buena",
                "Clase I (Ventilación forzada)",
                "Carga de columna en taladros secos de producción con ventilación activa.",
            ],
        ],
        "2. Selección de Familias de Explosivos por Zona del Frente",
    )
    filas_ini = [
        [s["producto"], s["tipo"], s["caracteristica"], s["aplicacion"]]
        for s in vol_p.get("sistemas_iniciacion", [])
    ]
    tabla_ini = Tabla(
        [
            "Accesorio / Sistema de Iniciación",
            "Composición / Tipo",
            "Característica Técnica",
            "Aplicación en el Frente Subterráneo PA14",
        ],
        filas_ini,
        "3. Sistemas y Accesorios de Iniciación Subterránea (EXSA Fanel MS / LP)",
    )

    return (
        tabla_ficha_jumbo,
        tabla_bd_exp,
        tabla_termo,
        tabla_familias,
        tabla_ini,
        tabla_rocas,
        tabla_brocas,
    )
