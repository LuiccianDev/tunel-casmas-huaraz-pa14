# Memoria Técnica 18: Revisión Exhaustiva de Cortes, Secciones Transversales y Movimiento de Tierras (Autodesk Civil 3D)

**Proyecto:** Túnel Casmas - Huaraz PA14  
**Asignatura:** Curso de Túneles e Ingeniería Subterránea  
**Fuentes de Civil 3D:** `banquetas_portal_b.xlsx`, `mov_tierra_acceso_tunel.xlsx`, `mov_tierra_acceso_botadero.xlsx`, `mov_tierra_acceso_banquetas.xlsx` y `dimensiones_assembly_accesos.xlsx`  
**Fecha:** Octubre 2026  

---

## 1. Alcance y Resumen Ejecutivo

El presente estudio consolida la **auditoría y revisión exhaustiva de los cortes de terreno, secciones transversales típicas (Assemblies), perfiles y cubicaciones de movimiento de tierras** para la infraestructura exterior del Túnel Casmas - Huaraz PA14 (Portal B / Huaraz).

Se procesaron y conciliaron los reportes estación por estación generados en **Autodesk Civil 3D** a partir de líneas de muestreo (Sample Lines a cada 20 metros), totalizando **979.13 metros lineales de alineamientos viales e industriales** y un volumen neto de excavación en roca de **76,105.14 m³ in-situ**.

---

## 2. Parámetros de Diseño Geométrico de los Assemblies

