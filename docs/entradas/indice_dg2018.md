# Índice Rápido de Líneas — Manual de Carreteras DG-2018 y Entradas Técnicas

> **Propósito (Ahorro de Tokens y Tiempo):** Antes de leer [`manual_de_carreteras_dg_2018.md`](./manual_de_carreteras_dg_2018.md) ($13,268\text{ líneas}$), consulta esta tabla y usa `view_file` indicando únicamente el rango `StartLine` y `EndLine` necesario (~40–80 líneas). **Prohibido** leer el archivo completo o los `.pdf` originales.

---

## 1. Mapa de Coordenadas en `docs/entradas/manual_de_carreteras_dg_2018.md`

| Sección / Tabla / Figura | Contenido Técnico | Rango de Líneas (`StartLine`–`EndLine`) | Página PDF Original |
|---|---|---|---|
| **Índice General** | Estructura completa del manual DG-2018 | `15` – `355` | Págs. 1–7 |
| **Sección 101** | Clasificación por demanda (Autopistas 1ra/2da clase, Carreteras 1ra/2da/3ra clase, Trochas) | `468` – `522` | Págs. 12–13 |
| **Sección 102** | Clasificación por orografía (Plano Tipo 1, Ondulado Tipo 2, Accidentado Tipo 3, Escarpado Tipo 4) | `523` – `550` | Pág. 14 |
| **Sección 202 y Tabla 202.01** | Vehículos de diseño (VL, B2, B3-1, B4-1, BA-1, C2, C3, T2S1, T3S2): dimensiones, vuelos y radios de giro | `954` – `1130` | Págs. 24–28 |
| **Sección 204 y Tabla 204.01** | Velocidad de diseño ($V_d$ de $30\text{ a }130\text{ km/h}$) según clasificación y orografía | `3056` – `3160` | Págs. 96–98 |
| **Sección 205 y Tabla 205.01** | Distancia de visibilidad de parada ($D_p$) en función de velocidad y pendiente | `3402` – `3535` | Págs. 103–105 |
| **Tabla 205.03** | Distancia de visibilidad de paso o adelantamiento ($D_a$) | `3750` – `3810` | Pág. 109 |
| **Sección 302 y Tabla 302.02** | Curvas horizontales: Radios mínimos ($R_{\min}$) y peraltes máximos ($p_{\max} \in \{4\%, 6\%, 8\%, 12\%\}$) | `4472` – `4750` | Págs. 125–129 |
| **Figuras 302.02–302.05** | Ábacos de peralte $e(R, V)$ para zonas urbanas y rurales | `4751` – `5050` | Págs. 130–131 |
| **Sección 302.06–302.07** | Curvas de transición (Clotoide / Espiral de Euler) y longitudes mínimas de transición $L_{\min}$ | `5100` – `5415` | Págs. 135–142 |
| **Sección 302.08 y Tablas 302.13–302.18** | Transición de peralte ($i_{p,\max} = 1.8 - 0.01V$, longitudes $L_t$) | `6200` – `6580` | Págs. 152–155 |
| **Sección 302.09 y Figura 302.18B** | Sobreancho en curvas ($S_a = n(R - \sqrt{R^2 - L^2}) + \frac{V}{10\sqrt{R}}$, $S_{a,\min} = 0.40\text{ m}$) | `6630` – `6765` | Págs. 160–161 |
| **Tabla 302.20 y Art. 302.09.04** | Factores de reducción de sobreancho y longitud de desarrollo del sobreancho | `6766` – `6850` | Págs. 162–163 |
| **Sección 303 y Tabla 303.01** | Perfil longitudinal: Pendientes máximas ($p_{\max}$) según demanda, orografía y $V_d$ | `7183` – `7350` | Págs. 174–176 |
| **Sección 303.04 y Figuras 303.06–303.08** | Curvas verticales parabólicas y parámetro $K$ ($K_{\text{SSD}} = D_p^2/404$, $K_{\text{PSD}} = D_a^2/946$, $K_{\text{HSD}}$) | `7351` – `7950` | Págs. 177–182 |
| **Sección 304 y Tabla 304.01** | Sección transversal: Anchos mínimos de calzada ($6.00, 6.60, 7.20\text{ m}$) y bermas (**Tabla 304.02**) | `8380` – `8560` | Págs. 191–194 |
| **Tabla 304.03** | Valores de bombeo de la calzada ($2.0\%$ pavimentado) | `8561` – `8605` | Pág. 195 |
| **Sección 304.08–304.10 y Figura 304.07** | Taludes de corte/relleno y diseño de **Banquetas** (corte $>7\text{ m}$, ancho $3\text{ m}$, sep. $10\text{ m}$) | `8820` – `8960` | Págs. 200–203 |

---

## 2. Catálogo de Documentos de Entrada en Markdown (`docs/entradas/`)

Todos los documentos en PDF han sido convertidos con `MarkItDown` a texto estructurado `.md`. **Consulta siempre el archivo `.md`:**

| Archivo `.md` Listo para Consulta | Líneas Totales | Contenido Principal |
|---|---|---|
| [`manual_de_carreteras_dg_2018.md`](./manual_de_carreteras_dg_2018.md) | `13,268` | Norma completa DG-2018 MTC Perú (usar rangos de la tabla superior). |
| [`marco_regulatorio_tecnico.md`](./marco_regulatorio_tecnico.md) | `895` | Resumen normativo del proyecto (DS 024-2016-EM, RNE, SUCAMEC, MC-03-16 Túneles). |
| [`fichas_tecnicas_maquinaria.md`](./fichas_tecnicas_maquinaria.md) | `742` | Especificaciones técnicas reales de flota subterránea y superficie (Jumbo, Scooptram, Dumper, etc.). |
| [`catalogo_explosivos_y_bibliografia_unidad2.md`](./catalogo_explosivos_y_bibliografia_unidad2.md) | `215` | Fichas de explosivos EXSA (Semexsa, Exadit, Gelatina Especial) y parámetros de voladura. |
| [`formulario_konya.md`](./formulario_konya.md) | `322` | Ecuaciones de C. J. Konya para burden ($B$), espaciamiento ($S$), taco ($T$) y sobreperforación ($J$). |
| [`ejemplo_resolucion_modelo_konya.md`](./ejemplo_resolucion_modelo_konya.md) | `395` | Ejercicio resuelto paso a paso del modelo de Konya en bancos/banquetas. |
| [`modelo_konya_eficientes.md`](./modelo_konya_eficientes.md) | `2,210` | Teoría completa de diseño de voladuras eficientes por el método de Konya. |
| [`modelo_konya_voladura_ii.md`](./modelo_konya_voladura_ii.md) | `370` | Diapositivas y tablas de corrección ($K_d, K_e, K_r$) del modelo de Konya. |
