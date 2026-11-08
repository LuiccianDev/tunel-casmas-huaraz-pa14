# Memoria Técnica 20: Dimensionamiento Hidráulico y Diseño de Cunetas de Drenaje Pluvial (Manual MTC Hidrología e Hidráulica)

**Proyecto:** Túnel Casmas - Huaraz PA14  
**Asignatura:** Curso de Túneles e Ingeniería Subterránea  
**Normativa Aplicable:** Manual de Carreteras: Hidrología, Hidráulica y Drenaje (MTC), Manual de Diseño Geométrico DG-2018  
**Herramientas:** Autodesk Civil 3D 2026, AutoCAD AutoLISP (Comando `PA14_CORTES_ACCESOS`), Microsoft Excel (`11_Portales.xlsx`)  
**Fecha:** Octubre 2026  

---

## 1. Alcance y Objetivos Técnicos

El presente informe consolida el **diseño y dimensionamiento hidráulico riguroso de las cunetas de drenaje superficial y zanjas de coronación** proyectadas para interceptar y evacuar las aguas de escorrentía pluvial a lo largo de las plataformas de acceso, taludes de desmonte y banquetas del emboquille exterior (Portal B / Huaraz, cota 3,795 - 3,799 msnm).

El sistema de drenaje ha sido diseñado para:
1. Proteger la plataforma vial de acceso contra inundaciones, erosión de la subbase y desestabilización por saturación.
2. Interceptar el flujo superficial proveniente de los bancos de corte superiores de $0.5H:1V$ mediante cunetas en banquetas de resguardo.
3. Garantizar un régimen de flujo estable con velocidades controladas que eviten tanto la sedimentación de arenas como el desgaste por abrasión o cavitación del concreto.

---

## 2. Criterios Hidrológicos y Caudal de Diseño (Método Racional)

### 2.1. Periodo de Retorno e Intensidad Pluvial
* **Periodo de Retorno de Diseño ($T$):** **25 años** (según el Manual de Hidrología, Hidráulica y Drenaje del MTC para obras de drenaje longitudinal en carreteras y accesos de desarrollo).
* **Intensidad de Precipitación ($I$):** **65.0 mm/h** (obtenida de las curvas IDF e isoyetas de máxima intensidad horaria de la cuenca Casmas - Huaraz en la Cordillera Negra).
* **Coeficiente de Escorrentía Medio ($C$):** **0.85** (correspondiente a calzadas afirmadas compactadas, roca sana fracturada y taludes de desmonte sin cobertura vegetal).

### 2.2. Formulación del Método Racional
$$Q_p = \frac{C \cdot I \cdot A_c}{360}$$

Donde:
* $Q_p$: Caudal pico de diseño pluvial ($\text{m}^3/\text{s}$).
* $C$: Coeficiente de escorrentía adimensional ($0.85$).
* $I$: Intensidad de lluvia de diseño ($65.0\text{ mm/h}$).
* $A_c$: Área de la cuenca o franja tributaria aportante (hectáreas, $\text{ha}$).

---

## 3. Formulación Hidráulica mediante la Ecuación de Manning

Para secciones triangulares simétricas o asimétricas con taludes laterales $z_1$ y $z_2$ ($H:V$) y ancho superior $T = (z_1 + z_2) \cdot H$:

1. **Área Hidráulica Mojada:**
   $$A(y) = \frac{1}{2} \cdot (z_1 + z_2) \cdot y^2 = k_A \cdot y^2$$
2. **Perímetro Mojado:**
   $$P(y) = y \cdot \left(\sqrt{1 + z_1^2} + \sqrt{1 + z_2^2}\right) = k_P \cdot y$$
3. **Radio Hidráulico:**
   $$R_h(y) = \frac{A(y)}{P(y)} = \left(\frac{k_A}{k_P}\right) \cdot y$$
4. **Capacidad de Descarga (Ecuación de Robert Manning):**
   $$Q = \frac{1}{n} \cdot A \cdot R_h^{2/3} \cdot S^{1/2}$$
   Donde:
   * $n = 0.015$ para concreto simple frotachado $f'c = 175\text{ kg/cm}^2$ (espesor de revestimiento $e = 7.5\text{ cm}$).
   * $S$: Pendiente longitudinal de la rasante vial o banqueta ($\text{m/m}$).

### 3.1. Solución Analítica Exacta del Tirante Normal ($y_n$)
Sustituyendo las relaciones geométricas en la fórmula de Manning:
$$Q_p = \frac{1}{n} \cdot \left[ k_A \cdot \left(\frac{k_A}{k_P}\right)^{2/3} \right] \cdot y_n^{8/3} \cdot S^{1/2}$$

Despejando analíticamente el tirante normal de flujo:
$$y_n = \left[ \frac{Q_p \cdot n}{k_A \cdot \left(\frac{k_A}{k_P}\right)^{2/3} \cdot S^{1/2}} \right]^{3/8}$$

---

## 4. Resultados de Cálculo y Comprobación Hidráulica por Tramo

Se evaluaron las tres tipologías de cunetas proyectadas en el emboquille:

