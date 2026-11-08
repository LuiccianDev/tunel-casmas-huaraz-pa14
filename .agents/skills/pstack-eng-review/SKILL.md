---
name: pstack-eng-review
description: Run a pstack engineering plan & architecture review: draw ASCII data-flow and dependency diagrams, build an edge-case and failure-mode matrix, verify reactive chain invariants, and run a post-implementation retrospective. Use when reviewing engineering plans, auditing module chains, or running /pstack.
---

# PStack Engineering Review (`pstack-eng-review`)

Adaptation of the official `pstack` engineering workflow (`plan-eng-review` + `qa` + `retro`) for rigorous engineering software and calculation pipelines.

## 1. Architecture & ASCII Data-Flow Diagram

Before approving or closing an engineering change, map the exact data flow in ASCII:

```text
[datos/parametros.toml]
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ Orquestador: main.MODULOS (Orden topológico de dependencias)      │
│ 01_Ubicacion -> 02_Geologia -> 11_Portales -> 15_Banquetas ->     │
│ 03_Seccion -> 14_Afrontonamiento -> 12_Voladura -> 04_Personal -> │
│ 05_Campamento -> 06_Maquinaria -> 07_Polvorin -> 08_Agua ->       │
│ 09_Electricidad -> 10_Cronograma -> 13_Sostenimiento              │
└───────────────────────────────────────────────────────────────────┘
        │
        ├──► salidas/excel/NN_Nombre.xlsx   (Fórmulas dinámicas ={Simbolo})
        ├──► docs/memoria/NN_Nombre.md      (Valores interpolados desde r)
        └──► salidas/lisp/PA14_dibujos.lsp  (Geometría CAD en metros)
```

## 2. Edge-Case & Invariant Matrix

For every module touched, verify:
- **Upstream `ctx` contract:** Does the module consume the exact key produced upstream (e.g., `ctx["voladura"]["frente_tunel"]["taladros_perforados"]`)?
- **Excel Formula Integrity:** Do all `{Symbol}` placeholders and `=Sheet!Cell` cross-sheet references resolve to existing symbols and sheet names?
- **Zero Orphan Parameters:** Are all TOML keys consumed in `src/` (`test_cero_parametros_huerfanos_en_toml`)?
- **Physical & Normative Bounds:** Do velocities, slopes, RMR/Q-slope ratings, and clearances satisfy MTC DG-2018, D.S. 024-2016-EM, RNE, and SUCAMEC?

## 3. QA & Verification Gate

Run the complete deterministic verification pipeline before shipping:
```powershell
.\scripts\check.ps1
```

