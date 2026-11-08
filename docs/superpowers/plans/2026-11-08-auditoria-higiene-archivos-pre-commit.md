# Plan de Auditoría e Higiene de Archivos Pre-Commit

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auditar rigurosamente el estado del repositorio para identificar, clasificar y depurar archivos innecesarios, temporales o excesivamente pesados antes de realizar el commit y push final a Git, garantizando que solo código productivo, documentación esencial y tests permanezcan versionados.

**Architecture:** Clasificación en 4 categorías (Pesados/Binarios, Temporales/Huérfanos, Restauración de Agentes, y Código/Documentación Legítima), verificación de reglas en `.gitignore`, ejecución del arnés de pruebas (`pytest`) y `check.ps1` previo al empaquetado de commits atómicos.

**Tech Stack:** Git, PowerShell, Python 3.12 (`uv`), pytest, Ruff.

**Spec:** Requerimiento del usuario de verificar qué archivos NO deben subirse antes de commitear y push.

## Global Constraints
- Python y herramientas se ejecutan estrictamente dentro del entorno virtual con `uv run`.
- NUNCA commitear archivos binarios pesados (`.pdf`, `.xlsx`, `.dll`, `.exe`).
- Preservar la integridad de los subagentes en `.agents/plugins/` (no permitir su borrado accidental).
- No romper ninguna de las 40 pruebas unitarias existentes (`pytest -q` debe mantenerse al 100%).

## Review Focus
1. **Archivos pesados (> 500 KB):** Confirmar que ningún binario ni PDF esté staged para commit.
2. **Archivos temporales o de cache:** Asegurar que `__pycache__`, `.pytest_cache`, `.ruff_cache` y archivos temporales estén estrictamente ignorados.
3. **Agentes borrados por error:** Restaurar los subagentes en `.agents/plugins/` que fueron eliminados localmente del working tree.
4. **Archivos experimentales vs productivos:** Clasificar `scripts/pruebas/` y `tests/test_pruebas_natm.py`.
5. **Reorganización de documentación:** Asegurar que el traslado a `docs/herramientas/` no deje enlaces rotos.

---

### Task 1: Clasificación y Auditoría de Archivos Pesados y Temporales

**Files:**
- Modify: `.gitignore`
- Check: `docs/entradas/*.pdf`, `graphify-out/`, `salidas/`

- [ ] **Step 1:** Verificar que los archivos PDF grandes (`manual_de_carreteras_dg_2018.pdf` de 9.66 MB y `modelo_konya_eficientes.pdf` de 1.16 MB) permanezcan ignorados por Git y no aparezcan en `git status`.
- [ ] **Step 2:** Verificar que las carpetas de salida (`salidas/`) y herramientas (`graphify-out/`, `.superpowers/`, `.venv/`) estén blindadas en `.gitignore`.
- [ ] **Step 3:** Comprobar si existen archivos temporales (`*.tmp`, `~$*.xlsx`, etc.) en el espacio de trabajo y eliminarlos si los hubiere.

---

### Task 2: Restauración de Subagentes del Sistema

**Files:**
- Restore: `.agents/plugins/asistente-pa14/agents/calculista.md`
- Restore: `.agents/plugins/asistente-pa14/agents/geologo.md`
- Restore: `.agents/plugins/autocad-gateway/agents/cad_civil3d.md`
- Restore: `.agents/plugins/autocad-gateway/skills/clean-code/SKILL.md`
- Restore: `.agents/plugins/code-reviewer/agents/auditor_qa.md`
- Restore: `.agents/plugins/powerbi/agents/powerbi.md`
- Restore: `.agents/plugins/qgis/agents/qgis.md`

- [ ] **Step 1:** Ejecutar `git restore .agents/plugins/` para recuperar los 7 archivos de subagentes y directivas que fueron eliminados inadvertidamente en el working tree local.
- [ ] **Step 2:** Verificar con `git status` que la sección `.agents/plugins/` esté limpia y sin eliminaciones pendientes.

---

### Task 3: Verificación y Agrupación de Código y Documentación Legítima

**Files:**
- Inspect: `src/casmas_pa14/modulos/portales/`
- Inspect: `docs/herramientas/`
- Inspect: `docs/memoria/16_...` a `21_...`
- Inspect: `scripts/doctor.ps1`, `scripts/utils/extraer_drive_unidad2.py`
- Inspect: `scripts/pruebas/` y `tests/test_pruebas_natm.py`

- [ ] **Step 1:** Revisar el paquete modular `src/casmas_pa14/modulos/portales/` y verificar que cumple con Clean Code y SRP.
- [ ] **Step 2:** Confirmar la validez de las 6 memorias técnicas nuevas (`16` a `21`) en `docs/memoria/`.
- [ ] **Step 3:** Confirmar la reorganización limpia de manuales MCP desde `docs/*.md` hacia `docs/herramientas/*.md`.
- [ ] **Step 4:** Evaluar si `scripts/pruebas/` y `tests/test_pruebas_natm.py` se mantienen como batería de pruebas NATM o si deben ignorarse.

---

### Task 4: Verificación Integral de Calidad y Suite de Pruebas

**Files:**
- Run: `uv run ruff check src/ tests/ scripts/`
- Run: `uv run pytest -q`
- Run: `.\scripts\check.ps1 -Fast`

- [ ] **Step 1:** Ejecutar formateo y linter de Ruff para garantizar cero advertencias de estilo o imports innecesarios.
- [ ] **Step 2:** Ejecutar la suite completa de 40 pruebas en `pytest` para confirmar 100% de aprobación.
- [ ] **Step 3:** Ejecutar el ciclo de verificación rápida de PA14 (`check.ps1 -Fast`).

---

### Task 5: Estrategia de Commits Atómicos y Limpios

**Files:**
- Commit 1: `fix(agents): restore multi-agent configuration and skill definitions`
- Commit 2: `docs(tools): reorganize MCP server guides into docs/herramientas`
- Commit 3: `feat(portales): modularize banquetas, civil3d cuts and drainage calculations`
- Commit 4: `docs(memoria): add technical calculation memories 16 to 21`
- Commit 5: `test(natm): add experimental NATM convergence and split-bench test harness`

- [ ] **Step 1:** Preparar los commits atómicos por responsabilidad para evitar un megacommit desordenado.
- [ ] **Step 2:** Confirmar que `git status` quede completamente limpio.
- [ ] **Step 3:** Solicitar confirmación final al usuario antes de ejecutar `git push origin master`.
