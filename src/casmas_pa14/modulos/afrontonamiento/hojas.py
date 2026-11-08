"""Constructores de hojas Excel para el libro 14_Afrontonamiento.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Libro, Tabla, tabla_parametros
from .tablas_sostenimiento import construir_filas_sostenimiento_fronton


def construir_libro_afrontonamiento(r: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 14_Afrontonamiento.xlsx con las 6 hojas dinámicas del sellado del portal."""
    af_p = p.get("afrontonamiento", {})

    filas_rmr = [
        (
            "1. Resistencia de la roca intacta (UCS = 50 - 100 MPa)",
            "P_ucs",
            r["pts_ucs"],
            "pts",
            "Bieniawski (1989) - Roca moderadamente dura",
        ),
        (
            "2. Índice de calidad de la roca (RQD = 50% - 75%)",
            "P_rqd",
            r["pts_rqd"],
            "pts",
            "Bieniawski (1989) - Calidad media en portal",
        ),
        (
            "3. Espaciamiento de discontinuidades (0.20 - 0.60 m)",
            "P_esp",
            r["pts_esp"],
            "pts",
            "Bieniawski (1989) - Fracturación moderada",
        ),
        (
            "4. Condición de las discontinuidades (Ligeramente rugosas, sep. < 1 mm)",
            "P_cond",
            r["pts_cond"],
            "pts",
            "Bieniawski (1989)",
        ),
        (
            "5. Agua subterránea (Húmedo / goteo ligero)",
            "P_agua",
            r["pts_agua"],
            "pts",
            "Bieniawski (1989) - Caudal < 10 L/min",
        ),
        (
            "RMR Básico (Suma de los 5 parámetros)",
            "RMR_b",
            "={P_ucs}+{P_rqd}+{P_esp}+{P_cond}+{P_agua}",
            "pts",
            "RMR_b = P_ucs + P_rqd + P_esp + P_cond + P_agua",
        ),
        (
            "6. Ajuste por orientación de discontinuidades (Regular)",
            "Aj_ori",
            r["aj_ori"],
            "pts",
            "Bieniawski (1989) para talud/portal",
        ),
        (
            "RMR Corregido de Diseño en el Frontón",
            "RMR_corr",
            "={RMR_b}+{Aj_ori}",
            "pts",
            "RMR_corr = RMR_b + Aj_ori (Clase III Regular)",
        ),
    ]
    tabla_clases_rmr = Tabla(
        [
            "Rango RMR",
            "Clase",
            "Calidad del Macizo Rocoso",
            "Cohesión (kPa)",
            "Ángulo de Fricción (°)",
            "Tiempo de Autosoporte Referencial",
        ],
        [
            [
                "81 - 100",
                "I",
                "Muy Buena",
                "> 400",
                "> 45°",
                "20 años para claro de 15 m",
            ],
            [
                "61 - 80",
                "II",
                "Buena",
                "300 - 400",
                "35° - 45°",
                "1 año para claro de 10 m",
            ],
            [
                "41 - 60",
                "III",
                "Regular (CASO PORTAL PA14 = 42)",
                "200 - 300",
                "25° - 35°",
                "1 semana para claro de 5 m",
            ],
            [
                "21 - 40",
                "IV",
                "Mala",
                "100 - 200",
                "15° - 25°",
                "10 horas para claro de 2.5 m",
            ],
            ["< 21", "V", "Muy Mala", "< 100", "< 15°", "30 minutos para claro de 1 m"],
        ],
        "Tabla de Clasificación Geomecánica RMR de Bieniawski (1989)",
    )

    filas_terzaghi = [
        (
            "Ancho de excavación del túnel",
            "B_exc",
            r["ancho_b"],
            "m",
            "03_Seccion (Ancho herradura B = 13.30 m)",
        ),
        (
            "Altura de excavación del túnel",
            "Ht_exc",
            r["alto_h"],
            "m",
            "03_Seccion (Altura herradura Ht = 9.58 m)",
        ),
        (
            "Condición de roca según Terzaghi (1946)",
            "Cond_T",
            4,
            "-",
            "Condición 4: Medianamente fracturada en bloques algo abiertos",
        ),
        (
            "Factor de carga de roca de Terzaghi",
            "k_terz",
            r["k_terz"],
            "-",
            "Terzaghi (1946): Hp = 0.25*B a 0.35*(B + Ht)",
        ),
        (
            "Peso específico del macizo rocoso",
            "gamma_r",
            r["gamma_kn_m3"],
            "kN/m³",
            "Geomecánica del portal (2.65 t/m³)",
        ),
        (
            "Ancho de influencia de carga (B + Ht)",
            "C_terz",
            "={B_exc}+{Ht_exc}",
            "m",
            "C = B_exc + Ht_exc",
        ),
        (
            "Altura de carga de roca aflojada (Hp)",
            "Hp_terz",
            "={k_terz}*{C_terz}",
            "m",
            "Hp = k_terz * (B_exc + Ht_exc)",
        ),
        (
            "Altura total de diseño del frontón (Ht + Hp)",
            "H_front",
            "={Ht_exc}+{Hp_terz}",
            "m",
            "H_front = Ht_exc + Hp_terz",
        ),
        (
            "Presión vertical de soporte requerida (kPa)",
            "Pv_kpa",
            "={gamma_r}*{Hp_terz}",
            "kPa",
            "Pv = gamma_r * Hp_terz",
        ),
        (
            "Presión vertical de soporte requerida (MPa)",
            "Pv_mpa",
            "={Pv_kpa}/1000",
            "MPa",
            "Pv(MPa) = Pv(kPa) / 1000",
        ),
    ]
    filas_clases_terz = [
        [c["id"], c["condicion"], c["formula_hp"], c["factor_k"], c["observacion"]]
        for c in af_p.get("terzaghi_clases", [])
    ]
    tabla_clases_terz = Tabla(
        [
            "N°",
            "Condición del Macizo Rocoso (Terzaghi 1946)",
            "Carga de Roca (Altura Hp)",
            "Factor k Adoptado",
            "Observaciones Técnicas",
        ],
        filas_clases_terz,
        "Clasificación de Cargas de Roca de Karl Terzaghi (1946)",
    )

    filas_afrontonamiento = [
        (
            "Longitud total del equipo con cuchara en suelo (CAT 966H)",
            "L_eq",
            r["l_eq"],
            "m",
            f"Ficha Técnica CAT 966H ({r['link_ficha_cat966h']})",
        ),
        (
            "Ancho sobre neumáticos (CAT 966H)",
            "W_eq",
            r["w_eq"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Altura hasta el techo de la cabina (CAT 966H)",
            "H_cab",
            r["h_cab"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Radio de giro exterior de neumáticos (CAT 966H)",
            "R_giro",
            r["r_giro"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Altura de descarga máxima a 45° (CAT 966H)",
            "H_desc",
            r["h_desc"],
            "m",
            "Ficha Técnica Caterpillar 966H",
        ),
        (
            "Distancia de seguridad operacional lateral",
            "D_seg",
            r["d_seg"],
            "m",
            "D.S. 024-2016-EM (Resguardo de maniobra)",
        ),
        (
            "Ancho de la sección del túnel (B)",
            "B_tun",
            "=Teoria_Cargas_Terzaghi!C6",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Altura de la sección del túnel (Ht)",
            "H_tun",
            "=Teoria_Cargas_Terzaghi!C7",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Altura recta de hastiales",
            "H_hast",
            "={H_tun}-({B_tun}/2)",
            "m",
            "H_hast = H_tun - B_tun / 2",
        ),
        (
            "Área rectangular inferior del túnel",
            "A_rect",
            "={B_tun}*{H_hast}",
            "m²",
            "A_rect = B_tun * H_hast",
        ),
        (
            "Área semicircular de la bóveda",
            "A_bov",
            "=(PI()*({B_tun}/2)^2)/2",
            "m²",
            "A_bov = pi * (B_tun/2)² / 2",
        ),
        (
            "Área total de la sección del túnel a descontar",
            "A_tun",
            "={A_rect}+{A_bov}",
            "m²",
            "A_tun = A_rect + A_bov (03_Seccion)",
        ),
        (
            "Semiancho de maniobra en explanada de portal",
            "W_semi",
            "={R_giro}+{L_eq}+{D_seg}",
            "m",
            "W_semi = R_giro + L_eq + D_seg",
        ),
        (
            "Ancho total del frontón (2 * Semiancho)",
            "W_front",
            "=2*{W_semi}",
            "m",
            "W_front = 2 * W_semi",
        ),
        (
            "Altura total del frontón (Ht + Hp)",
            "H_front_p",
            "=Teoria_Cargas_Terzaghi!C13",
            "m",
            "Vínculo dinámico a Teoria_Cargas_Terzaghi",
        ),
        (
            "Área bruta total del frontón",
            "A_bruta",
            "={W_front}*{H_front_p}",
            "m²",
            "A_bruta = W_front * H_front",
        ),
        (
            "TOTAL ÁREA NETA A SELLAR / AFRONTONAR",
            "A_neta",
            "={A_bruta}-{A_tun}",
            "m²",
            "A_neta = A_bruta - A_tun",
        ),
    ]

    filas_malla, filas_pernos, filas_shotcrete = construir_filas_sostenimiento_fronton(
        r
    )

    return Libro(
        "14_Afrontonamiento.xlsx",
        [
            Hoja(
                "RMR_Geomecanica",
                "Valoración Geomecánica RMR de Bieniawski (1989) en el Portal y Frontón",
                [
                    tabla_parametros(
                        filas_rmr, "Valoración RMR del Macizo Rocoso en el Frontón"
                    ),
                    tabla_clases_rmr,
                ],
            ),
            Hoja(
                "Teoria_Cargas_Terzaghi",
                "Teoría de Cargas de Roca de Karl Terzaghi (1946) Aplicada al Frontón del Portal",
                [
                    tabla_parametros(
                        filas_terzaghi,
                        "Cálculo de Altura de Carga (Hp) y Presión Vertical",
                    ),
                    tabla_clases_terz,
                ],
            ),
            Hoja(
                "Afrontonamiento_Portal",
                "Geometría del Afrontonamiento y Sellado del Portal (Maniobra CAT 966H) — Área Neta",
                [
                    tabla_parametros(
                        filas_afrontonamiento,
                        "Dimensionamiento del Frontón y Descuento de Sección del Túnel",
                    )
                ],
            ),
            Hoja(
                "Malla_Electrosoldada",
                "Cálculo de Malla Electrosoldada Q-188 en el Frontón del Portal",
                [
                    tabla_parametros(
                        filas_malla,
                        "Metrado de Paños con Traslape y Tiempo de Instalación",
                    )
                ],
            ),
            Hoja(
                "Pernos_RockBolt",
                "Cálculo de Pernos Helicoidales RockBolt, Cartuchos de Resina y Ciclo del Bolter",
                [
                    tabla_parametros(
                        filas_pernos,
                        "Dimensionamiento de Empernado Sistemático y Consumo de Resina",
                    )
                ],
            ),
            Hoja(
                "Shotcrete_Robotizado",
                "Dosificación y Rendimiento de Shotcrete Vía Húmeda con Fibra Sintética (Sellado del Portal)",
                [
                    tabla_parametros(
                        filas_shotcrete,
                        "Volúmenes, Insumos Sika y Tiempos de Lanzado Robotizado",
                    )
                ],
            ),
        ],
    )
