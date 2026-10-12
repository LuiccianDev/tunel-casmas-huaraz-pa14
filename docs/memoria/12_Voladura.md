# 12 · Memoria de Cálculo: Perforación y Voladura Subterránea del Túnel (Jumbo 3 Brazos Sandvik DT1131)

> Túnel Casmas Huaraz PA14 · Generado con `uv run pa14` desde `datos/parametros.toml`. **No editar a mano.**

## 1. Alcance y Diferenciación Operativa (Túnel Subterráneo vs. Banquetas en Superficie)

El presente documento (`12_Voladura.md` y libro `12_Voladura.xlsx`) desarrolla **exclusivamente la perforación y voladura subterránea en el frente de ataque del Túnel Casmas Huaraz PA14** ($B = 13.30\text{ m}, H = 9.58\text{ m}, A = 108.43\text{ m}^2$), donde se trabaja con **una sola cara libre inicial** empleando el **Jumbo Frontal Computarizado de 3 brazos Sandvik DT1131 / XE3C** ($300\text{ HP}$, barra de $12\text{ pies} = 3.66\text{ m}$, broca de producción $\varnothing 45\text{ mm}$ y escariador de alivio $\varnothing 102\text{ mm}$).

> **Nota de separación técnica:** La perforación y voladura a cielo abierto para los cortes escalonados de las **Banquetas y Taludes de Portal en Superficie** (que emplea la perforadora hidráulica sobre orugas **Epiroc PowerROC T25** con broca $\varnothing 64\text{ mm}$ y el modelo de bancos de C.J. Konya) se encuentra independizada en el entregable **`15_Voladura_Banquetas.xlsx`** y su memoria **`15_Voladura_Banquetas.md`**.

**Resumen de Perforación y Voladura Subterránea del Frente del Túnel (Jumbo 3 Brazos Sandvik DT1131)**

| Parámetro del Frente Subterráneo | Símbolo | Valor | Unidad | Criterio / Fuente |
|---|---|---|---|---|
| Equipo de perforación subterránea | Eq_tunel | Jumbo Frontal Computarizado 3 brazos Sandvik DT1131 / XE3C | - | 3 brazos automatizados iDATA |
| Área de excavación del frente | A_tun | 108.43 | m² | Sección herradura 13.30 x 9.58 m |
| Longitud de barreno (12 pies) | L_bar | 3.66 | m | Barra estándar Jumbo Sandvik DT1131 |
| Avance efectivo por disparo (90%) | Av_disp | 3.29 | m | L_bar * 0.90 |
| Volumen in-situ por disparo | V_disp | 357.18 | m³ | A_tun * Av_disp |
| Taladros vacíos de alivio (Ø 102 mm) | N_aliv | 4 | taladros | Escariados sin carga en el cuele |
| Taladros cargados en el frente (Ø 45 mm) | N_carg | 231 | taladros | Cuele (16) + Ayudas (20) + Destroza (105) + Contorno (64) + Arrastres (26) |
| Total de taladros perforados por disparo | N_perf | 235 | taladros | N_carg + N_aliv |
| Tiempo neto de perforación (3 brazos) | T_perf_h | 3.19 | h/disparo | M_perf / (Vp * 3 brazos * 60) |
| Consumo de explosivo por disparo | Q_disp_kg | 571.49 | kg/disparo | V_disp * 1.60 kg/m³ |

## 2. Modelo Matemático de C.J. Konya en la Zona de Destroza del Frente

Una vez aperturada la cavidad inicial por el **cuele quemado cilíndrico de 4 secciones** y sus ayudas, los taladros del núcleo de **destroza/producción** trabajan hacia la cara libre interna generada, rigiéndose por las relaciones del modelo de C.J. Konya para $\varnothing 45\text{ mm}$:

**Parámetros de Destroza Subterránea (Modelo Matemático de C.J. Konya)**

| Parámetro | Símbolo | Valor | Unidad | Criterio / Fórmula Konya |
|---|---|---|---|---|
| Diámetro de taladro de producción | De | 45 | mm | Jumbo 3 brazos Sandvik DT1131 |
| Densidad del explosivo | Sge | 1.2 | g/cm³ | Emulsión encartuchada / ANFO Pesado |
| Densidad de la roca | Sgr | 2.6 | g/cm³ | Litología ponderada PA14 |
| Burden teórico de Konya en destroza | B | 1.31 | m | 0.012 * (2*Sge/Sgr + 1.5) * De |
| Burden corregido (Kr, Kd, Ks) | Bc | 1.30 | m | B * Kr * Kd * Ks |
| Espaciamiento en destroza | S | 1.83 | m | 1.4 * B |
| Taco inerte | T | 0.92 | m | 0.7 * B |
| Carga total por taladro de destroza | Qt | 5.29 | kg/tal | (Cf + Cc) * Qbk |
| Factor de carga volumétrico en destroza | FC | 0.67 | kg/m³ | Qt / V |
| Retardo barreno a barreno | th | 8.2 | ms | Th * S |
| Retardo entre secciones | tR | 15.0 | ms | TR * B |