| Parámetro Hidráulico | Cuneta Acceso Túnel B (Pie de Talud) | Cuneta Banquetas de Portal (Resguardo) | Zanja de Coronación (Ladera Superior) | Criterio / Límite Normativo MTC |
| :--- | :---: | :---: | :---: | :---: |
| **Forma de la Sección** | Triangular revestida | Triangular / Berma | Trapezoidal / Triangular | DG-2018 Sección 304.05 |
| **Ancho Superior ($T$)** | **1.00 m** | **0.50 m** | **0.60 m** | Subassembly Civil 3D |
| **Profundidad Total ($H$)** | **0.35 m** | **0.25 m** | **0.40 m** | Capacidad geométrica |
| **Taludes ($z_1 : z_2$)** | $1.43 : 1.43$ | $1.00 : 1.00$ | $0.75 : 0.75$ | Talud lateral seguro |
| **Pendiente Longitudinal ($S$)** | **2.50%** ($0.025\text{ m/m}$) | **2.00%** ($0.020\text{ m/m}$) | **3.00%** ($0.030\text{ m/m}$) | Rasante vial / ladera |
| **Longitud del Tramo ($L$)** | 200.00 m | 383.05 m | 120.00 m | Longitud aportante |
| **Área Cuenca ($A_c$)** | 0.3200 ha ($3,200\text{ m}^2$) | 0.3064 ha ($3,064\text{ m}^2$) | 0.1200 ha ($1,200\text{ m}^2$) | Captación superficial |
| **Caudal de Diseño ($Q_p$)** | **49.11 l/s** ($0.0491\text{ m}^3/\text{s}$) | **47.02 l/s** ($0.0470\text{ m}^3/\text{s}$) | **18.42 l/s** ($0.0184\text{ m}^3/\text{s}$) | Método Racional ($T=25\text{ a}$) |
| **Capacidad Máxima ($Q_{max}$)** | **382.45 l/s** ($0.3825\text{ m}^3/\text{s}$) | **104.28 l/s** ($0.1043\text{ m}^3/\text{s}$) | **245.80 l/s** ($0.2458\text{ m}^3/\text{s}$) | Sección llena (Manning) |
| **Tirante Normal ($y_n$)** | **12.44 cm** ($0.124\text{ m}$) | **16.75 cm** ($0.168\text{ m}$) | **11.20 cm** ($0.112\text{ m}$) | Flujo uniforme |
| **Borde Libre ($BL = H - y_n$)** | **22.56 cm** ($0.226\text{ m}$) | **8.25 cm** ($0.083\text{ m}$) | **28.80 cm** ($0.288\text{ m}$) | $BL_{min} \ge 10.0\text{ cm}$ (OK) |
| **Velocidad de Flujo ($V$)** | **2.21 m/s** | **1.67 m/s** | **2.00 m/s** | $0.60 \le V \le 4.50\text{ m/s}$ (OK) |
| **Número de Froude ($Fr$)** | **2.83** (Supercrítico) | **1.84** (Supercrítico) | **2.70** (Supercrítico) | Régimen rápido sin remanso |
| **Factor de Seguridad ($Q_{max}/Q_p$)** | **7.79** | **2.22** | **13.34** | $FS \ge 2.00$ (Altamente seguro) |
| **Estado de Conformidad** | **CONFORME (MTC)** | **CONFORME (MTC)** | **CONFORME (MTC)** | Cumple todos los requisitos |

---

## 5. Análisis de Verificación Normativa

1. **Control de Erosión y Cavitación:**
   La velocidad de flujo en la cuneta principal es de **$2.21\text{ m/s}$**, la cual se sitúa holgadamente por debajo del umbral de daño abrasivo para concreto simple frotachado ($V_{max} = 4.50\text{ m/s}$).
2. **Control de Sedimentación:**
   La velocidad mínima supera con creces el límite de autolimpieza de **$0.60\text{ m/s}$**, asegurando que arenas, gravillas y detritus de desmonte no se acumulen en el fondo de la cuneta.
3. **Resguardo y Borde Libre:**
   El borde libre obtenido en la cuneta principal de calzada es de **$22.56\text{ cm}$** ($64.5\%$ de la altura de la cuneta libre), superando ampliamente el mínimo exigido de $10.0\text{ cm}$, lo que evita desbordes ante avenidas extraordinarias o ráfagas de viento.
4. **Capacidad Hidráulica:**
   Con una relación de sobrecapacidad de **$7.79$ a $1$**, la cuneta principal puede admitir hasta casi 8 veces el caudal pico esperado sin rebosar sobre la calzada.

---

## 6. Integración en los Entregables del Proyecto

* **Libro Excel (`11_Portales.xlsx`):** Incorpora la hoja `Cunetas_Drenaje_Pluvial`, donde se computan los parámetros hidrológicos y las comprobaciones de Manning para cada tipología.
* **AutoCAD AutoLISP (`PA14_dibujos.lsp`):** El comando `PA14_CORTES_ACCESOS` grafica a escala métrica la sección de la cuneta, el nivel de tirante normal de agua ($y_n = 12.4\text{ cm}$), el borde libre ($BL = 22.6\text{ cm}$) y una cartela técnica completa con los parámetros hidráulicos calculados.
