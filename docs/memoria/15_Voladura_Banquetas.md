# 15 · Memoria de Cálculo: Perforación y Voladura de Banquetas de Portal en Superficie (Epiroc PowerROC T25 — Modelo C.J. Konya)

> Túnel Casmas Huaraz PA14 · Generado con `uv run pa14` desde `datos/parametros.toml`. **No editar a mano.**

## 1. Alcance y Diferenciación Operativa (Banquetas en Superficie vs. Túnel Subterráneo)

El presente documento (`15_Voladura_Banquetas.md` y libro `15_Voladura_Banquetas.xlsx`) desarrolla **exclusivamente la perforación y voladura en superficie (a cielo abierto con dos caras libres)** para la excavación escalonada de las **Banquetas y Taludes de los Portales de Entrada y Salida**, empleando la **Perforadora Hidráulica sobre Orugas (`Rockdrill`) Epiroc PowerROC T25** ($173\text{ HP}$, martillo en cabeza `RD 14UP`, broca de botones $\varnothing 64\text{ mm} = 2.5''$ con varillaje T38/T45).

> **Nota de separación técnica:** La perforación y voladura subterránea en el frente interior del túnel (que emplea el **Jumbo Frontal Computarizado de 3 brazos Sandvik DT1131 / XE3C** con barra de $3.66\text{ m}$ y broca $\varnothing 45\text{ mm}$) se encuentra en el entregable separado **`12_Voladura.xlsx`** y **`12_Voladura.md`**.

**Parámetros de Perforación y Voladura de Banquetas en Superficie (Epiroc PowerROC T25)**

| Parámetro | Símbolo | Valor | Unidad | Justificación Técnica (Konya) |
|---|---|---|---|---|
| Equipo de perforación en banquetas | Equipo | Epiroc PowerROC T25 | - | Perforadora sobre orugas (173 HP, martillo RD 14UP) |
| Diámetro de broca de botones | De_t25 | 64.0 | mm | Broca 2.5" T38/T45 (48 <= 64 <= 90 mm) |
| Explosivo base seleccionado | Tipo_e | semexsa E-80 | - | Densidad 1.18 g/cm³, VOD 4500 m/s |
| Macizo rocoso del portal | Tipo_r | Diorita PA14 (Caso Base) | - | Densidad 2.76 g/cm³, UCS 250 MPa |
| Burden máximo teórico | B_max | 1.82 | m | 3.15 * De(in) * (rho_e/rho_r)^(1/3) * 0.3048 |
| Error de perforación | e | 0.25 | m | 0.05 + 0.03 * L |
| Burden práctico ajustado | B_p | 1.58 | m | B_max - e |
| Espaciamiento práctico | S_p | 1.81 | m | 1.15 * B_p (roca dura) |
| Sobreperforación (Pasadura) | J_b | 0.55 | m | 0.30 * B_max |
| Longitud de taco | T_b | 1.34 | m | 0.85 * B_p |
| Concentración lineal de carga | q_l | 3.80 | kg/m | (pi/4) * De² * rho_e |
| Carga explosiva por taladro (H=6m) | Q_tal | 19.77 | kg/tal | q_l * L_c |
| Factor de potencia volumétrico | q_v | 1.15 | kg/m³ | Q_tal / V_tal |
| Factor de potencia másico | FP_g | 417.8 | g/t | (Q_tal / W_tal) * 1000 |
| Malla de Buffer (B_buf x E_buf) | Buffer | 1.23 x 1.41 | m | Fila amortiguada ante talud final |
| Espaciamiento de Precorte (70°) | E_pre | 0.33 | m | De(in) * (Pb + RT) / RT * 0.0254 |

## 2. Programación de Perforación y Voladura para los 5 Tramos de Banquetas (`11_Portales`)

Integrando los volúmenes geométricos in-situ de las 5 banquetas calculadas en `11_Portales.xlsx` ($3,795.21\text{ m}^3$ en banco) con la malla práctica de C.J. Konya ($B_p = 1.58\text{ m} \times S_p = 1.81\text{ m}$), se obtiene el requerimiento total de taladros, metros perforados, horas de operación de la **Epiroc PowerROC T25** y consumo de explosivo **Semexsa E-80**:

**Resumen de Perforación y Voladura por Tramo de Banqueta del Portal**

| Tramo de Banqueta (11_Portales) | H (m) | Volumen In-Situ (m³) | L Taladro (m) | N° Taladros | Metros Perf. (m) | Horas T25 (h) | Explosivo (kg) |
|---|---|---|---|---|---|---|---|
| Banqueta 01 - Tramo I | 2.5 | 115.94 | 3.05 | 17 | 51.8 | 2.1 | 110.2 |
| Banqueta 01 - Tramo II | 5.0 | 159.15 | 5.55 | 12 | 66.6 | 2.7 | 191.6 |
| Banqueta 02 - Tramo I | 5.0 | 1222.58 | 5.55 | 86 | 477.0 | 19.1 | 1373.4 |
| Banqueta 02 - Tramo II | 5.0 | 2064.95 | 5.55 | 145 | 804.3 | 32.2 | 2315.7 |
| Banqueta 02 - Portal Tramo III | 5.0 | 2707.38 | 5.55 | 190 | 1053.9 | 42.2 | 3034.3 |
| **TOTAL BANQUETAS** | - | **6270.00** | - | **450** | **2453.5** | **98.1** | **7025.3** |
