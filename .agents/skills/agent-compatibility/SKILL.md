---
name: agent-compatibility
description: Keep AGENTS.md, .agents/plugins.json, .agents/skills.json, skills, and subagent definitions synchronized across Antigravity, Cursor, and Claude Code harnesses.
---

# Agent Compatibility

Ensure all agent customization files remain valid, discoverable, and synchronized:

1. **Manifest Integrity (`.agents/plugins.json` & `.agents/skills.json`)**
   - Verify every entry points to an existing directory and `SKILL.md` / `plugin.json`.
2. **Rule & Skill Consistency (`AGENTS.md` & `README.md`)**
   - When folders or modules are renamed or modularized (such as `civil3d/` -> `diseno_vial/` or subpackages in `src/casmas_pa14/modulos/`), update all references in `AGENTS.md`, plugin rules, skills, and `README.md`.
3. **Validation**
   - Run `uv run pytest tests/test_documentacion.py -q` to confirm zero broken references.

