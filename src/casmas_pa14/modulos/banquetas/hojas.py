"""Constructores de hojas Excel para el libro 15_Voladura_Banquetas.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Libro, Tabla, tabla_parametros


def construir_libro_banquetas(resultados: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 15_Voladura_Banquetas.xlsx exclusivo para Banquetas con PowerROC T25."""
    kt25 = resultados
    vol_p = p.get("voladura", {})
    vb_p = p.get("voladura_banquetas", {})

    filas_t25 = [
        ("Diámetro de broca seleccionada (Epiroc PowerROC T25)", "De_t25", kt25["de_mm"], "mm", 'Broca de botones 2.5" T38/T45 (06_Maquinaria)'),
        ("Diámetro de broca en pulgadas", "De_in", "={De_t25}/25.4", "pulg", "De_in = De_t25 / 25.4"),
        ("Explosivo comercial seleccionado", "Tipo_e", kt25["explosivo_base"], "-", "Catálogo Comercial (Hoja BD_Explosivos)"),
        ("Densidad del explosivo", "rho_e", "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 4, FALSE), 1.18)", "g/cm³", "Búsqueda dinámica en BD_Explosivos"),
        ("Velocidad de detonación (VOD)", "VOD_e", "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 5, FALSE), 4500)", "m/s", "Búsqueda dinámica en BD_Explosivos"),
        ("Presión de detonación del explosivo", "Pd_e", "=IFERROR(VLOOKUP({Tipo_e}, BD_Explosivos!$A$5:$I$31, 7, FALSE), 86)", "kbar", "Búsqueda dinámica en BD_Explosivos"),
        ("Macizo rocoso del portal", "Tipo_r", kt25["roca_base"], "-", "Catálogo Geomecánico (Hoja BD_Rocas)"),
        ("Densidad de la roca", "rho_r", "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 2, FALSE), 2.76)", "g/cm³", "Búsqueda dinámica en BD_Rocas"),
        ("Resistencia compresiva uniaxial (UCS)", "UCS_r", "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 3, FALSE), 250)", "MPa", "Búsqueda dinámica en BD_Rocas"),
        ("Factor de esponjamiento de la roca", "Fe_r", "=IFERROR(VLOOKUP({Tipo_r}, BD_Rocas!$A$5:$E$11, 4, FALSE), 1.50)", "-", "Búsqueda dinámica en BD_Rocas"),
        ("Resistencia a la tracción de la roca", "RT_r", kt25["rt_mpa"], "MPa", "Criterio mecánico en roca dura (Konya)"),
        ("Altura de banco de diseño en banquetas", "H_b", kt25["h_m"], "m", "11_Portales (Banquetas H = 5.0 - 6.0 m)"),
        ("Diámetro óptimo según altura de banco (8*H)", "D_opt", "=8*{H_b}", "mm", "Criterio Konya UNT: D_opt = 8 * H_b"),
        ("Diámetro máximo admisible según banco (15*H)", "D_max", "=15*{H_b}", "mm", "Criterio Konya UNT: D_max = 15 * H_b"),
        ("Factor de corrección por estratificación", "Kd_b", kt25["kd"], "-", "C.J. Konya (1.00 caso base)"),
        ("Factor de corrección geológica", "Ks_b", kt25["ks"], "-", "C.J. Konya (1.00 caso base)"),
        ("Factor de acoplamiento explosivo", "Ke_b", kt25["ke"], "-", "C.J. Konya (1.00 encartuchado atacado)"),
        ("Relación de Taco (T / B)", "kt_b", kt25["kt"], "-", "Konya (0.70 estratificada a 1.00 masiva)"),
        ("Relación de Sobreperforación (J / B_max)", "kj_b", kt25["kj"], "-", "Konya (J = 0.30 * B_max)"),
        ("Relación de Espaciamiento (S / B)", "ks_rel", kt25["ks_rel"], "-", "Konya roca dura (1.15 a 1.40)"),
        ("Error constante de emboquille", "e0", kt25["e0_m"], "m", "Konya: e = 0.05 + 0.03 * L"),
        ("Desviación angular de perforación", "em", kt25["em_m_m"], "m/m", "Konya: 0.03 m por metro perforado"),
        ("Burden máximo teórico (pies)", "B_max_ft", "=3.15*{De_in}*({rho_e}/{rho_r})^(1/3)", "pies", "B_max(ft) = 3.15 * De(in) * (rho_e / rho_r)^(1/3)"),
        ("Burden máximo teórico (m)", "B_max", "={B_max_ft}*0.3048", "m", "B_max(m) = B_max(ft) * 0.3048"),
        ("Sobreperforación (Pasadura)", "J_b", "={kj_b}*{B_max}", "m", "J = kj * B_max"),
        ("Longitud total de perforación", "L_b", "={H_b}+{J_b}", "m", "L = H_b + J_b"),
        ("Error total de perforación", "e_perf", "={e0}+{em}*{L_b}", "m", "e = 0.05 + 0.03 * L_b"),
        ("Burden práctico ajustado", "B_p", "=({B_max}*{Kd_b}*{Ks_b}*{Ke_b})-{e_perf}", "m", "B_p = (B_max * Kd * Ks * Ke) - e"),
        ("Longitud del Taco (Retacado)", "T_b", "={kt_b}*{B_p}", "m", "T_b = kt * B_p"),
        ("Longitud de columna explosiva", "L_c", "=MAX(0, {L_b}-{T_b})", "m", "L_c = L_b - T_b"),
        ("Espaciamiento práctico de diseño", "S_p", "={ks_rel}*{B_p}", "m", "S_p = ks_rel * B_p"),
        ("Espaciamiento secuencial teórico Konya", "S_seq", "=IF({H_b}<4*{B_p}, ({H_b}+7*{B_p})/8, 1.4*{B_p})", "m", "Si H<4B: (H+7B)/8; si H>=4B: 1.4*B"),
        ("Concentración lineal de carga", "q_l", "=(PI()*({De_t25}/1000)^2/4)*{rho_e}*1000", "kg/m", "q_l = (pi/4) * (De/1000)² * rho_e * 1000"),
        ("Carga explosiva por taladro", "Q_tal", "={q_l}*{L_c}", "kg", "Q_tal = q_l * L_c"),
        ("Volumen roto por taladro", "V_tal", "={B_p}*{S_p}*{H_b}", "m³", "V_tal = B_p * S_p * H_b"),
        ("Tonelaje roto por taladro", "W_tal", "={V_tal}*{rho_r}", "t", "W_tal = V_tal * rho_r"),
        ("Factor de potencia volumétrico", "q_v", "={Q_tal}/{V_tal}", "kg/m³", "q_v = Q_tal / V_tal"),
        ("Factor de potencia másico", "q_m", "={Q_tal}/{W_tal}", "kg/t", "q_m = Q_tal / W_tal"),
        ("Factor de potencia en gramos por tonelada", "FP_g", "={q_m}*1000", "g/t", "FP_g = q_m * 1000"),
        ("Índice de rigidez del banco", "IR_b", "={H_b}/{B_p}", "-", "IR = H_b / B_p (>= 2.5 adecuado, >= 4.0 excelente)"),
        ("Carga explosiva en taladro de Buffer (Amortiguado)", "W_buf", kt25["w_buffer_kg"], "kg", "Guía Konya: Carga controlada en fila Buffer"),
        ("Relación Factor de Carga Buffer / Producción", "KBP", kt25["kbp_buffer"], "-", "Guía Konya (KBP = 1.00)"),
        ("Burden de pozos de Buffer", "B_buf", "=SQRT(({W_buf}*1000)/({FP_g}*{KBP}*{H_b}*{rho_r}*({S_p}/{B_p})))", "m", "B_buf = [W*1000 / (FP*KBP*H*rho_r*SBR)]^(1/2)"),
        ("Espaciamiento de pozos de Buffer", "E_buf", "={B_buf}*({S_p}/{B_p})", "m", "E_buf = B_buf * (S_p / B_p)"),
        ("Presión en el barreno de Precorte", "Pb_pre", kt25["pb_precorte_mpa"], "MPa", "Carga desacoplada de contorno (Enaline / Exsacorte)"),
        ("Ángulo de inclinación de Precorte", "Beta_pre", kt25["ang_precorte_deg"], "grados", "Inclinación del talud respecto a la vertical (70° horiz.)"),
        ("Espaciamiento de taladros de Precorte", "E_pre", "=({De_in}*({Pb_pre}+{RT_r})/{RT_r})*0.0254", "m", "E_pre = [De(in) * (Pb + RT) / RT] * 0.0254 (Konya)"),
        ("Longitud de taladros de Precorte", "L_pre", "={H_b}/COS(RADIANS({Beta_pre}))", "m", "L_pre = H_b / cos(Beta)"),
        ("Volumen total real de las 5 banquetas del portal", "Vol_banco", "=Voladura_Por_Banqueta!C11", "m³", "Suma dinámica de las 5 banquetas (Hoja Voladura_Por_Banqueta)"),
        ("Volumen esponjado total para acarreo", "Vol_esp", "={Vol_banco}*{Fe_r}", "m³", "Vol_esp = Vol_banco * Fe_r"),
        ("Número de taladros en el banco de referencia", "N_tal_b", "=ROUNDUP({Vol_banco}/{V_tal}, 0)", "taladros", "N_tal = ROUNDUP(Vol_banco / V_tal, 0)"),
        ("Consumo de explosivo en banco de referencia", "Q_tot_b", "={N_tal_b}*{Q_tal}", "kg", "Q_tot = N_tal * Q_tal"),
        ("Metros de perforación (Epiroc PowerROC T25)", "M_perf_b", "={N_tal_b}*{L_b}", "m", "M_perf = N_tal * L_b"),
    ]

    cols_banq = [
        "ID Banqueta (11_Portales)",
        "Altura Banco H (m)",
        "Volumen In-Situ (m³)",
        "Burden Práctico Bp (m)",
        "Espaciamiento Sp (m)",
        "Pasadura J (m)",
        "Longitud Taladro L (m)",
        "Volumen/Taladro V_tal (m³)",
        "N° Taladros PowerROC T25",
        "Metros Perforados (m)",
        "Horas PowerROC T25 (h)",
        "Carga/Taladro Q (kg)",
        "Consumo Explosivo (kg)",
    ]
    filas_banq = []
    fila_ini = 6
    fila_act = fila_ini
    ql_val = round(kt25["ql_kg_m"], 4)
    rend_val = kt25["rend_perf_m_h"]

    for b in kt25["banquetas_desglose"]:
        filas_banq.append(
            [
                b["id"],
                b["altura_m"],
                b["vol_insitu_m3"],
                b["b_prac_m"],
                b["s_prac_m"],
                b["j_m"],
                f"=B{fila_act}+F{fila_act}",
                f"=D{fila_act}*E{fila_act}*B{fila_act}",
                f"=ROUNDUP(C{fila_act}/H{fila_act}, 0)",
                f"=I{fila_act}*G{fila_act}",
                f"=J{fila_act}/{rend_val}",
                f"=MAX(0, G{fila_act}-(0.85*D{fila_act}))*{ql_val}",
                f"=I{fila_act}*L{fila_act}",
            ]
        )
        fila_act += 1

    if kt25["banquetas_desglose"]:
        fila_fin = fila_act - 1
        filas_banq.append(
            [
                "TOTAL BANQUETAS PORTAL",
                "",
                f"=SUM(C{fila_ini}:C{fila_fin})",
                "",
                "",
                "",
                "",
                "",
                f"=SUM(I{fila_ini}:I{fila_fin})",
                f"=SUM(J{fila_ini}:J{fila_fin})",
                f"=SUM(K{fila_ini}:K{fila_fin})",
                "",
                f"=SUM(M{fila_ini}:M{fila_fin})",
            ]
        )

    tabla_banquetas = Tabla(
        cols_banq,
        filas_banq,
        "Programación de Perforación y Voladura por Tramo de Banqueta (Epiroc PowerROC T25 — Ø 64 mm)",
    )

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
        [e["nombre"], e["fabricante"], e["tipo"], e["densidad_g_cm3"], e["vod_m_s"], e["resistencia_agua"], e["pd_kbar"], e["energia_kcal_kg"], e["rws_pct"]]
        for e in vol_p.get("catalogo_explosivos", [])
    ]
    tabla_bd_exp = Tabla(
        ["Nombre de Explosivo", "Fabricante", "Tipo / Familia", "Densidad (g/cm³)", "VOD (m/s)", "Resistencia al Agua", "Presión Detonación Pd (kbar)", "Energía Específica (kcal/kg)", "Potencia Relativa RWS (%)"],
        filas_exp,
        "Catálogo Comercial de Explosivos Industriales (EXSA, Enaex, Orica)",
    )

    filas_rocas = [
        [r_item["nombre"], r_item["densidad_g_cm3"], r_item["ucs_mpa"], r_item["esponjamiento"], r_item["comportamiento"]]
        for r_item in vol_p.get("rocas_geomecanica", [])
    ]
    tabla_rocas = Tabla(
        ["Macizo Rocoso", "Densidad (g/cm³)", "Resistencia Compresiva Uniaxial Rc (MPa)", "Factor de Esponjamiento (Fe)", "Comportamiento en Voladura"],
        filas_rocas,
        "Base de Datos Geomecánica de Macizos Rocosos (Caso Base: Diorita PA14)",
    )

    filas_brocas = [
        [b["diametro_mm"], b["diametro_pulg"], b["tecnologia"], b["tipo_cortador"], b["sistema_rosca"], b["rango_roca"], b["modelos_referencia"], b["equipos_compatibles"], b["fabricantes"], b["compatible_t25"]]
        for b in vol_p.get("brocas_equipos", [])
    ]
    tabla_brocas = Tabla(
        ["Diámetro (mm)", "Diámetro (pulg)", "Tecnología", "Tipo de Cortador", "Sistema de Rosca / Martillo", "Rango de Roca Recomendado", "Modelos de Referencia", "Equipos Compatibles", "Fabricantes", "Compatible con Epiroc PowerROC T25"],
        filas_brocas,
        "Catálogo de Brocas de Perforación y Compatibilidad con Epiroc PowerROC T25",
    )

    filas_criterios = [
        ["Diámetro Óptimo y Máximo en Banco", "D_opt = 8 * H ; D_max = 15 * H", "Relación entre altura de banco H (m) y diámetro de broca D (mm) según Konya / UNT."],
        ["Burden Máximo Teórico (Konya 1983/1990)", "B_max (pies) = 3.15 * D_e(pulg) * (rho_e / rho_r)^(1/3)", "Función del diámetro de carga y la raíz cúbica de la relación de densidades."],
        ["Error de Perforación (e)", "e = 0.05 + 0.03 * L", "Suma del error de emboquille (0.05 m) y desviación angular (0.03 m/m)."],
        ["Burden Práctico Ajustado (B_p)", "B_p = (B_max * Kd * Ks * Ke) - e", "Distancia efectiva desde el eje del barreno hasta la cara libre del banco."],
        ["Sobreperforación / Pasadura (J)", "J = 0.30 * B_max", "Perforación bajo la cota de banqueta para evitar lomos o repiés."],
        ["Taco / Retacado Inerte (T)", "T = kt * B_p (kt = 0.85)", "Confinamiento con detrito angular para evitar cráteres, airblast y flyrock."],
        ["Espaciamiento Práctico (S_p)", "S_p = 1.15 * B_p (roca dura)", "Distancia entre taladros de una misma fila en banqueo de portal."],
        ["Pozos de Buffer y Precorte de Taludes", "B_buf = [W*1000/(FP*KBP*H*rho_r*SBR)]^0.5 ; E_pre = D_in*(Pb+RT)/RT", "Control de sobrerrotura (backbreak) en los taludes finales de las banquetas."],
    ]
    tabla_criterios = Tabla(
        ["Parámetro de Diseño", "Fórmula (Modelo Matemático de Bancos de C.J. Konya)", "Justificación Técnica y Criterio de Control en Banquetas"],
        filas_criterios,
        "1. Formulario Técnico del Modelo Matemático de Bancos de C.J. Konya",
    )
    filas_fuentes = [
        [f["categoria"], f["fuente"], f["justificacion"], f["enlace"]]
        for f in vol_p.get("fuentes_bibliograficas", [])
    ]
    tabla_fuentes = Tabla(
        ["Categoría", "Documento / Fuente Oficial", "Justificación en el Proyecto PA14", "Enlace Google Drive"],
        filas_fuentes,
        "2. Fuentes Bibliográficas y Documentación Verificada en Google Drive (Unidad 2)",
    )

    return Libro(
        archivo="15_Voladura_Banquetas.xlsx",
        hojas=[
            Hoja(
                nombre="Calculadora_Konya_T25",
                titulo="Calculadora de Perforación y Voladura de Banquetas con Epiroc PowerROC T25 (Broca 64 mm)",
                tablas=[tabla_parametros(filas_t25, "Diseño de Voladura de Banquetas en Superficie, Buffer y Precorte (Modelo C.J. Konya)")],
            ),
            Hoja(
                nombre="Voladura_Por_Banqueta",
                titulo="Desglose de Perforación y Voladura para los 5 Tramos de Banquetas (11_Portales)",
                tablas=[tabla_banquetas],
            ),
            Hoja(
                nombre="Ficha_PowerROC_T25",
                titulo="Especificaciones Técnicas Oficiales — Perforadora sobre Orugas Epiroc PowerROC T25",
                tablas=[tabla_ficha_t25],
            ),
            Hoja(
                nombre="BD_Explosivos",
                titulo="Base de Datos de Explosivos Industriales y Agentes de Voladura",
                tablas=[tabla_bd_exp],
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
            Hoja(
                nombre="Criterios_y_Fuentes",
                titulo="Formulario Matemático de C.J. Konya y Fuentes Documentales (Unidad 2)",
                tablas=[tabla_criterios, tabla_fuentes],
            ),
        ],
    )
