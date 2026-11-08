---
name: continual-learning
description: Capture recurring user corrections, domain invariants, and architectural conventions into AGENTS.md and automated tests so the agent never repeats the same mistake.
---

# Continual Learning

When a review or user correction uncovers a systemic issue, codify the lesson in two places before closing the task:

1. **Automated Guardrail (`tests/`)**
   - Add a fast, deterministic assertion in `tests/test_calculos.py`, `tests/test_auditoria_parametros.py`, or `tests/test_documentacion.py` that would fail immediately if the regression ever reappears.
2. **Concise Rule Update (`AGENTS.md`)**
   - If the correction establishes a new project convention (e.g., folder naming, subpackage structure in `modulos/`, or reactive `ctx` links), document it succinctly in `AGENTS.md`.

