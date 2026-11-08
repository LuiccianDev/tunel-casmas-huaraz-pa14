# Memoria Técnica 17: Auditoría Exhaustiva de Discrepancias y Consolidación de Datos Técnicos (Google Drive vs. PA14)

**Proyecto:** Túnel Casmas - Huaraz PA14  
**Asignatura:** Curso de Túneles e Ingeniería Subterránea  
**Fuentes Auditadas:** 21 Libros y Modelos de Google Drive (`UNIDAD 2`) vs. Código Base PA14  
**Fecha:** Octubre 2026  

---

## 1. Justificación y Propósito de la Auditoría

Al contrastar la base de datos de diseño preliminar del proyecto local frente a los 21 archivos y hojas de cálculo detalladas en Google Drive (`docs/entradas/drive_unidad2/`), se identificaron discrepancias técnicas significativas en:
1. La valoración geomecánica del macizo rocoso en el portal (condición de agua subterránea y RMR).
2. La arquitectura de la malla de perforación y voladura del frente subterráneo (malla empírica real de 141 taladros frente a fórmulas teóricas globales de 231 taladros).
3. El esquema de sostenimiento del frontón de emboquille (dimensionamiento comercial de paneles de malla, longitud de anclaje de pernos de cosido y espesor/rebote de shotcrete).
4. El ciclo cinemático de carguío y acarreo de la flota (tiempos de ciclo de CAT 966H y Volvo FMX 8x4).
5. La geometría de accesos industriales y banquetas del portal.

Para garantizar que el proyecto se ejecute de manera correcta y consistente, se adoptaron las cifras y modelos de Google Drive en `datos/parametros.toml`, asegurando que el motor reactivo de Python recalcule en tiempo real todos los libros Excel (`salidas/excel/`), planos AutoLISP (`salidas/lisp/`) y memorias técnicas (`docs/memoria/`).

---

## 2. Matriz de Discrepancias Identificadas y Resueltas

### 2.1. Geomecánica y Clasificación RMR en el Portal
* **Archivo de Referencia:** `geomecanica_portal.xlsx` (Hoja 1).
* **Discrepancia Encontrada:**
  - El código previo consideraba condición de agua "Húmedo" (7 pts) y RQD de 62%, resultando en un RMR básico de 57 y RMR ajustado de 52 (Clase III Regular).
  - El estudio geomecánico de detalle del portal establece:
    - Resistencia UCS: 80 MPa (7 pts).
    - RQD: 70.0% (13 pts).
    - Espaciamiento de juntas: 0.30 m (10 pts).
    - Condición de discontinuidades: 20 pts.
    - Agua subterránea: **Completamente seco** (15 pts).
    - **RMR básico = 65** (Clase II Buena).
    - Con ajuste por orientación desfavorable en talud (-5 pts), el **RMR ajustado de diseño es 60** (límite Clase II / III).
* **Resolución:** Actualizado en `datos/parametros.toml` (`[afrontonamiento]`), reflejando la roca real competente del emboquille.

### 2.2. Malla de Perforación y Voladura Subterránea
* **Archivos de Referencia:** `malla_1_disparo.xlsx` y `malla_2_alivio.xlsx`.
* **Discrepancia Encontrada:**
  - El código local estimaba 231 taladros cargados mediante la fórmula genérica de Langefors-Kihlström con factor de carga de 1.60 kg/m³ (~600 kg de explosivo por disparo).
  - El diseño real de la Unidad 2 optimiza la malla a:
    - **Malla 1 (1 alivio Ø 102 mm):** 140 taladros cargados + 1 alivio = **141 taladros totales**. Consumo explosivo = **362.28 kg/disparo** (1,199.6 cartuchos).
    - **Malla 2 (2 alivios Ø 102 mm):** 140 taladros cargados + 2 alivios = **142 taladros totales**. Consumo explosivo = **511.22 kg/disparo** (1,687.3 cartuchos).
    - Brocas diferenciadas: Alivio Ø 102 mm, Arranque/Ayudas/Arrastre Ø 51 mm, Hastiales/Corona Ø 48 mm.
* **Resolución:** Se incorporó la Malla 1 como configuración activa en `[voladura]`, reduciendo tiempos de perforación del Jumbo DT1131 de 3.5 h a ~2.1 h por disparo y optimizando el consumo de insumos.

