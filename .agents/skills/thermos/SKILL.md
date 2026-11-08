---
name: thermos
description: Run a parallel multi-angle audit across architecture, code quality, tests, and performance, then synthesize a prioritized action plan. Use when asked to run thermos, a full codebase health check, or a multi-angle engineering audit.
---

# Thermos — Parallel Multi-Angle Codebase Audit

Perform a comprehensive, zero-compromise engineering audit across four orthogonal axes, then synthesize a deduplicated, severity-ranked action plan.

## Audit Axes

1. **Architecture & Boundaries (`src/casmas_pa14/modulos/` & `datos/parametros.toml`)**
   - Verify single source of truth (`datos/parametros.toml` -> `ctx` reactive chain).
   - Ensure the root of `src/casmas_pa14/modulos/` contains ONLY `__init__.py`, numbered deliverables `m01_*.py`..`m15_*.py`, and clean domain subpackages (`personal/`, `maquinaria/`, `electricidad/`, `portales/`, `voladura/`, `afrontonamiento/`, `banquetas/`).
   - Verify strict separation between calculation (`modulos/`), presentation (`excel.py`, `lisp.py`), and orchestration (`main.py`).

2. **Code Quality & Maintainability (`thermo-nuclear-code-quality-review`)**
   - Enforce the `<= 500` line ceiling across every Python file in `modulos/**` and `< 150` lines for subpackage facades.
   - Hunt down hardcoded magic numbers, stale copy-pasted strings, and duplicated logic.

3. **Tests & Invariants**
   - Confirm every deliverable module (`m01`–`m15`), reactive `ctx` link, Excel cross-sheet formula, and TOML parameter (`test_cero_parametros_huerfanos_en_toml`) is covered by deterministic unit tests.

4. **Performance & Token Efficiency**
   - Ensure Graphify MCP / `graphify-out/` and `docs/entradas/indice_dg2018.md` line ranges are used instead of blind full-file scans.

## Output Format

1. **Executive Verdict** (`PASS` / `NEEDS FIXES`)
2. **Findings by Severity** (`Critical` -> `Important` -> `Minor`), citing `file:line`, root cause, and exact fix.
3. **Verification Gate:** Always conclude with `.\scripts\check.ps1`.

