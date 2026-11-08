---
name: deslop
description: Remove AI-generated code slop, redundant comments, dead fallbacks, hardcoded magic numbers, and over-engineered wrappers before committing or finishing a task.
---

# Deslop — Clean Up AI Slop Before Completion

Scan all modified files and eliminate patterns typical of unrefined AI-generated code:

1. **Dead Fallbacks & Silent `.get()` Defaults**
   - Remove magic fallback literals in `.get("key", 123.45)` when the parameter belongs in `datos/parametros.toml`.
2. **Stale Hardcoded Numbers in Strings**
   - Replace hardcoded counts or dimensions in table notes and Markdown memories (e.g., `"24 edificaciones"`, `"Ø 45 mm"`) with dynamic interpolations from `r`.
3. **Loose Helper Files & Bloated Modules**
   - Keep `src/casmas_pa14/modulos/` clean: only `__init__.py`, `m01`–`m15`, and domain subpackages (`<= 500` lines per file).
4. **Redundant Comments & Unused Imports**
   - Remove comments that merely restate the next line of code, and run `uv run ruff format . ; uv run ruff check --fix .`.

