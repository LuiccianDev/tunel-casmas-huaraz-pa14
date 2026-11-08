"""Constructores de hojas Excel para el libro 14_Afrontonamiento.xlsx."""

from __future__ import annotations

from typing import Any

from ...modelo import Hoja, Libro, Tabla, tabla_parametros


def construir_libro_afrontonamiento(r: dict[str, Any], p: dict[str, Any]) -> Libro:
    """Genera el libro 14_Afrontonamiento.xlsx con las 6 hojas dinámicas del sellado del portal."""
    af_p = p.get("afrontonamiento", {})

    filas_rmr = [
        ("1. Resistencia de la roca intacta (UCS = 50 - 100 MPa)", "P_ucs", r["pts_ucs"], "pts", "Bieniawski (1989) - Roca moderadamente dura"),
        ("2. Índice de calidad de la roca (RQD = 50% - 75%)", "P_rqd", r["pts_rqd"], "pts", "Bieniawski (1989) - Calidad media en portal"),
        ("3. Espaciamiento de discontinuidades (0.20 - 0.60 m)", "P_esp", r["pts_esp"], "pts", "Bieniawski (1989) - Fracturación moderada"),
        ("4. Condición de las discontinuidades (Ligeramente rugosas, sep. < 1 mm)", "P_cond", r["pts_cond"], "pts", "Bieniawski (1989)"),
        ("5. Agua subterránea (Húmedo / goteo ligero)", "P_agua", r["pts_agua"], "pts", "Bieniawski (1989) - Caudal < 10 L/min"),
        ("RMR Básico (Suma de los 5 parámetros)", "RMR_b", "={P_ucs}+{P_rqd}+{P_esp}+{P_cond}+{P_agua}", "pts", "RMR_b = P_ucs + P_rqd + P_esp + P_cond + P_agua"),
        ("6. Ajuste por orientación de discontinuidades (Regular)", "Aj_ori", r["aj_ori"], "pts", "Bieniawski (1989) para talud/portal"),
        ("RMR Corregido de Diseño en el Frontón", "RMR_corr", "={RMR_b}+{Aj_ori}", "pts", "RMR_corr = RMR_b + Aj_ori (Clase III Regular)"),
    ]
    tabla_clases_rmr = Tabla(
        ["Rango RMR", "Clase", "Calidad del Macizo Rocoso", "Cohesión (kPa)", "Ángulo de Fricción (°)", "Tiempo de Autosoporte Referencial"],
        [
            ["81 - 100", "I", "Muy Buena", "> 400", "> 45°", "20 años para claro de 15 m"],
            ["61 - 80", "II", "Buena", "300 - 400", "35° - 45°", "1 año para claro de 10 m"],
            ["41 - 60", "III", "Regular (CASO PORTAL PA14 = 42)", "200 - 300", "25° - 35°", "1 semana para claro de 5 m"],
            ["21 - 40", "IV", "Mala", "100 - 200", "15° - 25°", "10 horas para claro de 2.5 m"],
            ["< 21", "V", "Muy Mala", "< 100", "< 15°", "30 minutos para claro de 1 m"],
        ],
        "Tabla de Clasificación Geomecánica RMR de Bieniawski (1989)",
    )

    filas_terzaghi = [
        ("Ancho de excavación del túnel", "B_exc", r["ancho_b"], "m", "03_Seccion (Ancho herradura B = 13.30 m)"),
        ("Altura de excavación del túnel", "Ht_exc", r["alto_h"], "m", "03_Seccion (Altura herradura Ht = 9.58 m)"),
        ("Condición de roca según Terzaghi (1946)", "Cond_T", 4, "-", "Condición 4: Medianamente fracturada en bloques algo abiertos"),
        ("Factor de carga de roca de Terzaghi", "k_terz", r["k_terz"], "-", "Terzaghi (1946): Hp = 0.25*B a 0.35*(B + Ht)"),
        ("Peso específico del macizo rocoso", "gamma_r", r["gamma_kn_m3"], "kN/m³", "Geomecánica del portal (2.65 t/m³)"),
        ("Ancho de influencia de carga (B + Ht)", "C_terz", "={B_exc}+{Ht_exc}", "m", "C = B_exc + Ht_exc"),
        ("Altura de carga de roca aflojada (Hp)", "Hp_terz", "={k_terz}*{C_terz}", "m", "Hp = k_terz * (B_exc + Ht_exc)"),
        ("Altura total de diseño del frontón (Ht + Hp)", "H_front", "={Ht_exc}+{Hp_terz}", "m", "H_front = Ht_exc + Hp_terz"),
        ("Presión vertical de soporte requerida (kPa)", "Pv_kpa", "={gamma_r}*{Hp_terz}", "kPa", "Pv = gamma_r * Hp_terz"),
        ("Presión vertical de soporte requerida (MPa)", "Pv_mpa", "={Pv_kpa}/1000", "MPa", "Pv(MPa) = Pv(kPa) / 1000"),
    ]
    filas_clases_terz = [
        [c["id"], c["condicion"], c["formula_hp"], c["factor_k"], c["observacion"]]
        for c in af_p.get("terzaghi_clases", [])
    ]
    tabla_clases_terz = Tabla(
        ["N°", "Condición del Macizo Rocoso (Terzaghi 1946)", "Carga de Roca (Altura Hp)", "Factor k Adoptado", "Observaciones Técnicas"],
        filas_clases_terz,
        "Clasificación de Cargas de Roca de Karl Terzaghi (1946)",
    )

    filas_afrontonamiento = [
        ("Longitud total del equipo con cuchara en suelo (CAT 966H)", "L_eq", r["l_eq"], "m", f"Ficha Técnica CAT 966H ({r['link_ficha_cat966h']})"),
        ("Ancho sobre neumáticos (CAT 966H)", "W_eq", r["w_eq"], "m", "Ficha Técnica Caterpillar 966H"),
        ("Altura hasta el techo de la cabina (CAT 966H)", "H_cab", r["h_cab"], "m", "Ficha Técnica Caterpillar 966H"),
        ("Radio de giro exterior de neumáticos (CAT 966H)", "R_giro", r["r_giro"], "m", "Ficha Técnica Caterpillar 966H"),
        ("Altura de descarga máxima a 45° (CAT 966H)", "H_desc", r["h_desc"], "m", "Ficha Técnica Caterpillar 966H"),
        ("Distancia de seguridad operacional lateral", "D_seg", r["d_seg"], "m", "D.S. 024-2016-EM (Resguardo de maniobra)"),
        ("Ancho de la sección del túnel (B)", "B_tun", "=Teoria_Cargas_Terzaghi!C6", "m", "Vínculo dinámico a Teoria_Cargas_Terzaghi"),
        ("Altura de la sección del túnel (Ht)", "H_tun", "=Teoria_Cargas_Terzaghi!C7", "m", "Vínculo dinámico a Teoria_Cargas_Terzaghi"),
        ("Altura recta de hastiales", "H_hast", "={H_tun}-({B_tun}/2)", "m", "H_hast = H_tun - B_tun / 2"),
        ("Área rectangular inferior del túnel", "A_rect", "={B_tun}*{H_hast}", "m²", "A_rect = B_tun * H_hast"),
        ("Área semicircular de la bóveda", "A_bov", "=(PI()*({B_tun}/2)^2)/2", "m²", "A_bov = pi * (B_tun/2)² / 2"),
        ("Área total de la sección del túnel a descontar", "A_tun", "={A_rect}+{A_bov}", "m²", "A_tun = A_rect + A_bov (03_Seccion)"),
        ("Semiancho de maniobra en explanada de portal", "W_semi", "={R_giro}+{L_eq}+{D_seg}", "m", "W_semi = R_giro + L_eq + D_seg"),
        ("Ancho total del frontón (2 * Semiancho)", "W_front", "=2*{W_semi}", "m", "W_front = 2 * W_semi"),
        ("Altura total del frontón (Ht + Hp)", "H_front_p", "=Teoria_Cargas_Terzaghi!C13", "m", "Vínculo dinámico a Teoria_Cargas_Terzaghi"),
        ("Área bruta total del frontón", "A_bruta", "={W_front}*{H_front_p}", "m²", "A_bruta = W_front * H_front"),
        ("TOTAL ÁREA NETA A SELLAR / AFRONTONAR", "A_neta", "={A_bruta}-{A_tun}", "m²", "A_neta = A_bruta - A_tun"),
    ]

    filas_malla = [
        ("Área neta del frontón a sellar", "A_neta_m", "=Afrontonamiento_Portal!C22", "m²", "Vínculo dinámico a Afrontonamiento_Portal"),
        ("Largo comercial del paño de malla electrosoldada", "L_pano", r["l_pano"], "m", "Paño estándar Q-188 (6.00 x 2.40 m)"),
        ("Ancho comercial del paño de malla electrosoldada", "W_pano", r["w_pano"], "m", "Paño estándar Q-188 (6.00 x 2.40 m)"),
        ("Traslape mínimo en ambos sentidos (3 cocadas)", "Traslape", r["traslape"], "m", "MTC EG-2013 / D.S. 024-2016-EM (0.30 m)"),
        ("Largo efectivo útil del paño (con traslape)", "L_util", "={L_pano}-{Traslape}", "m", "L_util = L_pano - Traslape"),
        ("Ancho efectivo útil del paño (con traslape)", "W_util", "={W_pano}-{Traslape}", "m", "W_util = W_pano - Traslape"),
        ("Área neta efectiva cubierta por paño", "A_util_p", "={L_util}*{W_util}", "m²/paño", "A_util = L_util * W_util"),
        ("Cantidad exacta de paños requeridos", "N_panos_ex", "={A_neta_m}/{A_util_p}", "paños", "N_exacto = A_neta / A_util"),
        ("Cantidad de paños a instalar (Redondeo superior)", "N_panos", "=ROUNDUP({N_panos_ex}, 0)", "und", "ROUNDUP(N_exacto, 0)"),
        ("Tiempo unitario de instalación por paño", "t_pano", r["t_inst_pano_min"], "min/paño", "Cuadrilla de emboquille con telehandler"),
        ("Tiempo total de instalación de malla (minutos)", "T_malla_min", "={N_panos}*{t_pano}", "min", "T_min = N_panos * t_pano"),
        ("TOTAL TIEMPO DE INSTALACIÓN DE MALLA (HORAS)", "T_malla_h", "={T_malla_min}/60", "h", "T_h = T_min / 60"),
    ]

    filas_pernos = [
        ("Área neta del frontón a sellar", "A_neta_p", "=Afrontonamiento_Portal!C22", "m²", "Vínculo dinámico a Afrontonamiento_Portal"),
        ("Longitud del perno RockBolt helicoidal", "L_perno", r["l_perno_f"], "m", "Barra helicoidal ASTM A615 G60 (3.00 m)"),
        ("Diámetro de la barra del perno", "d_perno", r["d_perno_mm"], "mm", 'Barra de 22 mm (7/8")'),
        ("Diámetro de perforación del taladro", "d_tal", r["d_tal_mm"], "mm", 'Broca de 32 mm (1 1/4")'),
        ("Espaciamiento sistemático entre pernos (e x e)", "e_perno", r["esp_perno_f"], "m", "Cuadrícula de 1.50 x 1.50 m en Clase III"),
        ("Área de influencia tributaria por perno", "A_trib", "={e_perno}^2", "m²/perno", "A_trib = e_perno²"),
        ("Cantidad de pernos requeridos en el frontón", "N_pernos", "=ROUNDUP({A_neta_p}/{A_trib}, 0)", "und", "ROUNDUP(A_neta / A_trib, 0)"),
        ("Diámetro del cartucho de resina epóxica/poliéster", "d_cart", r["d_cart_mm"], "mm", "Ficha técnica cartucho de resina (28 mm)"),
        ("Longitud del cartucho de resina", "L_cart", r["l_cart_mm"], "mm", "Cartucho estándar de 305 mm (1 pie)"),
        ("Peso unitario del cartucho de resina", "w_cart", r["peso_cart_g"], "g", "320 g por cartucho"),
        ("Cantidad de cartuchos por caja comercial", "u_caja", r["cart_x_caja"], "und/caja", "Caja comercial de 50 unidades"),
        ("Volumen total del taladro perforado", "V_tal_p", "=PI()*({d_tal}/2000)^2*{L_perno}", "m³", "V_tal = pi * (d_tal/2)² * L_perno"),
        ("Volumen ocupado por la barra de acero", "V_bar", "=PI()*({d_perno}/2000)^2*{L_perno}", "m³", "V_bar = pi * (d_perno/2)² * L_perno"),
        ("Volumen anular libre requerido de resina", "V_anul", "={V_tal_p}-{V_bar}", "m³", "V_anul = V_tal - V_bar"),
        ("Volumen unitario de 1 cartucho de resina", "V_cart", "=PI()*({d_cart}/2000)^2*({L_cart}/1000)", "m³", "V_cart = pi * (d_cart/2)² * L_cart"),
        ("Cartuchos de resina por taladro (Redondeado)", "N_cart_tal", "=ROUNDUP({V_anul}/{V_cart}, 0)", "und", "ROUNDUP(V_anul / V_cart, 0)"),
        ("Total de cartuchos de resina para el frontón", "N_cart_tot", "={N_pernos}*{N_cart_tal}", "und", "N_pernos * N_cart_tal"),
        ("Total de cajas de resina a suministrar", "N_cajas", "=ROUNDUP({N_cart_tot}/{u_caja}, 0)", "und", "ROUNDUP(N_cart_tot / u_caja, 0)"),
        ("Masa total de resina epóxica requerida", "M_resina", "=({N_cart_tot}*{w_cart})/1000", "kg", "M_resina = N_cart_tot * w_cart / 1000"),
        ("Velocidad de perforación del Bolter Robótico", "v_bolter", r["vel_bolter"], "m/min", "Ficha técnica Bolter Robótico (06_Maquinaria)"),
        ("Tiempo de perforación pura por taladro", "t_perf_p", "={L_perno}/{v_bolter}", "min", "t_perf = L_perno / v_bolter"),
        ("Tiempo de posicionamiento y maniobra del brazo", "t_man_p", r["t_man_bolter"], "min", "1.00 min por taladro"),
        ("Tiempo de inyección de resina e inserción de perno", "t_iny_p", r["t_iny_bolter"], "min", "2.50 min por perno"),
        ("Tiempo de ciclo completo por perno instalado", "t_ciclo_p", "={t_perf_p}+{t_man_p}+{t_iny_p}", "min/perno", "t_ciclo = t_perf + t_man + t_iny"),
        ("TOTAL TIEMPO DE EMPERNADO CON BOLTER (HORAS)", "T_pernos_h", "=({N_pernos}*{t_ciclo_p})/60", "h", "T_h = (N_pernos * t_ciclo) / 60"),
    ]

    filas_shotcrete = [
        ("Área neta del frontón a sellar", "A_neta_s", "=Afrontonamiento_Portal!C22", "m²", "Vínculo dinámico a Afrontonamiento_Portal"),
        ("Espesor de diseño del concreto lanzado (Shotcrete)", "e_shot", r["e_shot_m"], "m", "e = 0.12 m (120 mm) para sellado Clase III"),
        ("Factor de pérdida por rebote (Lanzado robotizado)", "f_reb", r["rebote"], "-", "10% de rebote vía húmeda robotizada"),
        ("Volumen geométrico teórico de shotcrete", "V_shot_teo", "={A_neta_s}*{e_shot}", "m³", "V_teo = A_neta * e_shot"),
        ("Volumen real de producción considerando rebote", "V_shot_real", "={V_shot_teo}*(1+{f_reb})", "m³", "V_real = V_teo * (1 + f_reb)"),
        ("Dosificación de Cemento Portland Tipo I por m³", "Cem_m3", r["cem_kg_m3"], "kg/m³", "Diseño de mezcla f'c = 28 - 30 MPa"),
        ("Peso comercial de 1 bolsa de cemento", "w_bolsa", r["peso_bolsa_kg"], "kg/bolsa", "Estándar comercial en Perú (42.5 kg)"),
        ("Relación Agua / Cemento (A/C)", "Rel_AC", r["rel_ac"], "-", "Diseño reológico vía húmeda (0.58)"),
        ("Dosificación de agregado / arena graduada por m³", "Arena_m3", r["arena_kg_m3"], "kg/m³", "Huso granulométrico EFNARC (1,700 kg/m³)"),
        ("Porcentaje de aditivo acelerante SikaCem Gunite PE", "Pct_acel", r["acel_pct"], "-", "4.0% del peso del cemento"),
        ("Porcentaje de adición de Nanosílice / Microsílice", "Pct_nano", r["nano_pct"], "-", "1.0% del peso del cemento"),
        ("Dosificación de macrofibra sintética SikaFiber Force-60", "Fibra_m3", r["fibra_kg_m3"], "kg/m³", "Absorción de energía >= 500 J (EFNARC)"),
        ("Cemento total requerido para el frontón", "Cem_tot", "={V_shot_real}*{Cem_m3}", "kg", "Cem_tot = V_real * Cem_m3"),
        ("Cantidad total de bolsas de cemento (Redondeado)", "Bolsas_tot", "=ROUNDUP({Cem_tot}/{w_bolsa}, 0)", "und", "ROUNDUP(Cem_tot / 42.5, 0)"),
        ("Agua de mezcla total requerida", "Agua_tot_l", "={V_shot_real}*({Cem_m3}*{Rel_AC})", "L", "Agua(L) = V_real * (Cem_m3 * A/C)"),
        ("Arena graduada total requerida (Toneladas)", "Arena_tot_t", "=({V_shot_real}*{Arena_m3})/1000", "t", "Arena(t) = V_real * Arena_m3 / 1000"),
        ("Aditivo acelerante SikaCem total requerido", "Acel_tot", "={Cem_tot}*{Pct_acel}", "kg", "Acel_tot = Cem_tot * Pct_acel"),
        ("Nanosílice total requerida", "Nano_tot", "={Cem_tot}*{Pct_nano}", "kg", "Nano_tot = Cem_tot * Pct_nano"),
        ("Macrofibra sintética SikaFiber total requerida", "Fibra_tot", "={V_shot_real}*{Fibra_m3}", "kg", "Fibra_tot = V_real * Fibra_m3"),
        ("Rendimiento horario del Robot Lanzador de Shotcrete", "Rend_rob", r["rend_robot"], "m³/h", "Putzmeister Wetkret 4 / Normet (06_Maquinaria)"),
        ("Tiempo efectivo de lanzado robotizado", "t_lanz_h", "={V_shot_real}/{Rend_rob}", "h", "t_lanz = V_real / Rend_rob"),
        ("Tiempo de fraguado inicial requerido", "t_frag_h", r["t_fraguado_h"], "h", "Espera de endurecimiento temprano"),
        ("TOTAL TIEMPO DE APLICACIÓN Y FRAGUADO DE SHOTCRETE", "T_shot_h", "={t_lanz_h}+{t_frag_h}", "h", "T_shot = t_lanz + t_frag"),
    ]

    return Libro(
        "14_Afrontonamiento.xlsx",
        [
            Hoja(
                "RMR_Geomecanica",
                "Valoración Geomecánica RMR de Bieniawski (1989) en el Portal y Frontón",
                [tabla_parametros(filas_rmr, "Valoración RMR del Macizo Rocoso en el Frontón"), tabla_clases_rmr],
            ),
            Hoja(
                "Teoria_Cargas_Terzaghi",
                "Teoría de Cargas de Roca de Karl Terzaghi (1946) Aplicada al Frontón del Portal",
                [tabla_parametros(filas_terzaghi, "Cálculo de Altura de Carga (Hp) y Presión Vertical"), tabla_clases_terz],
            ),
            Hoja(
                "Afrontonamiento_Portal",
                "Geometría del Afrontonamiento y Sellado del Portal (Maniobra CAT 966H) — Área Neta",
                [tabla_parametros(filas_afrontonamiento, "Dimensionamiento del Frontón y Descuento de Sección del Túnel")],
            ),
            Hoja(
                "Malla_Electrosoldada",
                "Cálculo de Malla Electrosoldada Q-188 en el Frontón del Portal",
                [tabla_parametros(filas_malla, "Metrado de Paños con Traslape y Tiempo de Instalación")],
            ),
            Hoja(
                "Pernos_RockBolt",
                "Cálculo de Pernos Helicoidales RockBolt, Cartuchos de Resina y Ciclo del Bolter",
                [tabla_parametros(filas_pernos, "Dimensionamiento de Empernado Sistemático y Consumo de Resina")],
            ),
            Hoja(
                "Shotcrete_Robotizado",
                "Dosificación y Rendimiento de Shotcrete Vía Húmeda con Fibra Sintética (Sellado del Portal)",
                [tabla_parametros(filas_shotcrete, "Volúmenes, Insumos Sika y Tiempos de Lanzado Robotizado")],
            ),
        ],
    )