De acuerdo con [`dimensiones_assembly_accesos.xlsx`](file:///c:/Users/DAVID/Desktop/WorksSpacesCoding/Tunel-Casmas-Huaraz-PA14/docs/entradas/drive_unidad2/dimensiones_assembly_accesos.xlsx), se definen tres plantillas tipo de sección transversal (Assemblies) adaptadas a la orografía escarpada de la Cordillera Negra:

| Parámetro Geométrico | Assembly Acceso Portal B | Assembly Accesos Banquetas 1 y 2 | Assembly Acceso Botadero B | Norma / Sustento |
| :--- | :--- | :--- | :--- | :--- |
| **Ancho de Calzada ($b$)** | **3.60 m** (carril único) | **3.20 m** (acceso técnico) | **3.60 m** (carril minero) | MTC DG-2018 / Manual Accesos |
| **Bermas laterales** | **0.90 m** | Sin berma (acceso banqueo) | **0.50 m** | MTC DG-2018 Tabla 304.02 |
| **Cunetas triangulares** | **1.00 m** (profundidad 0.30 m) | **0.20 m** | **0.20 m** | Drenaje superficial de escorrentía |
| **Talud de corte en roca** | **0.5H : 1V** ($63.43^\circ$) | **0.5H : 1V** ($63.43^\circ$) | **0.5H : 1V** ($63.43^\circ$) | Calibrado con Q-slope ($63.42^\circ$) |
| **Altura de banco ($H_b$)** | **6.00 m** | **6.00 m** | **6.00 m** | Banco de excavación con retroexcavadora |
| **Ancho de banqueta** | **5.00 m** | **5.00 m** | **5.00 m** | Berma de retención de caída de rocas |

> [!NOTE]
> La relación de talud **0.5H:1V ($63.43^\circ$)** adoptada en los Assemblies de Civil 3D concuerda exactamente con el ángulo máximo estable sin sostenimiento calculado mediante el índice **Q-slope de Bar & Barton (2015)** en la Memoria 16 ($\beta = 63.42^\circ$), demostrando total coherencia geomecánica e ingenieril.

---

## 3. Resumen y Cuadratura de Cubicaciones por Alineamiento

A continuación se detalla la cubicación consolidada por eje vial y grupo de líneas de muestreo:

### 3.1. Alineamiento `ACCESO-TUNEL-B` (Acceso Principal al Emboquille)
* **Grupo de Líneas de Muestreo:** `SL-ACCESO-PORTA-B`
* **Estacionamiento:** Progresiva `0+000.000` a `0+200.000` (Longitud: 200.00 m).
* **Cotas de rasante:** 3,795.00 msnm a 3,799.00 msnm.
* **Áreas de corte:** Varían desde 5.57 m² (0+000) hasta 319.20 m² (0+200, aproximación al frontón).
* **Volumen de corte in-situ:** **28,600.00 m³**
* **Volumen de relleno:** **5.20 m³**

### 3.2. Alineamiento `ALINEAMIENTO-BOTADERO-PORTAL-B` (Vía al DME 2)
* **Grupo de Líneas de Muestreo:** `SL-BOTADERO-B`
* **Estacionamiento:** Progresiva `0+000.000` a `0+356.078` (Longitud: 356.08 m).
* **Cotas:** Descenso suave hacia la terraza del Botadero 2 (cota 3,820 msnm).
* **Áreas de corte:** Máximo de 53.20 m² en progresiva 0+140.
* **Volumen de corte in-situ:** **10,500.00 m³**
* **Volumen de relleno:** **13.49 m³**

### 3.3. Alineamiento `ALINEAMIENTO-ACCESO-BANQUETA-1` (Rampa Banqueta Superior)
* **Grupo de Líneas de Muestreo:** `SL-BANQUETA-1`
* **Estacionamiento:** Progresiva `0+000.000` a `0+276.425` (Longitud: 276.43 m).
* **Áreas de corte:** Máximo de 83.23 m² en progresiva 0+200.
* **Volumen de corte in-situ:** **11,000.00 m³**
* **Volumen de relleno:** **6.16 m³**

### 3.4. Alineamiento `ALINEAMIENTO-ACCESO-BANQUETA-2` (Rampa Banqueta Intermedia)
* **Grupo de Líneas de Muestreo:** `SL-BANQUETA-2`
* **Estacionamiento:** Progresiva `0+000.000` a `0+106.621` (Longitud: 106.62 m).
* **Áreas de corte:** Máximo de 21.66 m² en progresiva 0+040.
* **Volumen de corte in-situ:** **1,760.00 m³**
* **Volumen de relleno:** **2.18 m³**

### 3.5. Alineamiento `BANQUETAS-TUNEL` (Corte Masivo del Frontón y Emboquille)
* **Grupo de Líneas de Muestreo:** `SL-BANQUETAS-TUNEL`
* **Estacionamiento:** Progresiva `0+000.000` a `0+039.954` (Longitud: 40.00 m).
* **Áreas de corte transversal:**
  - Estación 0+000: 614.97 m²
  - Estación 0+020: 602.22 m² (Volumen de tramo: 12,171.91 m³)
  - Estación 0+040: 607.91 m² (Volumen de tramo: 12,073.23 m³)
* **Volumen de corte in-situ:** **24,245.14 m³**
* **Volumen de relleno:** **0.00 m³**

---

## 4. Cuadro Consolidado de Balance de Tierras

$$\text{Volumen Total de Excavación} = 28,600 + 10,500 + 11,000 + 1,760 + 24,245.14 = \mathbf{76,105.14\text{ m}^3\text{ in-situ}}$$

Con un factor de esponjamiento medio de $1.25$ para material de roca fracturada y cobertura, el volumen suelto total a transportar y conformar en los botaderos es:

$$V_{\text{suelto}} = 76,105.14 \times 1.25 = \mathbf{95,131.43\text{ m}^3\text{ suelto}}$$

* **Destino del material:**
  - Material apto para subbase y afirmado de accesos: $\sim 1,500\text{ m}^3$.
  - Material excedente evacuado a Botadero 2 (Portal B): $\sim 93,600\text{ m}^3$ sueltos, conformados en terrazas de 10 m con tractor Caterpillar D8T.

---

## 5. Integración en el Pipeline PA14

Los datos y fórmulas de esta memoria se encuentran incorporados de forma reactiva en:
- `datos/parametros.toml` (`[portales.cortes_civil3d]`).
- [`salidas/excel/11_Portales.xlsx`](file:///c:/Users/DAVID/Desktop/WorksSpacesCoding/Tunel-Casmas-Huaraz-PA14/salidas/excel/11_Portales.xlsx), en su hoja `Cortes_Civil3D_Accesos`.
- Módulo `m11_portales.py`.
