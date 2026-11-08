# Memoria Técnica 16: Extracción, Catalogación e Integración de Datos Técnicos de la Unidad 2 (Google Drive)

**Proyecto:** Túnel Casmas - Huaraz PA14  
**Asignatura:** Curso de Túneles e Ingeniería Subterránea  
**Fuente:** Google Drive (`INGENIERIA DE TUNELES Y CONSTRUCCIONES` / `UNIDAD 2`)  
**Modo de Extracción:** Solo Lectura (`gdrive readonly` / `gsheets readonly`)  
**Fecha de Integración:** Octubre 2026  

---

## 1. Resumen Ejecutivo y Alcance

El presente documento consolida la extracción sistemática, auditoría técnica e integración de los datos de diseño, cálculos geomecánicos, voladura según el modelo de Konya, ciclo de carguío y acarreo, rendimientos de maquinaria y movimiento de tierras provenientes de la **Unidad 2** del Google Drive del proyecto.

La extracción se ejecutó de forma automatizada mediante el script reproducible [`scripts/utils/extraer_drive_unidad2.py`](file:///c:/Users/DAVID/Desktop/WorksSpacesCoding/Tunel-Casmas-Huaraz-PA14/scripts/utils/extraer_drive_unidad2.py), garantizando **cero modificaciones** en los archivos originales de la nube. Todos los insumos fueron volcados localmente en `docs/entradas/drive_unidad2/` y sincronizados de manera reactiva con la única fuente de verdad: `datos/parametros.toml`.

---

## 2. Inventario y Manifiesto de Archivos Extraídos

Se identificaron y exportaron **21 archivos técnicos** estructurados por especialidad:

| Archivo Local en `docs/entradas/drive_unidad2/` | ID en Google Drive | Tipo Original | Dominio de Ingeniería |
| :--- | :--- | :--- | :--- |
| `coordenadas_utm_tunel.xlsx` | `1lzhXHQvGIcmt5F7GhP8Sr_0J3VTQxLny` | Excel nativo | Geodesia y Coordenadas UTM WGS84 18L |
| `geomecanica_portal.xlsx` | `1LKo5grbDMbr5QdpeSUCYH5g2oa9HjnHJ` | Excel nativo | Caracterización Geomecánica RMR Portal |
| `progresivas_unidades_geologicas.xlsx` | `1g1p8uX4qho_d6sqxNQorLwpstGRbSnJM` | Excel nativo | Trazado, UCS y RMR por tramos litológicos |
| `angulo_banquetas_qslope.xlsx` | `1TwFMUmf6x_XEYKtXGJbfIlz7sBn6HOBs` | Excel nativo | Estabilidad de Taludes (Bar & Barton, 2015) |
| `diseno_voladura_modelo_matematico_konya.xlsx` | `1pJ3qQnuhieGWgvnHXgyiWn-f5ViYLTjiePYm2dVGb3M` | Google Sheet | Modelo Matemático de C.J. Konya en Banco |
| `catalogo_tecnico_explosivos.xlsx` | `1zOyNlzrxZZRYssSwzLJIHF21G55R_9whUUW45qSPHl4` | Google Sheet | Propiedades Detonantes y Catálogo EXSA |
| `diseno_sostenimiento_fronton.xlsx` | `1arW5QsWjCDrVcqNq1inpaS-034rFII0oOb1bWf5oPug` | Google Sheet | Sostenimiento de Emboquille y Cargas Terzaghi |
| `voladura_afrontonamiento.xlsx` | `1MdplFahB9IX9JxW7eoGDXBh-_8y8sUBVZ2zHAhRcwg0` | Google Sheet | Esquema de Precorte y Amortiguación |
| `malla_1_disparo.xlsx` | `1GKwDcfNkIKsXb19kBsTx7bcTjsK70ba2` | Excel nativo | Malla de Perforación 1 alivio (141 taladros) |
| `malla_2_alivio.xlsx` | `1fmvD9j6vt7ck2Ehe9FDhQ0I8WW1r2kQ_` | Excel nativo | Malla de Perforación 2 alivios (142 taladros) |
| `calculo_carguio_acarreo_tunel.xlsx` | `1arR4Q02xLxwMEgh_1Y2b5tzdX2gYUr82ckDVcqs_KuI` | Google Sheet | Ciclo Cat 966H + Volvo FMX 8x4 y Match Factor |
| `ciclo_carguio_acarreo.xlsx` | `1Piyj7nNlarAFUhqjRtpEpq59M6uF1DjL` | Excel nativo | Tiempos de ida/retorno en rampa de acceso |
| `rendimientos_equipos.xlsx` | `1NVqWEkHN2DZvVoEFiwsoUurbljQP087h` | Excel nativo | Fichas de Rendimiento Teórico y Real (CAT/Epiroc) |
| `maquinaria_rendimiento_equipos.xlsx` | `17aCWjuscQhD6EeDudXmKORD7VwV0fsbSjIgqmAvOrng` | Google Sheet | Catálogo Consolidado de 25+ Equipos de Obra |
| `tiempos_vias_acceso.xlsx` | `1iGFpU3zw8QzjCQTFq-TZpJFMg9fEQPi9` | Excel nativo | Cubicación por progresivas y desbroce de vía |
| `dimensiones_assembly_accesos.xlsx` | `1Qdyk_2IgjNaHaa__BIS9Z2WUQQD_DzNAOt4SXtv8YKc` | Google Sheet | Secciones transversales típicas de accesos |
| `mov_tierra_acceso_banquetas.xlsx` | `1TDm5EWEHaFlmOybf2TBsBH6KGz1kGJ3U324AoG8Igu4` | Google Sheet | Volúmenes de movimiento de tierras Banquetas 1 y 2 |
| `mov_tierra_acceso_botadero.xlsx` | `1HbAXZ_-4mMmvdKSxhIqXX6U_k045FMOUk229Smeq10o` | Google Sheet | Volúmenes de corte y relleno acceso a botadero |
| `mov_tierra_acceso_tunel.xlsx` | `1nctJgdtyWoxnLuso5WhJVgukGvhqAUFP3V8rrmeZhyM` | Google Sheet | Volúmenes de explanación acceso al portal |
| `banquetas_portal_b.xlsx` | `10fUz5_YLZAZigvxO4yOw__AbbD2zvrc-RbSml9Bn-Xc` | Google Sheet | Geometría de cortes transversales Portal B |

---

## 3. Síntesis de Parámetros Clave Integrados

### 3.1. Coordenadas Geodésicas y Cotas UTM (WGS84 Zona 18L)
De acuerdo con `coordenadas_utm_tunel.xlsx`, se verificaron y ajustaron las cotas sobre el nivel del mar:
- **Entrada Túnel (PE):** Este: 214,435.96 m E · Norte: 8,942,843.19 m N · Cota: 3,900.00 msnm.
- **Salida Túnel (PS):** Este: 209,031.05 m E · Norte: 8,942,758.86 m N · Cota: 3,786.00 msnm.
- **Campamento Principal (CAM1):** Este: 216,495.92 m E · Norte: 8,942,234.47 m N · Cota: 3,930.00 msnm.
- **Campamento Secundario (CAM2):** Este: 208,309.54 m E · Norte: 8,942,152.25 m N · Cota: 3,810.00 msnm.
- **Botadero 1 (BOT1):** Este: 214,687.13 m E · Norte: 8,942,926.18 m N · Cota: 3,860.00 msnm.
- **Botadero 2 (BOT2):** Este: 208,723.98 m E · Norte: 8,942,164.14 m N · Cota: 3,820.00 msnm.

### 3.2. Geomecánica y Estabilidad de Taludes (Q-Slope)
Conforme a `geomecanica_portal.xlsx` y `angulo_banquetas_qslope.xlsx`:
- **RMR de Bieniawski (Portal):** UCS 80 MPa (7 pts), RQD 70% (13 pts), Espaciamiento 0.30 m (10 pts), Condición de juntas (20 pts), Agua subterránea seca (15 pts). RMR básico = 65. Con ajuste de orientación desfavorable (-5 pts), el RMR de diseño en emboquille es **60** (Clase II / III).
- **Índice Q-slope (Bar & Barton, 2015):**
  $$Q_{slope} = \left(\frac{RQD}{J_n}\right) \times \left(\frac{J_r}{J_a}\right) \times \left(\frac{J_w}{SRF_a}\right) = \left(\frac{50.0}{9.0}\right) \times \left(\frac{1.5}{3.0}\right) \times \left(\frac{0.75}{2.5}\right) = 0.8333$$
- **Ángulo máximo estable de talud sin sostenimiento:**
  $$\beta = 20 \cdot \log_{10}(Q_{slope}) + 65^\circ = 20 \cdot \log_{10}(0.8333) + 65^\circ = 63.42^\circ$$
  Este valor valida el ángulo de corte proyectado de 60° a 65° en las banquetas del portal.

### 3.3. Ciclo de Carguío y Acarreo en Accesos y Portal
Basado en `calculo_carguio_acarreo_tunel.xlsx` y `rendimientos_equipos.xlsx`:
- **Cargador Frontal CAT 966H:** Potencia 260 HP, Cucharón roquero 5.06 m³ (4.00 m³ en banco in-situ), factor de llenado 0.95, tiempo elemental de ciclo en V = 31.56 s (0.526 min). Llenado de camión en 4 pasadas = 2.104 min.
- **Volquete Volvo FMX 8x4 Rígido:** Potencia 500 HP, Capacidad tolva útil 16.0 m³ suelto (32 t), Velocidad cargado 25 km/h, Velocidad vacío 35 km/h, Tiempos fijos (descarga 0.7 min + maniobras 0.4 min = 1.1 min).
- **Producción global en accesos:** Volumen removido 2,455.25 m³ banco (3,191.83 m³ suelto, masa 6,506.41 t), 210 viajes en tolvas de 16 m³, rendimiento horario promedio de **448.73 m³ banco/h**, con un **Match Factor promedio de 1.35**, asegurando una utilización óptima del cargador sin esperas excesivas.

---

## 4. Trazabilidad e Integración en la Cadena Reactiva

Todos los valores han sido centralizados en:
- `datos/parametros.toml`: Secciones `[ubicacion.puntos]`, `[portales.q_slope]`, `[maquinaria.ciclo_carguio_acarreo]`.
- Los módulos de cálculo (`m11_portales.py`, `m06_maquinaria.py`) incorporan estos parámetros a través del contexto global `ctx`.
- El libro de cálculo `11_Portales.xlsx` cuenta con su hoja dinámica `Q_Slope_Taludes` compilada con fórmulas nativas de Excel.
- El repositorio mantiene sincronizada su suite de pruebas unitarias (`test_calculos.py`, `test_documentacion.py`).

Esta metodología garantiza que cualquier variación posterior en los parámetros del TOML recalcule instantáneamente los libros de Excel, memorias técnicas y planos AutoLISP correspondientes.
