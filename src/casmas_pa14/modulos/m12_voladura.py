"""12 · Voladura Subterránea del Túnel (Jumbo 3 brazos Sandvik DT1131 / XE3C + Catálogo de Explosivos).

Diseña exclusivamente la malla de perforación y voladura subterránea en el frente de ataque
del túnel PA14 (sección herradura 13.30 x 9.58 m, A = 108.43 m²) empleando el Jumbo Frontal
Computarizado de 3 brazos Sandvik DT1131 / XE3C (barra de 12 pies = 3.66 m, broca de producción
Ø 45 mm y escariador de alivio Ø 102 mm), distribuida por zonas del frente (Cuele quemado,
Ayudas, Destroza, Cuadradores, Corona/Recorte y Arrastres) junto con el modelo de C.J. Konya
aplicado al núcleo de destroza y los catálogos de explosivos e iniciación.
Nota: La voladura en superficie para las banquetas del portal con la perforadora sobre orugas
Epiroc PowerROC T25 se calcula por separado en `m15_voladura_banquetas.py` (`15_Voladura_Banquetas.xlsx`).
"""

from typing import Any

from ..modelo import Hoja, Libro, Memoria, Tabla, tabla_parametros

CLAVE = "voladura"


def calcular(p: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
    """Calcula la perforación y voladura subterránea del túnel con Jumbo 3 brazos Sandvik DT1131."""
    vol = p.get("voladura", {})
    perf = p.get("perforacion", {})
    sec = ctx.get("seccion", {})

    ancho_m = float(sec.get("ancho_m", 13.30))
    altura_m = float(sec.get("altura_m", 9.58))
    area_m2 = float(sec.get("area_m2", 108.43))
    perimetro_m = float(sec.get("perimetro_m", 39.99))

    # Parámetros del Jumbo de 3 brazos Sandvik DT1131 y perforación del frente
    equipo_tunel = str(
        vol.get(
            "equipo_perforacion_tunel",
            "Jumbo Frontal Computarizado 3 brazos Sandvik DT1131 / XE3C",
        )
    )
    brazos_jumbo = int(vol.get("brazos_jumbo", 3))
    potencia_jumbo_hp = int(vol.get("potencia_jumbo_hp", 300))
    vp_m_min = float(vol.get("velocidad_penetracion_m_min", 1.50))
    lb_m = float(perf.get("longitud_barreno_m", 3.66))
    ef_avance = float(perf.get("eficiencia_avance", 0.90))
    esp_perif_m = float(perf.get("espaciamiento_periferico_m", 0.60))
    k_langefors = float(perf.get("coeficiente_roca_k", 1.50))
    fc_especifico = float(perf.get("factor_carga_kg_m3", 1.60))

    d_alivio_mm = float(vol.get("diametro_alivio_mm", 102.0))
    de_mm = float(vol.get("diametro_explosivo_mm", 45.0))

    # Distribución de taladros en el frente subterráneo
    n_alivio_vacios = int(vol.get("taladros_alivio_vacios", 4))
    n_cuele = int(vol.get("taladros_cuele_und", 16))
    n_ayudas = int(vol.get("taladros_ayudas_und", 20))
    n_destroza = int(vol.get("taladros_destroza_und", 105))
    n_cuadradores = int(vol.get("taladros_cuadradores_und", 22))
    n_corona = int(vol.get("taladros_corona_und", 42))
    n_arrastres = int(vol.get("taladros_arrastres_und", 26))

    taladros_cargados = (
        n_cuele + n_ayudas + n_destroza + n_cuadradores + n_corona + n_arrastres
    )
    taladros_perforados = taladros_cargados + n_alivio_vacios
    avance_disparo_m = lb_m * ef_avance
    vol_disparo_m3 = area_m2 * avance_disparo_m
    metros_perf_disparo = taladros_perforados * lb_m
    tiempo_perf_neto_h = metros_perf_disparo / (vp_m_min * brazos_jumbo * 60.0)
    kg_explosivo_disparo = vol_disparo_m3 * fc_especifico

    # Modelo de C.J. Konya aplicado a los taladros de destroza del frente subterráneo
    sge = float(vol.get("densidad_explosivo_g_cm3", 1.20))
    sgr = float(vol.get("densidad_roca_g_cm3", 2.60))
    h = float(vol.get("altura_banco_m", avance_disparo_m))
    th_factor = float(vol.get("constante_retardo_ms_m", 4.5))
    tr_factor = float(vol.get("factor_tiempo_filas_ms_m", 11.5))
    kr_lineas = float(vol.get("factor_kr_lineas", 0.90))
    kd_depo = float(vol.get("factor_kd_depositacion", 1.00))
    ks_estr = float(vol.get("factor_ks_estructura", 1.10))

    if "geologia" in ctx and ctx["geologia"].get("tramos"):
        primer_tramo = ctx["geologia"]["tramos"][0]
        if isinstance(primer_tramo, dict) and "densidad_t_m3" in primer_tramo:
            sgr = float(primer_tramo["densidad_t_m3"])

    burden_m = 0.012 * ((2.0 * (sge / sgr)) + 1.5) * de_mm
    burden_corr_m = burden_m * kr_lineas * kd_depo * ks_estr
    espaciamiento_m = 1.4 * burden_m
    sobre_perf_m = 0.3 * burden_m
    taco_m = 0.7 * burden_m
    rigidez = h / burden_m if burden_m > 0 else 0.0
    longitud_taladro_m = h + sobre_perf_m
    vol_romper_m3 = burden_m * espaciamiento_m * h
    de_cm = de_mm / 10.0
    qbk_kg_m = 0.078539 * sge * (de_cm**2)

    carga_fondo_m = 1.3 * burden_m
    carga_columna_m = max(0.0, longitud_taladro_m - (carga_fondo_m + taco_m))
    if carga_columna_m == 0:
        carga_fondo_m = max(0.0, longitud_taladro_m - taco_m)

    carga_total_kg = (carga_fondo_m + carga_columna_m) * qbk_kg_m
    factor_carga_kg_m3 = carga_total_kg / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    toneladas_romper = vol_romper_m3 * sgr
    factor_potencia_kg_tm = (
        carga_total_kg / toneladas_romper if toneladas_romper > 0 else 0.0
    )
    retardo_barrenos_ms = th_factor * espaciamiento_m
    retardo_filas_ms = tr_factor * burden_m
    perf_especifica_m_m3 = (
        longitud_taladro_m / vol_romper_m3 if vol_romper_m3 > 0 else 0.0
    )

    return {
        "frente_tunel": {
            "equipo_tunel": equipo_tunel,
            "brazos_jumbo": brazos_jumbo,
            "potencia_jumbo_hp": potencia_jumbo_hp,
            "vp_m_min": vp_m_min,
            "ancho_m": ancho_m,
            "altura_m": altura_m,
            "area_m2": area_m2,
            "perimetro_m": perimetro_m,
            "lb_m": lb_m,
            "ef_avance": ef_avance,
            "esp_perif_m": esp_perif_m,
            "k_langefors": k_langefors,
            "fc_especifico": fc_especifico,
            "d_alivio_mm": d_alivio_mm,
            "de_mm": de_mm,
            "n_alivio_vacios": n_alivio_vacios,
            "n_cuele": n_cuele,
            "n_ayudas": n_ayudas,
            "n_destroza": n_destroza,
            "n_cuadradores": n_cuadradores,
            "n_corona": n_corona,
            "n_arrastres": n_arrastres,
            "taladros_cargados": taladros_cargados,
            "taladros_perforados": taladros_perforados,
            "avance_disparo_m": avance_disparo_m,
            "vol_disparo_m3": vol_disparo_m3,
            "metros_perf_disparo": metros_perf_disparo,
            "tiempo_perf_neto_h": tiempo_perf_neto_h,
            "kg_explosivo_disparo": kg_explosivo_disparo,
        },
        "inputs": {
            "sge": sge,
            "sgr": sgr,
            "de_mm": de_mm,
            "h": h,
            "th_factor": th_factor,
            "tr_factor": tr_factor,
            "kr_lineas": kr_lineas,
            "kd_depo": kd_depo,
            "ks_estr": ks_estr,
            "burden_m": burden_m,
            "espaciamiento_m": espaciamiento_m,
        },
        "calculados": {
            "burden_m": burden_m,
            "burden_corr_m": burden_corr_m,
            "espaciamiento_m": espaciamiento_m,
            "sobre_perf_m": sobre_perf_m,
            "taco_m": taco_m,
            "rigidez": rigidez,
            "longitud_taladro_m": longitud_taladro_m,
            "vol_romper_m3": vol_romper_m3,
            "qbk_kg_m": qbk_kg_m,
            "carga_fondo_m": carga_fondo_m,
            "carga_columna_m": carga_columna_m,
            "carga_total_kg": carga_total_kg,
            "factor_carga_kg_m3": factor_carga_kg_m3,
            "factor_potencia_kg_tm": factor_potencia_kg_tm,
            "retardo_barrenos_ms": retardo_barrenos_ms,
            "retardo_filas_ms": retardo_filas_ms,
            "perf_especifica_m_m3": perf_especifica_m_m3,
        },
    }


def libro(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 12_Voladura.xlsx exclusivo para la Voladura Subterránea del Túnel."""
    ft = resultados["frente_tunel"]
    inp = resultados["inputs"]
    vol_p = p.get("voladura", {})

    # 1. Hoja Malla_y_Avance_Tunel (Perforación y Voladura Subterránea con Jumbo 3 Brazos Sandvik DT1131)
    filas_malla = [
        (
            "Equipo de perforación en frente subterráneo",
            "Eq_tunel",
            ft["equipo_tunel"],
            "-",
            "06_Maquinaria (Ficha Sandvik DT1131)",
        ),
        (
            "Número de brazos hidráulicos del Jumbo",
            "N_brazos",
            ft["brazos_jumbo"],
            "brazos",
            "Jumbo Frontal Computarizado 3 brazos",
        ),
        (
            "Velocidad de penetración neta por brazo",
            "Vp_j",
            ft["vp_m_min"],
            "m/min",
            "Martillo hidráulico alta frecuencia en andesita/diorita",
        ),
        (
            "Ancho de excavación del túnel",
            "B_tun",
            ft["ancho_m"],
            "m",
            "03_Seccion (Sección Herradura)",
        ),
        (
            "Altura total de excavación del túnel",
            "H_tun",
            ft["altura_m"],
            "m",
            "03_Seccion (Sección Herradura)",
        ),
        (
            "Área de excavación del frente",
            "A_tun",
            round(ft["area_m2"], 2),
            "m²",
            "03_Seccion (B*hw + pi*B²/8)",
        ),
        (
            "Perímetro de excavación del frente",
            "P_tun",
            round(ft["perimetro_m"], 2),
            "m",
            "03_Seccion (B + 2*hw + pi*B/2)",
        ),
        (
            "Diámetro de taladros vacíos de alivio (Cuele)",
            "D_aliv",
            ft["d_alivio_mm"],
            "mm",
            'Broca escariadora de 4" (102 mm)',
        ),
        (
            "Diámetro de taladros de producción y contorno",
            "D_prod",
            ft["de_mm"],
            "mm",
            'Broca de botones de 1 3/4" (45 mm)',
        ),
        (
            "Longitud de barreno ( Barra de 12 pies )",
            "L_bar",
            ft["lb_m"],
            "m",
            "Barra estándar 12' Jumbo Sandvik DT1131",
        ),
        (
            "Eficiencia de avance por disparo",
            "Ef_av",
            ft["ef_avance"],
            "-",
            "Manual EXSA (Cuele quemado cilíndrico = 90%)",
        ),
        (
            "Avance efectivo por disparo",
            "Av_disp",
            "={L_bar}*{Ef_av}",
            "m/disparo",
            "Av_disp = L_bar * Ef_av",
        ),
        (
            "Volumen in-situ roto por disparo",
            "V_disp",
            "={A_tun}*{Av_disp}",
            "m³/disparo",
            "V_disp = A_tun * Av_disp",
        ),
        (
            "Espaciamiento periférico de recorte (Smooth Blasting)",
            "E_per",
            ft["esp_perif_m"],
            "m",
            "Manual EXSA (E = 15 * D_prod = 0.60 m)",
        ),
        (
            "Coeficiente de roca (Langefors-Kihlström)",
            "k_roca",
            ft["k_langefors"],
            "tal/m²",
            "Roca intermedia a dura (k = 1.50)",
        ),
        (
            "Número de taladros cargados (Fórmula Langefors)",
            "N_lang",
            "=ROUNDUP({P_tun}/{E_per}+{k_roca}*{A_tun}, 0)",
            "taladros",
            "N = ROUNDUP(P / E_per + k * A, 0)",
        ),
        (
            "Taladros vacíos de alivio en el arranque (Ø 102 mm)",
            "N_aliv",
            ft["n_alivio_vacios"],
            "taladros",
            "4 taladros escariados sin carga explosiva",
        ),
        (
            "Taladros de Arranque / Cuele quemado (4 secciones)",
            "N_cuele",
            ft["n_cuele"],
            "taladros",
            "Cuele cilíndrico de 4 cuadrículas concéntricas",
        ),
        (
            "Taladros de Ayudas de Arranque",
            "N_ayuda",
            ft["n_ayudas"],
            "taladros",
            "Expansión primaria alrededor del cuele",
        ),
        (
            "Taladros de Destroza / Producción (Núcleo)",
            "N_dest",
            ft["n_destroza"],
            "taladros",
            "Rotura principal hacia cavidad ampliada",
        ),
        (
            "Taladros Cuadradores (Hastiales)",
            "N_cuad",
            ft["n_cuadradores"],
            "taladros",
            "Perfilado lateral de hastiales",
        ),
        (
            "Taladros de Alzas / Corona (Recorte de Bóveda)",
            "N_cor",
            ft["n_corona"],
            "taladros",
            "Voladura amortiguada con Exsacorte / Enaline",
        ),
        (
            "Taladros de Arrastre / Zapateras (Piso)",
            "N_arr",
            ft["n_arrastres"],
            "taladros",
            "Corte a nivel de rasante con emulsión resistente al agua",
        ),
        (
            "Total de taladros cargados en el frente",
            "N_carg",
            "={N_cuele}+{N_ayuda}+{N_dest}+{N_cuad}+{N_cor}+{N_arr}",
            "taladros",
            "Suma de las 6 zonas cargadas del frente",
        ),
        (
            "Total de taladros perforados por disparo",
            "N_perf",
            "={N_carg}+{N_aliv}",
            "taladros",
            "N_perf = N_carg + N_aliv",
        ),
        (
            "Metros lineales perforados por disparo",
            "M_perf_t",
            "={N_perf}*{L_bar}",
            "m/disparo",
            "M_perf = N_perf * L_bar",
        ),
        (
            "Tiempo neto de perforación (Jumbo 3 brazos DT1131)",
            "T_perf_h",
            "={M_perf_t}/({Vp_j}*{N_brazos}*60)",
            "h/disparo",
            "T_perf = M_perf / (Vp * N_brazos * 60)",
        ),
        (
            "Factor de carga específico en frente subterráneo",
            "FC_tun",
            ft["fc_especifico"],
            "kg/m³",
            "Manual EXSA 5ta Ed. (Sección herradura)",
        ),
        (
            "Consumo total de explosivos por disparo en túnel",
            "Q_disp_kg",
            "={V_disp}*{FC_tun}",
            "kg/disparo",
            "Q_disp = V_disp * FC_tun (vinculado a 07_Polvorin)",
        ),
    ]

    # 2. Hoja Voladura_Konya_Tunel (Modelo C.J. Konya aplicado a taladros de destroza del túnel)
    filas_konya = [
        (
            "Densidad del explosivo subterráneo",
            "Sge",
            inp["sge"],
            "g/cm³",
            "Emulsión encartuchada Semexsa / Exagel-E",
        ),
        (
            "Densidad de la roca en frente",
            "Sgr",
            inp["sgr"],
            "g/cm³",
            "02_Geologia / Litología ponderada PA14",
        ),
        (
            "Diámetro de broca en producción (Jumbo DT1131)",
            "De",
            inp["de_mm"],
            "mm",
            "Broca de botones Ø 45 mm (Jumbo 3 brazos Sandvik DT1131)",
        ),
        (
            "Profundidad de avance efectivo (corte hacia cara libre)",
            "H",
            inp["h"],
            "m",
            "Avance efectivo por disparo (3.294 m)",
        ),
        (
            "Factor corrección N° de secciones",
            "Kr",
            inp["kr_lineas"],
            "-",
            "Konya Tabla 1 (3 o más filas = 0.90)",
        ),
        (
            "Factor corrección por depositación",
            "Kd",
            inp["kd_depo"],
            "-",
            "Konya Tabla 2 (Depositación general = 1.00)",
        ),
        (
            "Factor corrección por estructura",
            "Ks",
            inp["ks_estr"],
            "-",
            "Konya Tabla 3 (Capas unidas = 1.10)",
        ),
        (
            "Burden teórico en destroza sin corregir",
            "B",
            "=0.012*((2*({Sge}/{Sgr}))+1.5)*{De}",
            "m",
            "B = 0.012 * [(2 * (Sge / Sgr)) + 1.5] * De",
        ),
        (
            "Burden corregido geomecánico",
            "Bc",
            "={B}*{Kr}*{Kd}*{Ks}",
            "m",
            "Bc = B * Kr * Kd * Ks (Guía Konya)",
        ),
        ("Espaciamiento en destroza", "S", "=1.4*{B}", "m", "S = 1.4 * B"),
        ("Sobreperforación de confinamiento", "J", "=0.3*{B}", "m", "J = 0.3 * B"),
        ("Taco inerte (detrito/arcilla)", "T", "=0.7*{B}", "m", "T = 0.7 * B"),
        (
            "Relación de rigidez",
            "H/B",
            "={H}/{B}",
            "-",
            "H / B (confinamiento de taladro)",
        ),
        ("Longitud total de taladro", "L", "={H}+{J}", "m", "L = H + J"),
        (
            "Volumen roto por taladro de destroza",
            "V",
            "={B}*{S}*{H}",
            "m³/tal",
            "V = B * S * H",
        ),
        (
            "Concentración lineal de carga (Ø 45 mm)",
            "Qbk",
            "=0.078539*{Sge}*({De}/10)^2",
            "kg/m",
            "Qbk = 0.078539 * Sge * (De/10)²",
        ),
        ("Longitud carga de fondo", "Cf", "=1.3*{B}", "m", "Cf = 1.3 * B"),
        (
            "Longitud carga de columna",
            "Cc",
            "=MAX(0, {L}-({Cf}+{T}))",
            "m",
            "Cc = L - (Cf + T)",
        ),
        (
            "Carga total por taladro de destroza",
            "Qt",
            "=({Cf}+{Cc})*{Qbk}",
            "kg/tal",
            "Qt = (Cf + Cc) * Qbk",
        ),
        (
            "Factor de Carga Volumétrico en destroza",
            "FC",
            "={Qt}/{V}",
            "kg/m³",
            "FC = Qt / V",
        ),
        (
            "Factor de Potencia Másico en destroza",
            "FP",
            "={Qt}/({V}*{Sgr})",
            "kg/TM",
            "FP = Qt / (V * Sgr)",
        ),
        (
            "Constante retardo barrenos",
            "Th",
            inp["th_factor"],
            "ms/m",
            "López Jimeno / Konya (Tabla Roca)",
        ),
        ("Retardo barreno a barreno", "th", "={Th}*{S}", "ms", "th = Th * S"),
        (
            "Factor tiempo entre secciones",
            "TR",
            inp["tr_factor"],
            "ms/m",
            "Konya (Alivio progresivo = 11.5 ms/m)",
        ),
        ("Retardo entre secciones", "tR", "={TR}*{B}", "ms", "tR = TR * B"),
        (
            "Perforación específica en destroza",
            "PE",
            "={L}/{V}",
            "m/m³",
            "PE = L / V",
        ),
    ]

    # 3. Hoja Ficha_Jumbo_DT1131
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

    # 4. Hoja BD_Explosivos (27 explosivos comerciales)
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

    # 5. Hoja Catalogo_Detonacion
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

    # 6. Hoja BD_Rocas
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
        "Base de Datos Geomecánica de Macizos Rocosos",
    )

    # 7. Hoja BD_Brocas_Equipos
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
            "Compatible con PowerROC T25 (Superficie)",
        ],
        filas_brocas,
        "Catálogo de Brocas de Perforación Subterránea (Jumbo DT1131) y Superficie",
    )

    return Libro(
        archivo="12_Voladura.xlsx",
        hojas=[
            Hoja(
                nombre="Malla_y_Avance_Tunel",
                titulo="Perforación y Voladura Subterránea del Frente del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
                tablas=[
                    tabla_parametros(
                        filas_malla,
                        "1. Diseño de Malla de Perforación, Distribución de Taladros y Avance del Frente",
                    )
                ],
            ),
            Hoja(
                nombre="Voladura_Konya_Tunel",
                titulo="Modelo Matemático de C.J. Konya Aplicado a Taladros de Destroza del Túnel (Ø 45 mm)",
                tablas=[
                    tabla_parametros(
                        filas_konya,
                        "2. Parámetros y Cálculos de Destroza Subterránea (Formulario C.J. Konya)",
                    )
                ],
            ),
            Hoja(
                nombre="Ficha_Jumbo_DT1131",
                titulo="Especificaciones Técnicas Oficiales — Jumbo Frontal 3 Brazos Sandvik DT1131 / XE3C",
                tablas=[tabla_ficha_jumbo],
            ),
            Hoja(
                nombre="BD_Explosivos",
                titulo="Base de Datos de Explosivos Industriales y Agentes de Voladura",
                tablas=[tabla_bd_exp],
            ),
            Hoja(
                nombre="Catalogo_Detonacion",
                titulo="Parámetros de Detonación, Familias de Explosivos y Sistemas de Iniciación",
                tablas=[tabla_termo, tabla_familias, tabla_ini],
            ),
            Hoja(
                nombre="BD_Rocas",
                titulo="Base de Datos Geomecánica de Macizos Rocosos",
                tablas=[tabla_rocas],
            ),
            Hoja(
                nombre="BD_Brocas_Equipos",
                titulo="Catálogo Técnico de Brocas de Perforación y Equipos Compatibles",
                tablas=[tabla_brocas],
            ),
        ],
    )


def memoria(r: dict[str, Any], p: dict[str, Any]) -> Memoria:
    """Genera la memoria técnica 12_Voladura.md exclusiva para la voladura subterránea del túnel."""
    ft = r["frente_tunel"]
    inp = r["inputs"]
    calc = r["calculados"]

    t_malla = Tabla(
        [
            "Parámetro del Frente Subterráneo",
            "Símbolo",
            "Valor",
            "Unidad",
            "Criterio / Fuente",
        ],
        [
            [
                "Equipo de perforación subterránea",
                "Eq_tunel",
                ft["equipo_tunel"],
                "-",
                "3 brazos automatizados iDATA",
            ],
            [
                "Área de excavación del frente",
                "A_tun",
                f"{ft['area_m2']:.2f}",
                "m²",
                "Sección herradura 13.30 x 9.58 m",
            ],
            [
                "Longitud de barreno (12 pies)",
                "L_bar",
                f"{ft['lb_m']:.2f}",
                "m",
                "Barra estándar Jumbo Sandvik DT1131",
            ],
            [
                "Avance efectivo por disparo (90%)",
                "Av_disp",
                f"{ft['avance_disparo_m']:.2f}",
                "m",
                "L_bar * 0.90",
            ],
            [
                "Volumen in-situ por disparo",
                "V_disp",
                f"{ft['vol_disparo_m3']:.2f}",
                "m³",
                "A_tun * Av_disp",
            ],
            [
                "Taladros vacíos de alivio (Ø 102 mm)",
                "N_aliv",
                ft["n_alivio_vacios"],
                "taladros",
                "Escariados sin carga en el cuele",
            ],
            [
                "Taladros cargados en el frente (Ø 45 mm)",
                "N_carg",
                ft["taladros_cargados"],
                "taladros",
                "Cuele (16) + Ayudas (20) + Destroza (105) + Contorno (64) + Arrastres (26)",
            ],
            [
                "Total de taladros perforados por disparo",
                "N_perf",
                ft["taladros_perforados"],
                "taladros",
                "N_carg + N_aliv",
            ],
            [
                "Tiempo neto de perforación (3 brazos)",
                "T_perf_h",
                f"{ft['tiempo_perf_neto_h']:.2f}",
                "h/disparo",
                "M_perf / (Vp * 3 brazos * 60)",
            ],
            [
                "Consumo de explosivo por disparo",
                "Q_disp_kg",
                f"{ft['kg_explosivo_disparo']:.2f}",
                "kg/disparo",
                "V_disp * 1.60 kg/m³",
            ],
        ],
        "Resumen de Perforación y Voladura Subterránea del Frente del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
    )

    t_resumen_tunel = Tabla(
        ["Parámetro", "Símbolo", "Valor", "Unidad", "Criterio / Fórmula Konya"],
        [
            [
                "Diámetro de taladro de producción",
                "De",
                inp["de_mm"],
                "mm",
                "Jumbo 3 brazos Sandvik DT1131",
            ],
            [
                "Densidad del explosivo",
                "Sge",
                inp["sge"],
                "g/cm³",
                "Emulsión encartuchada / ANFO Pesado",
            ],
            [
                "Densidad de la roca",
                "Sgr",
                inp["sgr"],
                "g/cm³",
                "Litología ponderada PA14",
            ],
            [
                "Burden teórico de Konya en destroza",
                "B",
                f"{calc['burden_m']:.2f}",
                "m",
                "0.012 * (2*Sge/Sgr + 1.5) * De",
            ],
            [
                "Burden corregido (Kr, Kd, Ks)",
                "Bc",
                f"{calc['burden_corr_m']:.2f}",
                "m",
                "B * Kr * Kd * Ks",
            ],
            [
                "Espaciamiento en destroza",
                "S",
                f"{calc['espaciamiento_m']:.2f}",
                "m",
                "1.4 * B",
            ],
            ["Taco inerte", "T", f"{calc['taco_m']:.2f}", "m", "0.7 * B"],
            [
                "Carga total por taladro de destroza",
                "Qt",
                f"{calc['carga_total_kg']:.2f}",
                "kg/tal",
                "(Cf + Cc) * Qbk",
            ],
            [
                "Factor de carga volumétrico en destroza",
                "FC",
                f"{calc['factor_carga_kg_m3']:.2f}",
                "kg/m³",
                "Qt / V",
            ],
            [
                "Retardo barreno a barreno",
                "th",
                f"{calc['retardo_barrenos_ms']:.1f}",
                "ms",
                "Th * S",
            ],
            [
                "Retardo entre secciones",
                "tR",
                f"{calc['retardo_filas_ms']:.1f}",
                "ms",
                "TR * B",
            ],
        ],
        "Parámetros de Destroza Subterránea (Modelo Matemático de C.J. Konya)",
    )

    return Memoria(
        archivo="12_Voladura.md",
        titulo="12 · Memoria de Cálculo: Perforación y Voladura Subterránea del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
        secciones=[
            (
                "1. Alcance y Diferenciación Operativa (Túnel Subterráneo vs. Banquetas en Superficie)",
                [
                    "El presente documento (`12_Voladura.md` y libro `12_Voladura.xlsx`) desarrolla **exclusivamente la "
                    "perforación y voladura subterránea en el frente de ataque del Túnel Casmas Huaraz PA14** "
                    "($B = 13.30\\text{ m}, H = 9.58\\text{ m}, A = 108.43\\text{ m}^2$), donde se trabaja con **una sola "
                    "cara libre inicial** empleando el **Jumbo Frontal Computarizado de 3 brazos Sandvik DT1131 / XE3C** "
                    "($300\\text{ HP}$, barra de $12\\text{ pies} = 3.66\\text{ m}$, broca de producción $\\varnothing 45\\text{ mm}$ "
                    "y escariador de alivio $\\varnothing 102\\text{ mm}$).",
                    "> **Nota de separación técnica:** La perforación y voladura a cielo abierto para los cortes escalonados "
                    "de las **Banquetas y Taludes de Portal en Superficie** (que emplea la perforadora hidráulica sobre "
                    "orugas **Epiroc PowerROC T25** con broca $\\varnothing 64\\text{ mm}$ y el modelo de bancos de C.J. Konya) "
                    "se encuentra independizada en el entregable **`15_Voladura_Banquetas.xlsx`** y su memoria **`15_Voladura_Banquetas.md`**.",
                    t_malla,
                ],
            ),
            (
                "2. Modelo Matemático de C.J. Konya en la Zona de Destroza del Frente",
                [
                    "Una vez aperturada la cavidad inicial por el **cuele quemado cilíndrico de 4 secciones** y sus "
                    "ayudas, los taladros del núcleo de **destroza/producción** trabajan hacia la cara libre interna "
                    "generada, rigiéndose por las relaciones del modelo de C.J. Konya para $\\varnothing 45\\text{ mm}$:",
                    t_resumen_tunel,
                ],
            ),
        ],
    )
