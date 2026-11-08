---
name: thermo-nuclear-review
description: Run an exhaustive parallel review of architecture, code quality, test coverage, and runtime/calculation correctness before merging or completing a major milestone.
---

# Thermo-Nuclear Review

Conduct a deep, four-dimensional review of the current branch or workspace changes:

1. **Architecture & Data Flow Review**
   - Trace every input from `datos/parametros.toml` through `calcular(p, ctx)` into `libro(r, p)`, `memoria(r, p)`, and `lisp.py`.
   - Flag any module that reads stale upstream values or bypasses `ctx`.

2. **Code Quality & SRP Review**
   - Verify no file in `src/casmas_pa14/modulos/**` exceeds `500` lines and no facade exceeds `150` lines.
   - Verify no loose helper files sit at the top level of `src/casmas_pa14/modulos/`.

3. **Test & Edge-Case Review**
   - Verify Excel formulas (`={Simbolo}` and `=Sheet!Cell`) reference valid symbols and existing sheet names.
   - Confirm `uv run pytest -q` exercises both nominal and boundary conditions.

4. **Living Documentation Review**
   - Ensure `README.md`, `docs/memoria/*.md`, and `tests/test_documentacion.py` are 100% synchronized with `main.MODULOS`.

