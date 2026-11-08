---
name: thermo-nuclear-code-quality-review
description: Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, or especially harsh maintainability review.
---

# Thermo-Nuclear Code Quality Review

Review the codebase with an uncompromising maintainability bar. Assume the code will be maintained for years and that every shortcut compounds.

## Core Principles

1. **Code Judo (Simplify Before Adding)**
   - Look for ways to delete special cases by choosing a cleaner data model or table-driven structure in `datos/parametros.toml`.
2. **Strict File & Module Size Ceilings (SRP)**
   - Top-level `src/casmas_pa14/modulos/` must only contain `__init__.py`, `m01_*.py`..`m15_*.py`, and domain subpackages.
   - Complex deliverables must use a clean facade (`< 150` lines) + domain subpackage (`calculo.py`, `hojas.py`, `memoria_doc.py`), with every file `<= 500` lines after `uv run ruff format .`.
3. **Zero Magic Numbers & Zero Stale Strings**
   - Every engineering constant must live in `datos/parametros.toml`.
   - Markdown memories (`memoria_doc.py`) and Excel subtitles (`hojas.py`) must interpolate computed values from `r` rather than hardcoding numbers.
4. **Evidence-Based Findings**
   - Report findings ranked by impact (`Critical`, `Important`, `Minor`) with exact `file:line` references and concrete refactoring steps.