### 2.3. Sostenimiento del Frontón de Emboquille
* **Archivo de Referencia:** `diseno_sostenimiento_fronton.xlsx` (`Malla_Electrosoldada`, `Pernos_RockBolt`, `Shotcrete_Robotizado`).
* **Discrepancia Encontrada:**
  - *Malla electrosoldada:* Se asumían paños de 6.0 m × 2.40 m. La ficha técnica de Aceros Arequipa Q-139 en Drive especifica rollos mineros de **25.0 m × 2.42 m** (alambre Ø 3.4 mm, cocada 10x10 cm, área útil 52.36 m²/panel), requiriendo exactamente **12 paneles** para cubrir los 591.57 m² netos.
  - *Pernos de anclaje:* Se calculaban pernos cortos de 3.0 m @ 1.50 m. El diseño de emboquille en Drive utiliza **pernos de cosido profundo de 9.0 m** con malla cuadrada de **4.50 m × 4.50 m**, taladro Ø 32 mm y resina Ø 28 mm.
  - *Shotcrete robotizado:* Se asumía espesor de 12 cm con 10% de rebote. El diseño de emboquille en Drive fija un **espesor de 10 cm (0.10 m)** con **15% de rebote**, agregando aditivo acelerante SikaCem PE (17 kg/m³), nanosílice (4.25 kg/m³) y macrofibra Force-60 (4.0 kg/m³).
* **Resolución:** Parámetros alineados al 100% en `[afrontonamiento]` y propagados a `m14_afrontonamiento.py`.

### 2.4. Flota, Ciclo de Carguío y Acarreo
* **Archivos de Referencia:** `calculo_carguio_acarreo_tunel.xlsx` y `rendimientos_equipos.xlsx`.
* **Discrepancia Encontrada:**
  - El código previo utilizaba tiempos fijos genéricos de 8.0 min y flota 6x4.
  - El estudio detallado de la Unidad 2 demuestra:
    - **Cargador CAT 966H:** Cucharón roquero de 5.06 m³ (4.00 m³ banco), factor de llenado 0.95, tiempo elemental en V de **31.56 s** (0.526 min). Llenado de tolva en **4 pasadas = 2.104 min**.
    - **Volquetes Volvo FMX 8x4 Rígidos:** Tolva útil de 16.0 m³ suelto (32 t), tiempos fijos de descarga (0.7 min) y maniobras (0.4 min) = **1.10 min**.
    - **Match Factor:** Rango balanceado de 1.06 a 1.35 para 4 unidades asignadas.
* **Resolución:** Integrado en `[maquinaria.ciclo_carguio_acarreo]` y en `[maquinaria.accesos]`.

### 2.5. Geometría de Accesos y Banquetas
* **Archivos de Referencia:** `diseno_accesos_banquetas_mov_tierra.xlsx` (`2. Geometría y Volúmenes Vías` y `4. Banquetas del Portal`).
* **Discrepancia Encontrada:**
  - Se modelaba una vía de calzada reducida (3.60 m).
  - El proyecto vial de accesos de la Unidad 2 define una calzada uniforme de **5.00 m**, talud de corte 1:1 y afirmado de 0.20 m para los 4 accesos:
    - Acceso 1 (155 m, 1,018.13 m³ corte).
    - Acceso 2 (112 m, 725.00 m³ corte).
    - Acceso 3 (53 m, 332.13 m³ corte).
    - Acceso a Base/Portal (60 m, 380.00 m³ corte).
    - Total de corte en accesos: **2,455.25 m³ banco**.
  - Banquetas de portal: 3 banquetas de **$35\text{ m} \times 4\text{ m} \times 6\text{ m}$** (420 m³ banco c/u).
* **Resolución:** Incorporado en `[maquinaria.accesos]` y en `[portales.banquetas_diseno_u2]`.

---

## 3. Verificación de la Integración

Tras actualizar `datos/parametros.toml` y los módulos correspondientes:
1. `uv run pa14` ejecutó la regeneración de los 15 libros de cálculo de Excel (`salidas/excel/*.xlsx`), memorias técnicas y planos AutoLISP.
2. `uv run pytest -q` aprobó la suite completa de pruebas unitarias.
3. El proyecto queda blindado contra inconsistencias, garantizando trazabilidad completa con los datos empíricos de Google Drive.
