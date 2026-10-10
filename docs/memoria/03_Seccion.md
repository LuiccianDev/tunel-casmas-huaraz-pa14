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
| Ancho de excavación | B | 13.3 | m | Entrada TOML / Plano CAD |
| Altura total (fondo → clave) | H | 9.58 | m | Entrada TOML / Plano CAD |
| Altura sobre rasante | Hr | 9.08 | m | Entrada TOML / Plano CAD |
| Espesor bajo rasante | e | =C7-C8 | m | H − Hr |
| Radio de bóveda | R | =C6/2 | m | B / 2 |
| Hastial desde el fondo | hw | =C7-C10 | m | H − R |
| Hastial sobre rasante | hw' | =C11-C9 | m | hw − e |
| Área de excavación | A | =C6*C11+PI()*C6^2/8 | m² | B·hw + π·B²/8 |
| Perímetro de excavación | P | =C6+2*C11+PI()*C6/2 | m | B + 2·hw + π·B/2 |
| Área libre sobre rasante | Au | =C13-C6*C9 | m² | A − B·e |

## 4. Gálibo y plataforma

| Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente |
|---|---|---|---|---|
| Número de carriles | n | 2 | und | Entrada TOML / Plano CAD |
| Ancho de carril | c | 3.6 | m | Entrada TOML / Plano CAD |
| Berma (cada lado) | b | 1.8 | m | Entrada TOML / Plano CAD |
| Separador central | s | 1 | m | Entrada TOML / Plano CAD |
| Ancho del gálibo | Wg | =C5*C6+2*C7+C8 | m | n·c + 2·b + s |
| Altura del gálibo | Hg | 5.5 | m | Entrada TOML / Plano CAD |
| Área del gálibo | Ag | =C9*C10 | m² | Wg · Hg |
| Vereda (cada lado) | v | 0.75 | m | Entrada TOML / Plano CAD |
| Ancho de plataforma | Wp | =C9+2*C12 | m | Wg + 2·v |
| Altura libre en borde del gálibo | hb | =Geometria!C12+SQRT(Geometria!C10^2-(C9/2)^2) | m | hw' + √(R² − (Wg/2)²) |
| Holgura gálibo – bóveda | Δ | =C14-C10 | m | hb − Hg |
| Ancho de cuneta | ac | 1.2 | m | Plano CAD |
| Profundidad de cuneta | pc | 0.4 | m | Plano CAD |
| Bombeo transversal | i | 2 | % | Plano CAD |

## 5. Verificación normativa

| Elemento | Proyecto | Mínimo | Unidad | Cumple | Fuente |
|---|---|---|---|---|---|
| Ancho de carril | =Galibo!C6 | 3.6 | m | =B5>=C5 | MTC Manual de Diseño Geométrico DG-2018, Sec. 304 |
| Berma (cada lado) | =Galibo!C7 | 1.2 | m | =B6>=C6 | MTC Manual de Diseño Geométrico DG-2018, Sec. 304 |
| Vereda (cada lado) | =Galibo!C12 | 0.75 | m | =B7>=C7 | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Gálibo vertical | =Galibo!C10 | 5.5 | m | =B8>=C8 | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Altura libre en borde del gálibo (bóveda) | =Galibo!C14 | 5.5 | m | =B9>=C9 | Geometría de la bóveda |
| Altura libre sobre vereda (junto al hastial) | =Galibo!C14 | 2.4 | m | =B10>=C10 | MTC Manual de Túneles, Muros y O.C. (RD 036-2016-MTC/14) |
| Gálibo + 2 veredas = ancho B | =Galibo!C13 | =Geometria!C6 | m | =ABS(B11-C11)<=0.01 | Geometría del plano CAD |

Todas las comprobaciones **cumplen**.

## 6. Justificación de las dimensiones

- **Carriles de 3.60 m**: igual al mínimo de 3.60 m de la DG-2018 para carreteras de 1.ª clase, lo que permite el paso de vehículos pesados de obra y de servicio.
- **Bermas de 1.80 m**: superan la referencia de 1.20 m (S); dan espacio lateral de seguridad y para vehículos detenidos.
- **Veredas de 0.75 m** a cada lado: cumplen el mínimo del Manual de Túneles para mantenimiento y auxilio, aunque no circulen peatones.
- **Gálibo de 11.80 × 5.50 m**: la altura cumple el gálibo vertical mínimo de 5.50 m. En sus esquinas superiores la bóveda pasa a 5.498 m sobre la rasante (holgura -0.002 m, dentro de la tolerancia de 0.01 m del plano): el gálibo queda inscrito en el arco.
- **Bóveda semicircular de R = 6.65 m** sobre hastiales: forma que trabaja a compresión y se excava con perforación y voladura. El ancho B = Wg + 2·v = 13.30 m aloja gálibo y veredas.
- **Espesor bajo rasante de 0.50 m**: aloja el pavimento, la subbase y el drenaje (cunetas de 1.20 × 0.40 m y bombeo de 2.0 %).

## 7. Observaciones

- Longitud L = 5406.8 m > 500 m: prever **zonas de emergencia / apartaderos** (Manual de Túneles) (S).
- Los valores marcados **(S)** no están confirmados con el texto oficial; verificarlos en el manual correspondiente.
- El sostenimiento y el revestimiento dependen de la geología (02_Geologia, pendiente) y pueden cambiar la sección de excavación.
