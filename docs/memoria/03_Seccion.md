# 03 · Sección del túnel — Memoria de cálculo y justificación normativa

> Túnel Casmas Huaraz PA14 · Generado con `uv run pa14` desde `datos/parametros.toml`. **No editar a mano.**

## 1. Objetivo

Definir y justificar la sección transversal del túnel según la normativa peruana del MTC, a partir del plano CAD del proyecto (9.58 m × 13.30 m).

## 2. Normativa aplicada

- MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14): gálibo vertical, veredas, zonas de emergencia.
- MTC Manual de Diseño Geométrico DG-2018, Sec. 304: ancho de carril y bermas.
- Valores normativos en `datos/parametros.toml` → `[seccion.norma]`.

## 3. Geometría de excavación

| Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente |
|---|---|---|---|---|
| Tipo de sección |  | Herradura: hastiales rectos + bóveda semicircular (R = B/2) |  | Plano CAD |
| Ancho de excavación | B | 13.3 | m | Plano CAD |
| Altura total (fondo → clave) | H | 9.58 | m | Plano CAD |
| Altura sobre rasante | Hr | 9.08 | m | Plano CAD |
| Espesor bajo rasante | e | 0.5 | m | H − Hr |
| Radio de bóveda | R | 6.65 | m | B / 2 |
| Hastial desde el fondo | hw | 2.93 | m | H − R |
| Hastial sobre rasante | hw' | 2.43 | m | hw − e |
| Área de excavación | A | 108.434 | m² | B·hw + π·B²/8 |
| Perímetro de excavación | P | 40.052 | m | B + 2·hw + π·B/2 |
| Área libre sobre rasante | Au | 101.784 | m² | A − B·e |

## 4. Gálibo y plataforma

| Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente |
|---|---|---|---|---|
| Número de carriles | n | 2 | und | Plano CAD |
| Ancho de carril | c | 3.6 | m | Plano CAD |
| Berma (cada lado) | b | 1.8 | m | Plano CAD |
| Separador central | s | 1 | m | Plano CAD |
| Ancho del gálibo | Wg | 11.8 | m | n·c + 2·b + s |
| Altura del gálibo | Hg | 5.5 | m | Plano CAD |
| Área del gálibo | Ag | 64.9 | m² | Wg · Hg |
| Vereda (cada lado) | v | 0.75 | m | Plano CAD |
| Ancho de plataforma | Wp | 13.3 | m | Wg + 2·v |
| Altura libre en borde del gálibo | hb | 5.498 | m | hw' + √(R² − (Wg/2)²) |
| Holgura gálibo – bóveda | Δ | -0.002 | m | hb − Hg |
| Ancho de cuneta | ac | 1.2 | m | Plano CAD |
| Profundidad de cuneta | pc | 0.4 | m | Plano CAD |
| Bombeo transversal | i | 2 | % | Plano CAD |

## 5. Verificación normativa

| Elemento | Proyecto | Mínimo | Unidad | Cumple | Fuente |
|---|---|---|---|---|---|
| Ancho de carril | 3.6 | 3.6 | m | Sí | MTC Manual de Diseño Geométrico DG-2018, Sec. 304 |
| Berma (cada lado) | 1.8 | 1.2 | m | Sí | MTC Manual de Diseño Geométrico DG-2018, Sec. 304 |
| Vereda (cada lado) | 0.75 | 0.75 | m | Sí | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Gálibo vertical | 5.5 | 5.5 | m | Sí | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Altura libre en borde del gálibo (bóveda) | 5.498 | 5.5 | m | Sí | Geometría: hw' + √(R² − (Wg/2)²), tolerancia 0.01 m |
| Altura libre sobre vereda (junto al hastial) | 2.43 | 2.4 | m | Sí | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Gálibo + 2 veredas = ancho B | 13.3 | 13.3 | m | Sí | Geometría del plano CAD |

Todas las comprobaciones **cumplen**.

## 6. Justificación de las dimensiones

- **Carriles de 3.60 m**: igual al mínimo de 3.60 m de la DG-2018 para carreteras de 1.ª clase, lo que permite el paso de vehículos pesados de obra y de servicio.
- **Bermas de 1.80 m**: superan la referencia de 1.20 m (S); dan espacio lateral de seguridad y para vehículos detenidos.
- **Veredas de 0.75 m** a cada lado: cumplen el mínimo del Manual de Túneles para mantenimiento y auxilio, aunque no circulen peatones.
- **Gálibo de 11.80 × 5.50 m**: la altura cumple el gálibo vertical mínimo de 5.50 m. En sus esquinas superiores la bóveda pasa a 5.498 m sobre la rasante (holgura -0.002 m, dentro de la tolerancia de 0.01 m del plano): el gálibo queda inscrito en el arco.
- **Bóveda semicircular de R = 6.65 m** sobre hastiales: forma que trabaja a compresión y se excava con perforación y voladura. El ancho B = Wg + 2·v = 13.30 m aloja gálibo y veredas.
- **Espesor bajo rasante de 0.50 m**: aloja el pavimento, la subbase y el drenaje (cunetas de 1.20 × 0.40 m y bombeo de 2.0 %).

## 7. Observaciones

- Longitud L = 5539.3 m > 500 m: prever **zonas de emergencia / apartaderos** (Manual de Túneles) (S).
- Los valores marcados **(S)** no están confirmados con el texto oficial; verificarlos en el manual correspondiente.
- El sostenimiento y el revestimiento dependen de la geología (02_Geologia, pendiente) y pueden cambiar la sección de excavación.
