
<div align="center">


 <h1>Túnel Casmas Huaraz PA14 </h1>

<img src="assets/banner-readme.webp" alt="Túnel Vial Tinco - Banner" width="100%" >



[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)
[![QGIS](https://img.shields.io/badge/QGIS-3.40+-green.svg)](https://qgis.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Academic](https://img.shields.io/badge/Academic-UNT%20Minas-red.svg)](https://www.unitru.edu.pe/)

</div>

Proyecto del curso de **Túneles**: cálculos de ingeniería del túnel y sus
instalaciones, exportados a **Excel** (un libro por entregable), memorias técnicas
en **Markdown** y doble canal de planos para **AutoCAD** (generación batch en **AutoLISP** e interacción en tiempo real vía **AutoCAD AI Gateway** y **MCP Server**).

---

## 1. Entregables de Ingeniería

| # | Excel | Hojas / Contenido | Memoria | Estado |
|---|-------|-------------------|---------|--------|
| **01** | `01_Ubicacion.xlsx` | Coordenadas · Eje del túnel · Distancias | — | ✅ |
| **02** | `02_Geologia.xlsx` | Perfil litológico · RMR · Calidad de roca | — | ⏳ datos estructurados |
| **11** | `11_Portales.xlsx` | Banquetas_Portales (Geometría, taludes, volúmenes in-situ y esponjados) | — | ✅ |
| **03** | `03_Seccion.xlsx` | Geometría · Perforación y avance · Volúmenes | `03_seccion.md` | ✅ |
| **12** | `12_Voladura.xlsx` | Voladura_Konya (Burden, espaciamiento, cargas fondo/columna, retardos) | — | ✅ |
| **04** | `04_Personal.xlsx` | Relación de personal · Turnos · Resumen | `04_personal.md` | ✅ |
| **05** | `05_Campamento.xlsx` | Edificaciones · Áreas requeridas · Resumen | `05_campamento.md` | ✅ |
| **06** | `06_Maquinaria.xlsx` | Frente · Botadero · Campamento · 26 Fichas técnicas individuales · Resumen_Flota | `06_maquinaria.md` | ✅ |
| **07** | `07_Polvorin.xlsx` | Consumo explosivos · Distancias de seguridad · Dimensionamiento | — | ✅ |
| **08** | `08_Agua.xlsx` | Consumo industrial/humano · PETAP · PETAR · Pozos | — | ✅ |
| **09** | `09_Electricidad.xlsx` | Ventilación · Subestaciones y cargas · Grupo electrógeno · Resumen | — | ✅ |
| **10** | `10_Cronograma.xlsx` | Actividades constructivas · Duraciones · Carta Gantt | — | ✅ |
| **13** | `13_Sostenimiento.xlsx` | Sostenimiento (Bieniawski/Barton: pernos, shotcrete, cerchas por tramo) | — | ✅ |
| **—** | `PA14_dibujos.lsp` | Planos AutoLISP: Sección tipo, campamento, polvorines, saneamiento, botadero, malla | — | ✅ |

Cada hoja utiliza el formato estándar: **Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente**.  
Los cálculos se formulan de manera dinámica en Excel (`={Simbolo1}*{Simbolo2}`), garantizando recálculo inmediato sin valores estáticos hardcodeados.

---

## 2. Integración con AutoCAD: Doble Canal

El proyecto cuenta con dos canales independientes y complementarios para generar planos y visualizar geometrías en AutoCAD:

```mermaid
flowchart TD
    A["datos/parametros.toml"] --> B["Pipeline casmas_pa14 (Python)"]
    B --> C["salidas/lisp/PA14_dibujos.lsp (Canal 1: Batch Offline)"]
    C -->|APPLOAD| D["AutoCAD 2027 (Plano Formal)"]
    
    E["Agente de IA (Antigravity / Claude)"] -->|JSON-RPC STDIO| F["AutoCAD MCP Server (.NET 10)"]
    F -->|HTTP REST :5055| G["AutoCAD AI Gateway (.NET 10 / NETLOAD)"]
    G -->|Application.Idle| D
```

### Canal 1: Batch Portable (AutoLISP)
* **Archivo generado:** `salidas/lisp/PA14_dibujos.lsp`.
* **Propósito:** Entregable formal y autónomo para entrega del proyecto. No requiere tener AutoCAD abierto durante la ejecución de Python.
* **Carga en AutoCAD:** Comando `APPLOAD` → seleccionar `PA14_dibujos.lsp`.
* **Comandos disponibles:** `PA14_TODO`, `PA14_SECCION`, `PA14_CAMPAMENTO`, `PA14_POLVORIN`, `PA14_SANEAMIENTO`, `PA14_BOTADERO`, `PA14_MALLA`.
* **Estándar:** Unidades en metros, capas institucionales `PA14-*`, entidades generadas mediante `entmake`.

### Canal 2: Interactivo en Tiempo Real (Gateway + MCP Server en C# / .NET 10)
* **Propósito:** Control directo, dibujo interactivo y telemetría de AutoCAD por parte de asistentes de Inteligencia Artificial (Antigravity, Cursor, Claude Desktop).
* **Puerto oficial:** **`http://localhost:5055/`**.
* **Componentes (`plugins/`):**
  1. **`AutoCAD_AI_Gateway`**: Plugin nativo .NET 10 cargado en AutoCAD con `NETLOAD`. Expone comandos `AI_START_SERVER` y `AI_STOP_SERVER`, gestionando una cola concurrente segura en `Application.Idle` con cancelación preventiva `\x03\x03` y 16 endpoints REST (8 de AutoCAD base y 8 de Civil 3D: superficies, cotas de terreno y alineamientos, con lectura y escritura; el mismo DLL funciona en AutoCAD 2027 y Civil 3D 2027).
  2. **`AutoCAD_MCP_Server`**: Servidor Model Context Protocol v2.2 (STDIO) que expone 20 herramientas de IA (12 de AutoCAD y 8 de Civil 3D) para consultar el modelo (capas, textos, entidades, límites) e inyectar comandos CAD paramétricos o YQArch en metros.

---

## 3. Requisitos del Sistema

* **Cálculos y Python:** [uv](https://docs.astral.sh/uv/) (administra automáticamente Python 3.12 y el entorno virtual `.venv`).
* **CAD Plugins (Opcional, para desarrollo en C#):**
  * SDK de .NET 10.0 (x64).
  * Autodesk AutoCAD 2027 (x64).

---

## 4. Uso Rápido y Automatización

### Configuración inicial del entorno Python:
```powershell
uv sync                 # Crea .venv e instala dependencias
uv run pa14             # Ejecuta los 13 módulos y genera Excel + LISP
```

### Scripts de automatización en `scripts/`:

| Acción | Comando PowerShell (Windows) | Descripción |
|---|---|---|
| **Verificación Total** | `.\scripts\check.ps1` | Ruff format + Ruff check + Pytest + Generación PA14 |
| **Generar Entregables** | `.\scripts\run.ps1` | Ejecuta el pipeline completo de ingeniería |
| **Compilar Plugins CAD** | `.\scripts\build_plugins.ps1` | Compila `AutoCAD_AI_Gateway` y `AutoCAD_MCP_Server` en Release |

---

## 5. Tareas de Desarrollo y Pruebas

| Tarea | Comando |
|---|---|
| Actualizar dependencias | `uv sync` |
| Ejecutar pipeline de ingeniería | `uv run pa14` |
| Formatear código Python | `uv run ruff format .` |
| Linting y correcciones automáticas | `uv run ruff check --fix .` |
| Ejecutar suite de pruebas (incluye guardián documental) | `uv run pytest -q` |
| Compilar solución .NET de AutoCAD | `dotnet build -c Release plugins/AutoCAD_Integration.slnx` |
| Sincronizar grafo de conocimiento (Graphify) | `uvx --from graphifyy graphify update .` |

---

## 6. Estructura del Repositorio

```
├── datos/
│   └── parametros.toml          # ÚNICA fuente de datos de entrada del proyecto
├── src/casmas_pa14/
│   ├── main.py                  # Orquestador del pipeline (MODULOS 01-13)
│   ├── config.py                # Rutas y carga del archivo TOML
│   ├── modelo.py                # Estructuras Libro, Hoja, Tabla
│   ├── excel.py                 # Motor de generación dinámica de Excel
│   ├── lisp.py                  # Generador de planos AutoLISP (.lsp)
│   ├── memoria.py               # Generador de memorias técnicas (.md)
│   └── modulos/                 # 13 módulos de ingeniería (m01 a m13)
├── plugins/
│   ├── AutoCAD_Integration.slnx # Solución unificada de integración CAD (.NET 10)
│   ├── AutoCAD_AI_Gateway/      # Plugin nativo C# para AutoCAD 2027 (puerto 5055)
│   └── AutoCAD_MCP_Server/      # Servidor Model Context Protocol v2.2 STDIO
├── tests/                       # Suite de pruebas unitarias y guardián documental
├── docs/
│   ├── memoria/                 # Memorias técnicas de cálculo en Markdown
│   ├── entradas/                # Documentos de referencia y especificaciones
│   └── PLANIFICACION.md         # Seguimiento de avance del proyecto
├── salidas/                     # Entregables generados (ignorado por git)
│   ├── excel/                   # Libros de cálculo .xlsx
│   ├── lisp/                    # Archivo PA14_dibujos.lsp
│   └── documentos/              # Reportes y salidas documentales
├── scripts/                     # Scripts de automatización (check, run, build_plugins)
├── AGENTS.md                    # Reglas obligatorias para asistentes de IA
└── pyproject.toml               # Configuración del proyecto, dependencias y herramientas
```

---

## 7. Normas de Referencia

* **DS 024-2016-EM**: Reglamento de Seguridad y Salud Ocupacional en Minería (ventilación, refugios, polvorines, distancias).
* **Reglamento Nacional de Edificaciones (RNE)**: Normas OS.100, IS.010, IS.020 (saneamiento, agua potable y alcantarillado).
* **Reglamento SUCAMEC**: Normativa técnica para almacenamiento de explosivos y polvorines auxiliares.
* **Geomecánica de Túneles**: Criterios de Hoek-Brown, Bieniawski (RMR) y Barton (Q) para sostenimiento; formulación de C. Konya para voladura.
