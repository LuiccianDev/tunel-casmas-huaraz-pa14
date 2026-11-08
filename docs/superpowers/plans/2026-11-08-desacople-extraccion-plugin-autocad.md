# Plan de Desacople y Extracción del Plugin de AutoCAD

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminar de manera limpia y segura todos los componentes locales de AutoCAD Gateway y AutoCAD MCP Server (.NET/C#) de este repositorio (`Tunel-Casmas-Huaraz-PA14`), actualizando la documentación, configuración de plugins y suite de pruebas para referenciar el nuevo repositorio oficial independiente [`LuiccianDev/autocad-mcp`](https://github.com/LuiccianDev/autocad-mcp).

**Architecture:** Extracción de la carpeta completa `plugins/` (solución .NET), remoción del plugin local de agentes `.agents/plugins/autocad-gateway/` y su registro en `.agents/plugins.json`, eliminación del script `scripts/build_plugins.ps1`, archivo/remoción de la documentación local `docs/herramientas/documentacion_mcp_autocad.md`, actualización de referencias en `README.md` hacia el repositorio externo `LuiccianDev/autocad-mcp`, y refactorización del guardián de pruebas `tests/test_documentacion.py` para mantener 100% de tests pasando en `check.ps1`.

**Tech Stack:** Python 3.12 (`uv`), pytest, Git, PowerShell, Antigravity Plugins Engine.

**Spec:** Deseo del usuario de eliminar el plugin de AutoCAD de este proyecto porque ya fue separado en un repositorio independiente propio: [`LuiccianDev/autocad-mcp`](https://github.com/LuiccianDev/autocad-mcp).

## Global Constraints
- Python se ejecuta estrictamente dentro del entorno virtual con `uv run`.
- Preservar intacto el generador batch de planos AutoLISP del túnel (`src/casmas_pa14/lisp.py` y `salidas/lisp/*.lsp`), ya que es el entregable formal de ingeniería de túneles del curso.
- Cero regresiones en la suite de pruebas: `pytest` y `.\scripts\check.ps1` deben pasar sin errores tras el desacople.
- Actualizar `README.md` para documentar la interoperabilidad con AutoCAD mediante el nuevo repositorio externo `LuiccianDev/autocad-mcp` (Canal Interactivo).

## Review Focus
1. **Verificación de dependencias:** Confirmar que ningún archivo en `src/casmas_pa14/` importe o dependa de `plugins/` o de C#.
2. **Higiene de `.agents/plugins/`:** Actualizar `.agents/plugins.json` y `.agents/skills.json` para retirar `autocad-gateway` sin romper los otros 5 plugins (`asistente-pa14`, `code-reviewer`, `graphify`, `powerbi`, `qgis`).
3. **Refactorización de `tests/test_documentacion.py`:** Ajustar los tests que inspeccionaban los READMEs de `plugins/AutoCAD_*` y el puerto 5055 para que no busquen archivos inexistentes.
4. **Validación de `scripts/check.ps1`:** Confirmar que el ciclo de verificación integral pase limpio en menos de 15 segundos sin buscar `build_plugins.ps1`.
5. **Sincronización de Graphify:** Actualizar el grafo de conocimiento para remover nodos huérfanos de C#.

---

### Task 1: Eliminación de la Solución .NET y Scripts de Compilación de AutoCAD

**Files:**
- Delete directory: `plugins/` (`plugins/AutoCAD_AI_Gateway/`, `plugins/AutoCAD_MCP_Server/`, `plugins/AutoCAD_Integration.slnx`)
- Delete file: `scripts/build_plugins.ps1`
- Delete file: `docs/herramientas/documentacion_mcp_autocad.md`

- [ ] **Step 1:** Verificar que `plugins/` no tenga cambios sin commitear y que todo el código esté resguardado en el repositorio remoto `LuiccianDev/autocad-mcp`.
- [ ] **Step 2:** Eliminar la carpeta `plugins/` del repositorio local.
- [ ] **Step 3:** Eliminar el script `scripts/build_plugins.ps1`.
- [ ] **Step 4:** Eliminar el documento de referencia `docs/herramientas/documentacion_mcp_autocad.md`.
- [ ] **Step 5:** Ejecutar `git status` para verificar la eliminación de estos archivos y registrar un commit preliminar o confirmar el cambio.

---

### Task 2: Remoción del Plugin de Agente Local `autocad-gateway`

**Files:**
- Delete directory: `.agents/plugins/autocad-gateway/`
- Modify: `.agents/plugins.json`

- [ ] **Step 1:** Eliminar la carpeta `.agents/plugins/autocad-gateway/` (que contenía `cad_civil3d.md`, `rules/AGENTS.md` y sus skills de C#/.NET).
- [ ] **Step 2:** Editar `.agents/plugins.json` para retirar la entrada de `autocad-gateway`, dejando activos los 5 plugins oficiales del proyecto (`asistente-pa14`, `code-reviewer`, `graphify`, `powerbi`, `qgis`).
- [ ] **Step 3:** Verificar que `.agents/skills.json` permanezca coherente.

---

### Task 3: Refactorización del Guardián de Documentación (`tests/test_documentacion.py`)

**Files:**
- Modify: `tests/test_documentacion.py`

- [ ] **Step 1:** Eliminar las variables obsoletas `README_GATEWAY`, `README_MCP` y `DOC_MCP` que apuntaban a carpetas en `plugins/`.
- [ ] **Step 2:** Refactorizar o eliminar `test_readmes_usan_puerto_oficial_5055` para que solo audite los archivos vigentes o valide la referencia al puerto 5055 en el README raíz.
- [ ] **Step 3:** Eliminar o adaptar `test_plugins_readmes_documentan_endpoints_y_herramientas` y `test_mcp_configuraciones_y_binarios_alineados`, sustituyéndolos por un test que valide que `README.md` referencia el repositorio oficial `https://github.com/LuiccianDev/autocad-mcp`.
- [ ] **Step 4:** Actualizar `test_estructura_plugins_antigravity` para que la lista de plugins esperados sea:
  ```python
  plugins_esperados = {
      "asistente-pa14",
      "code-reviewer",
      "graphify",
      "powerbi",
      "qgis",
  }
  ```
- [ ] **Step 5:** Ejecutar `uv run pytest tests/test_documentacion.py -q` para verificar que la suite pasa en verde.

---

### Task 4: Actualización de `README.md` y Documentación del Proyecto

**Files:**
- Modify: `README.md`

- [ ] **Step 1:** En la sección "Doble Canal AutoCAD", actualizar el "Canal 2: Interactivo en Vivo (AutoCAD AI Gateway & MCP Server)" para indicar que el servicio es provisto por el componente desacoplado externo [`LuiccianDev/autocad-mcp`](https://github.com/LuiccianDev/autocad-mcp).
- [ ] **Step 2:** Remover la fila de `.\scripts\build_plugins.ps1` de la tabla de scripts útiles en `README.md`.
- [ ] **Step 3:** En Notion (`Projects`), registrar una nota o actualización de que la integración CAD en vivo se conecta mediante el repositorio desacoplado.

---

### Task 5: Verificación Integral, Sincronización de Graphify y Cierre

**Files:**
- Run: `uv run ruff check --fix .`
- Run: `uv run ruff format .`
- Run: `uv run pytest -q`
- Run: `.\scripts\check.ps1 -Fast`
- Run: `uvx --from graphifyy graphify update .`

- [ ] **Step 1:** Ejecutar `ruff format` y `ruff check` sobre todo el proyecto.
- [ ] **Step 2:** Ejecutar la suite completa de pruebas unitarias (`pytest -q`) asegurando que todos los tests pasen.
- [ ] **Step 3:** Ejecutar el ciclo de verificación oficial (`.\scripts\check.ps1 -Fast`).
- [ ] **Step 4:** Actualizar el grafo de Graphify (`uvx --from graphifyy graphify update .`) para depurar los símbolos eliminados de C#.
- [ ] **Step 5:** Confirmar con `git status` y empaquetar los commits atómicos de desacople.
