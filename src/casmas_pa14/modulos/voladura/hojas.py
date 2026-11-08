"""Constructores de hojas Excel para el libro 12_Voladura.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Libro, Tabla, tabla_parametros


def construir_libro_voladura(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 12_Voladura.xlsx exclusivo para la Voladura Subterránea del Túnel."""
    ft = resultados["frente_tunel"]
    inp = resultados["inputs"]
    vol_p = p.get("voladura", {})

    filas_malla = [
        ("Equipo de perforación en frente subterráneo", "Eq_tunel", ft["equipo_tunel"], "-", "06_Maquinaria (Ficha Sandvik DT1131)"),
        ("Número de brazos hidráulicos del Jumbo", "N_brazos", ft["brazos_jumbo"], "brazos", "Jumbo Frontal Computarizado 3 brazos"),
        ("Velocidad de penetración neta por brazo", "Vp_j", ft["vp_m_min"], "m/min", "Martillo hidráulico alta frecuencia en andesita/diorita"),
        ("Ancho de excavación del túnel", "B_tun", ft["ancho_m"], "m", "03_Seccion (Sección Herradura)"),
        ("Altura total de excavación del túnel", "H_tun", ft["altura_m"], "m", "03_Seccion (Sección Herradura)"),
        ("Área de excavación del frente", "A_tun", round(ft["area_m2"], 2), "m²", "03_Seccion (B*hw + pi*B²/8)"),
        ("Perímetro de excavación del frente", "P_tun", round(ft["perimetro_m"], 2), "m", "03_Seccion (B + 2*hw + pi*B/2)"),
        ("Diámetro de taladros vacíos de alivio (Cuele)", "D_aliv", ft["d_alivio_mm"], "mm", 'Broca escariadora de 4" (102 mm)'),
        ("Diámetro de taladros de producción y contorno", "D_prod", ft["de_mm"], "mm", 'Brocas de producción Ø 51 mm (2") y contorno Ø 48 mm (1 7/8")'),
        ("Longitud de barreno ( Barra de 12 pies )", "L_bar", ft["lb_m"], "m", "Barra estándar 12' Jumbo Sandvik DT1131"),
        ("Eficiencia de avance por disparo", "Ef_av", ft["ef_avance"], "-", "Manual EXSA (Cuele quemado cilíndrico = 90%)"),
        ("Avance efectivo por disparo", "Av_disp", "={L_bar}*{Ef_av}", "m/disparo", "Av_disp = L_bar * Ef_av"),
        ("Volumen in-situ roto por disparo", "V_disp", "={A_tun}*{Av_disp}", "m³/disparo", "V_disp = A_tun * Av_disp"),
        ("Espaciamiento periférico de recorte (Smooth Blasting)", "E_per", ft["esp_perif_m"], "m", "Manual EXSA (E = 15 * D_prod = 0.60 m)"),
        ("Coeficiente de roca (Langefors-Kihlström)", "k_roca", ft["k_langefors"], "tal/m²", "Roca intermedia a dura (k = 1.50)"),
        ("Número de taladros cargados (Fórmula Langefors)", "N_lang", "=ROUNDUP({P_tun}/{E_per}+{k_roca}*{A_tun}, 0)", "taladros", "N = ROUNDUP(P / E_per + k * A, 0)"),
        ("Taladros vacíos de alivio en el arranque (Ø 102 mm)", "N_aliv", ft["n_alivio_vacios"], "taladros", f"{ft['n_alivio_vacios']} taladro(s) escariado(s) de Ø 102 mm sin carga explosiva"),
        ("Taladros de Arranque / Cuele quemado (4 secciones)", "N_cuele", ft["n_cuele"], "taladros", "Cuele cilíndrico de 4 cuadrículas concéntricas"),
        ("Taladros de Ayudas de Arranque", "N_ayuda", ft["n_ayudas"], "taladros", "Expansión primaria alrededor del cuele"),
        ("Taladros de Destroza / Producción (Núcleo)", "N_dest", ft["n_destroza"], "taladros", "Rotura principal hacia cavidad ampliada"),
        ("Taladros Cuadradores (Hastiales)", "N_cuad", ft["n_cuadradores"], "taladros", "Perfilado lateral de hastiales"),
        ("Taladros de Alzas / Corona (Recorte de Bóveda)", "N_cor", ft["n_corona"], "taladros", "Voladura amortiguada con Exsacorte / Enaline"),
        ("Taladros de Arrastre / Zapateras (Piso)", "N_arr", ft["n_arrastres"], "taladros", "Corte a nivel de rasante con emulsión resistente al agua"),
        ("Total de taladros cargados en el frente", "N_carg", "={N_cuele}+{N_ayuda}+{N_dest}+{N_cuad}+{N_cor}+{N_arr}", "taladros", "Suma de las 6 zonas cargadas del frente"),
        ("Total de taladros perforados por disparo", "N_perf", "={N_carg}+{N_aliv}", "taladros", "N_perf = N_carg + N_aliv"),
        ("Metros lineales perforados por disparo", "M_perf_t", "={N_perf}*{L_bar}", "m/disparo", "M_perf = N_perf * L_bar"),
        ("Tiempo neto de perforación (Jumbo 3 brazos DT1131)", "T_perf_h", "={M_perf_t}/({Vp_j}*{N_brazos}*60)", "h/disparo", "T_perf = M_perf / (Vp * N_brazos * 60)"),
        ("Factor de carga específico en frente subterráneo", "FC_tun", ft["fc_especifico"], "kg/m³", "Manual EXSA 5ta Ed. (Sección herradura)"),
        ("Consumo total de explosivos por disparo en túnel", "Q_disp_kg", "={V_disp}*{FC_tun}", "kg/disparo", "Q_disp = V_disp * FC_tun (vinculado a 07_Polvorin)"),
    ]

    filas_konya = [
        ("Densidad del explosivo subterráneo", "Sge", inp["sge"], "g/cm³", "Emulsión encartuchada Semexsa / Exagel-E"),
        ("Densidad de la roca en frente", "Sgr", inp["sgr"], "g/cm³", "02_Geologia / Litología ponderada PA14"),
        ("Diámetro de broca en producción (Jumbo DT1131)", "De", inp["de_mm"], "mm", "Broca de botones Ø 45 mm (Jumbo 3 brazos Sandvik DT1131)"),
        ("Profundidad de avance efectivo (corte hacia cara libre)", "H", inp["h"], "m", "Avance efectivo por disparo (3.294 m)"),
        ("Factor corrección N° de secciones", "Kr", inp["kr_lineas"], "-", "Konya Tabla 1 (3 o más filas = 0.90)"),
        ("Factor corrección por depositación", "Kd", inp["kd_depo"], "-", "Konya Tabla 2 (Depositación general = 1.00)"),
        ("Factor corrección por estructura", "Ks", inp["ks_estr"], "-", "Konya Tabla 3 (Capas unidas = 1.10)"),
        ("Burden teórico en destroza sin corregir", "B", "=0.012*((2*({Sge}/{Sgr}))+1.5)*{De}", "m", "B = 0.012 * [(2 * (Sge / Sgr)) + 1.5] * De"),
        ("Burden corregido geomecánico", "Bc", "={B}*{Kr}*{Kd}*{Ks}", "m", "Bc = B * Kr * Kd * Ks (Guía Konya)"),
        ("Espaciamiento en destroza", "S", "=1.4*{B}", "m", "S = 1.4 * B"),
        ("Sobreperforación de confinamiento", "J", "=0.3*{B}", "m", "J = 0.3 * B"),
        ("Taco inerte (detrito/arcilla)", "T", "=0.7*{B}", "m", "T = 0.7 * B"),
        ("Relación de rigidez", "H/B", "={H}/{B}", "-", "H / B (confinamiento de taladro)"),
        ("Longitud total de taladro", "L", "={H}+{J}", "m", "L = H + J"),
        ("Volumen roto por taladro de destroza", "V", "={B}*{S}*{H}", "m³/tal", "V = B * S * H"),
        ("Concentración lineal de carga (Ø 45 mm)", "Qbk", "=0.078539*{Sge}*({De}/10)^2", "kg/m", "Qbk = 0.078539 * Sge * (De/10)²"),
        ("Longitud carga de fondo", "Cf", "=1.3*{B}", "m", "Cf = 1.3 * B"),
        ("Longitud carga de columna", "Cc", "=MAX(0, {L}-({Cf}+{T}))", "m", "Cc = L - (Cf + T)"),
        ("Carga total por taladro de destroza", "Qt", "=({Cf}+{Cc})*{Qbk}", "kg/tal", "Qt = (Cf + Cc) * Qbk"),
        ("Factor de Carga Volumétrico en destroza", "FC", "={Qt}/{V}", "kg/m³", "FC = Qt / V"),
        ("Factor de Potencia Másico en destroza", "FP", "={Qt}/({V}*{Sgr})", "kg/TM", "FP = Qt / (V * Sgr)"),
        ("Constante retardo barrenos", "Th", inp["th_factor"], "ms/m", "López Jimeno / Konya (Tabla Roca)"),
        ("Retardo barreno a barreno", "th", "={Th}*{S}", "ms", "th = Th * S"),
        ("Factor tiempo entre secciones", "TR", inp["tr_factor"], "ms/m", "Konya (Alivio progresivo = 11.5 ms/m)"),
        ("Retardo entre secciones", "tR", "={TR}*{B}", "ms", "tR = TR * B"),
        ("Perforación específica en destroza", "PE", "={L}/{V}", "m/m³", "PE = L / V"),
    ]

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
        ["Característica Técnica", "Especificación Oficial (Jumbo 3 Brazos Sandvik DT1131)"],
        filas_ficha_jumbo,
        "Ficha Técnica del Jumbo Frontal Computarizado de 3 Brazos Sandvik DT1131 / XE3C",
    )

    filas_exp = [
        [e["nombre"], e["fabricante"], e["tipo"], e["densidad_g_cm3"], e["vod_m_s"], e["resistencia_agua"], e["pd_kbar"], e["energia_kcal_kg"], e["rws_pct"]]
        for e in vol_p.get("catalogo_explosivos", [])
    ]
    tabla_bd_exp = Tabla(
        ["Nombre de Explosivo", "Fabricante", "Tipo / Familia", "Densidad (g/cm³)", "VOD (m/s)", "Resistencia al Agua", "Presión Detonación Pd (kbar)", "Energía Específica (kcal/kg)", "Potencia Relativa RWS (%)"],
        filas_exp,
        "Catálogo Comercial de Explosivos Industriales (EXSA, Enaex, Orica)",
    )

    tabla_termo = Tabla(
        ["Parámetro Termodinámico", "Fórmula / Expresión", "Unidad", "Efecto en la Voladura Subterránea (Manual EXSA)"],
        [
            ["Presión de Detonación (Pd)", "Pd = 0.25 * rho_e * VOD² * 10^-6", "GPa (1 GPa = 10 kbar)", "Gobierna el efecto de impacto o brisance en el arranque (cuele quemado)."],
            ["Presión de Explosión (Pe)", "Pe = 0.50 * Pd", "GPa / kbar", "Presión isentrópica de gases en expansión hacia las caras libres del cuele."],
            ["Reducción de Presión (Taladro Seco)", "% Red = 1 - (d_exp / d_taladro)^2.6", "%", "Amortiguamiento de onda de choque en recorte perimetral de bóveda y hastiales."],
            ["Reducción de Presión (Taladro Húmedo)", "% Red = 1 - (d_exp / d_taladro)^1.8", "%", "Transmisión hidrodinámica superior en zapateras/arrastres con agua."],
        ],
        "1. Parámetros Termodinámicos de Detonación y Desacoplamiento",
    )
    tabla_familias = Tabla(
        ["Familia de Explosivo", "Densidad (g/cm³)", "VOD (m/s)", "Resistencia al Agua", "Categoría de Humos", "Aplicación en el Frente Subterráneo PA14"],
        [
            ["Emulsiones Encartuchadas (Emulnor / Slurrex-E)", "1.14 - 1.22", "5,000 - 5,800", "Excelente", "Clase I (Subterráneo)", "Arranque (cuele quemado), ayudas y arrastres/zapateras inundadas."],
            ["Dinamitas Semigelatinas / Gelatinas (Semexsa / Exagel)", "1.12 - 1.38", "4,200 - 5,800", "Buena a Excelente", "Clase I", "Carga de fondo y destroza en roca andesítica/diorítica tenaz."],
            ["Explosivos de Contorno (Exsablock / Exsacorte / Enaline)", "0.81 - 1.21", "3,500 - 4,800", "Buena a Excelente", "Clase I", "Recorte perimetral amortiguado (Smooth Blasting) en bóveda y hastiales."],
            ["Agentes Granulares / ANFO Pesado", "0.80 - 1.25", "3,800 - 4,900", "Nula a Buena", "Clase I (Ventilación forzada)", "Carga de columna en taladros secos de producción con ventilación activa."],
        ],
        "2. Selección de Familias de Explosivos por Zona del Frente",
    )
    filas_ini = [
        [s["producto"], s["tipo"], s["caracteristica"], s["aplicacion"]]
        for s in vol_p.get("sistemas_iniciacion", [])
    ]
    tabla_ini = Tabla(
        ["Accesorio / Sistema de Iniciación", "Composición / Tipo", "Característica Técnica", "Aplicación en el Frente Subterráneo PA14"],
        filas_ini,
        "3. Sistemas y Accesorios de Iniciación Subterránea (EXSA Fanel MS / LP)",
    )

    filas_rocas = [
        [r_item["nombre"], r_item["densidad_g_cm3"], r_item["ucs_mpa"], r_item["esponjamiento"], r_item["comportamiento"]]
        for r_item in vol_p.get("rocas_geomecanica", [])
    ]
    tabla_rocas = Tabla(
        ["Macizo Rocoso", "Densidad (g/cm³)", "Resistencia Compresiva Uniaxial Rc (MPa)", "Factor de Esponjamiento (Fe)", "Comportamiento en Voladura"],
        filas_rocas,
        "Base de Datos Geomecánica de Macizos Rocosos",
    )

    filas_brocas = [
        [b["diametro_mm"], b["diametro_pulg"], b["tecnologia"], b["tipo_cortador"], b["sistema_rosca"], b["rango_roca"], b["modelos_referencia"], b["equipos_compatibles"], b["fabricantes"], b["compatible_t25"]]
        for b in vol_p.get("brocas_equipos", [])
    ]
    tabla_brocas = Tabla(
        ["Diámetro (mm)", "Diámetro (pulg)", "Tecnología", "Tipo de Cortador", "Sistema de Rosca / Martillo", "Rango de Roca Recomendado", "Modelos de Referencia", "Equipos Compatibles", "Fabricantes", "Compatible con PowerROC T25 (Superficie)"],
        filas_brocas,
        "Catálogo de Brocas de Perforación Subterránea (Jumbo DT1131) y Superficie",
    )

    return Libro(
        archivo="12_Voladura.xlsx",
        hojas=[
            Hoja(
                nombre="Malla_y_Avance_Tunel",
                titulo="Perforación y Voladura Subterránea del Frente del Túnel (Jumbo 3 Brazos Sandvik DT1131)",
                tablas=[tabla_parametros(filas_malla, "1. Diseño de Malla de Perforación, Distribución de Taladros y Avance del Frente")],
            ),
            Hoja(
                nombre="Voladura_Konya_Tunel",
                titulo="Modelo Matemático de C.J. Konya Aplicado a Taladros de Destroza del Túnel (Ø 45 mm)",
                tablas=[tabla_parametros(filas_konya, "2. Parámetros y Cálculos de Destroza Subterránea (Formulario C.J. Konya)")],
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
