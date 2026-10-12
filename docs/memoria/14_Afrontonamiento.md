# 14 · Memoria de Cálculo: Afrontonamiento y Sellado del Portal de Emboquille

> Túnel Casmas Huaraz PA14 · Generado con `uv run pa14` desde `datos/parametros.toml`. **No editar a mano.**

## 1. Fundamento y Geometría del Afrontonamiento del Portal

El **afrontonamiento y sellado del portal** prepara y estabiliza el talud frontal exterior de emboquille antes de iniciar el avance subterráneo del túnel. Su dimensionamiento integra la **Teoría de Cargas de Roca de Karl Terzaghi (1946)** para un macizo Clase III ($\text{RMR} = 42$, Condición 4: *roca medianamente fracturada en bloques algo abiertos*, $H_p = 0.35(B + H_t)$) con la envolvente cinemática de giro del cargador frontal **Caterpillar 966H** ([Ficha Técnica en Drive](https://drive.google.com/file/d/1MmeCiUDpEDKpKdOn1hrj8rbDK1uqPrcL/view)), descontando el área de la sección herradura del túnel ($108.43\text{ m}^2$) para obtener el **Área Neta del Frontón a Sellar ($493.08\text{ m}^2$)**.

**Síntesis de Ingeniería del Afrontonamiento y Sellado del Portal**

| Componente / Parámetro | Valor Calculado | Unidad | Criterio Técnico / Fuente |
|---|---|---|---|
| Valoración Geomecánica RMR Básico / Corregido | 57 / 52 | pts | Bieniawski (1989) — Clase III (Roca Regular) |
| Altura de carga de roca aflojada (Hp Terzaghi) | 8.008 | m | Condición 4: Hp = 0.35 * (B + Ht) |
| Altura total del frontón (Ht + Hp) | 17.588 | m | Ht = 9.58 m + Hp = 8.01 m |
| Presión vertical de diseño sobre clave | 212.212 | kPa | gamma = 26.5 kN/m³ * Hp |
| Ancho total de maniobra en portal (CAT 966H) | 34.2 | m | 2 * (R_giro 7.26 + L_eq 8.84 + D_seg 1.0) |
| Área bruta del frontón | 601.51 | m² | Ancho frontón * Altura frontón |
| Área de la sección herradura del túnel descontada | 108.434 | m² | 03_Seccion (13.30 x 9.58 m) |
| ÁREA NETA A SELLAR / AFRONTONAR EN EL PORTAL | 493.076 | m² | Área bruta - Área sección del túnel |
| Paños de malla electrosoldada (6.0 x 2.4 m, traslape 0.30 m) | 42 | paños | Área útil 11.97 m²/paño (10.50 h) |
| Pernos RockBolt (L=3.0 m, d=22 mm, malla 1.5x1.5 m) | 220 | pernos | Ciclo Bolter Robótico: 20.17 h |
| Cartuchos de resina epóxica (28x305 mm, 320 g) | 1540 | cartuchos | 7 cart/perno (31 cajas, 492.8 kg) |
| Volumen real de Shotcrete (e=0.12 m + 10% rebote) | 65.086 | m³ | Cemento: 651 bolsas, Fibra: 260.3 kg (5.71 h) |
