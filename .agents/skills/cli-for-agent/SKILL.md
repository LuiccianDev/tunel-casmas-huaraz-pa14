---
name: cli-for-agent
description: Design, audit, and maintain agent-friendly CLI entrypoints and verification scripts (such as uv run pa14 and scripts/check.ps1) with deterministic exit codes, clear progress output, and fast execution modes.
---

# CLI for Agent

Guidelines for maintaining and extending the project's CLI entrypoints (`uv run pa14`, `uv run python diseno_vial/generar_dg2018.py`, `.\scripts\check.ps1`):

1. **Deterministic Non-Interactive Execution**
   - CLI commands must never block on interactive prompts during batch runs (`uv run pa14` regenerates all 15 Excel workbooks, 15 Markdown memories, and AutoLISP files deterministically).
2. **Fast vs. Full Verification Modes**
   - `.\scripts\check.ps1 -Fast` runs Ruff format/check, `generar_dg2018.py`, and `pytest -q` for rapid iteration.
   - `.\scripts\check.ps1` runs the full pipeline including `uv run pa14` to verify end-to-end deliverable generation.
3. **Actionable Error Messages**
   - Validation errors in `parametros.py` and `excel.py` must name the exact TOML key, module `CLAVE`, sheet name, and symbol that failed.

