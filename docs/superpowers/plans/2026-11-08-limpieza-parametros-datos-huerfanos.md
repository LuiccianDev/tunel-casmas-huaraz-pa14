# Limpieza de Parámetros, Excels de Entrada y Datos Huérfanos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auditar y eliminar 279 parámetros huérfanos en `datos/parametros.toml`, eliminar los 21 archivos Excel binarios no utilizados en `docs/entradas/drive_unidad2/` (~20.8 MB) y depurar el código Python en `src/casmas_pa14/`, garantizando una arquitectura esbelta donde `parametros.toml` sea la única fuente de verdad real, con cero regresiones en cálculos, libros Excel de salida, planos AutoLISP y suite de pruebas.

**Architecture:** Se adopta un enfoque Test-Driven Cleanup (TDC):
1. Arnés de auditoría automatizado (`tests/test_auditoria_parametros.py`) para medir y vigilar claves huérfanas en el TOML.
2. Eliminación de los archivos Excel binarios pesados en `docs/entradas/drive_unidad2/` que no son consumidos por el pipeline de Python, preservando el manifiesto y script de re-descarga.
3. Depuración sistemática por capas en `parametros.toml`: normativas fantasma no integradas, campos sobrantes en portales/maquinaria y tablas desfasadas en campamento/sostenimiento/afrontonamiento.
4. Higiene de código en `src/casmas_pa14/` y verificación en cascada integral con `pytest` y `.\scripts\check.ps1`.

**Tech Stack:** Python 3.12+, `tomllib` (estándar), `pytest`, `ruff`, `openpyxl`, Entorno `uv`.

**Spec:**
- Regla 1 del proyecto PA14: "`datos/parametros.toml` es la **única fuente de datos**. Ningún módulo retiene valores estáticos ni duplicados."
- Consulta del usuario: Eliminación de datos extras innecesarios en `parametros.toml`, código Python y depuración de los Excel de entrada en `docs/entradas/`.

---

## Global Constraints

- **Python en uv únicamente:** Todos los comandos deben ejecutarse con `uv run` (`uv run pytest`, `uv run pa14`, `uv run ruff`).
- **Reactividad en Cadena:** No alterar ninguna clave que sea consumida activamente por las fórmulas de Excel (`{Simbolo}`) o por los cálculos de ingeniería en `ctx`.
- **Preservación del Esquema Activo:** Las 585 claves en uso activo en `src/casmas_pa14/` deben conservarse intactas con sus valores numéricos y unidades.
- **Validación Final Obligatoria:** Toda modificación debe culminar con la ejecución limpia de `.\scripts\check.ps1` (o `uv run ruff check --fix . ; uv run ruff format . ; uv run pytest -q ; uv run pa14`).

---

## Review Focus

1. **Desacoplamiento total de Excels de entrada:** Confirmar que ningún módulo de Python haga `load_workbook` o `read_excel` sobre `docs/entradas/drive_unidad2/`.
2. **Claves de TOML compartidas en fórmulas Excel:** Verificar que ninguna clave eliminada sea referenciada como símbolo en `COLUMNAS_PARAMETRO` o en las fórmulas dinámicas (`={Simbolo}`).
3. **Generación de Planos AutoLISP:** Comprobar que `generar_lisp` y `generar_lisp_campamento` no lean atributos eliminados a través de `ctx`.
4. **Valores por defecto en `.get()`:** Identificar accesos defensivos tipo `p.get("seccion", {}).get(...)` para no romper lógica oculta.
5. **Documentación Viva (READMEs):** Garantizar que `tests/test_documentacion.py` no detecte discrepancias en tablas de entregables tras la limpieza.

---

### Task 1: Arnés de Detección y Auditoría Automática de Parámetros Huérfanos

**Files:**
- Create: `tests/test_auditoria_parametros.py`
- Test: `tests/test_auditoria_parametros.py`

**Interfaces:**
- Consumes: `datos/parametros.toml`, archivos `.py` en `src/casmas_pa14/`
- Produces: Función de auditoría `obtener_parametros_huerfanos(toml_path, src_dir) -> list[str]` y test unitario parametrizado.

- [ ] **Step 1: Escribir el test de detección de parámetros huérfanos**

Crear `tests/test_auditoria_parametros.py` con una función que recorra recursivamente todas las claves hoja de `datos/parametros.toml` y verifique que estén referenciadas en el código fuente de `src/casmas_pa14/`.

```python
import tomllib
from pathlib import Path
import re


def obtener_claves_toml(d: dict, prefijo: str = "") -> list[tuple[str, str]]:
    claves = []
    for k, v in d.items():
        ruta = f"{prefijo}.{k}" if prefijo else k
        if isinstance(v, dict):
            claves.extend(obtener_claves_toml(v, ruta))
        else:
            claves.append((ruta, k))
    return claves


def test_cero_parametros_huerfanos_en_toml():
    toml_path = Path("datos/parametros.toml")
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    py_files = list(Path("src/casmas_pa14").rglob("*.py"))
    py_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore") for p in py_files
    )

    huerfanas = []
    for full_key, leaf_key in obtener_claves_toml(data):
        patron = re.compile(r"['\"]" + re.escape(leaf_key) + r"['\"]")
        if not patron.search(py_text):
            huerfanas.append(full_key)

    assert len(huerfanas) == 0, (
        f"Se detectaron {len(huerfanas)} claves huérfanas en parametros.toml: {huerfanas[:10]}..."
    )
```

- [ ] **Step 2: Ejecutar el test para verificar que falla actualmente**

Run: `uv run pytest tests/test_auditoria_parametros.py -v`
Expected: FAIL indicando 279 claves huérfanas detectadas en `parametros.toml`.

- [ ] **Step 3: Commit del arnés de prueba**

```bash
git add tests/test_auditoria_parametros.py
git commit -m "test: add automated orphan parameters audit test"
```

---

### Task 2: Eliminación de Archivos Excel Innecesarios de Entrada (`docs/entradas/drive_unidad2/`)

**Files:**
- Delete: 21 archivos `.xlsx` en `docs/entradas/drive_unidad2/*.xlsx` (~20.8 MB)
- Retain: `docs/entradas/drive_unidad2/manifest.json`, `scripts/utils/extraer_drive_unidad2.py`
- Test: `tests/test_arnes_fuente_excel.py`, `tests/test_calculos.py`

**Interfaces:**
- Consumes: Ninguna dependencia en Python (verificado: `src/` no contiene llamadas a `load_workbook` ni `read_excel`)
- Produces: Repositorio aliviado en ~20.8 MB de archivos binarios innecesarios.

- [ ] **Step 1: Verificar que ningún archivo de Python lee los Excel de entrada**

Ejecutar comprobación rápida de imports y lecturas de Excel en `src/`:
Run: `uv run python -c "from pathlib import Path; assert not any('load_workbook' in p.read_text('utf-8', 'ignore') for p in Path('src').rglob('*.py'))"`
Expected: PASS (cero dependencias).

- [ ] **Step 2: Eliminar los 21 archivos `.xlsx` en `docs/entradas/drive_unidad2/`**

Remover los archivos `.xlsx` manteniendo intacto `docs/entradas/drive_unidad2/manifest.json` y el script de descarga `scripts/utils/extraer_drive_unidad2.py` por trazabilidad de origen.

- [ ] **Step 3: Ejecutar la suite completa de pruebas para confirmar cero roturas**

Run: `uv run pytest tests/test_calculos.py tests/test_arnes_fuente_excel.py tests/test_arnes_fuente_lisp.py -q`
Expected: 100% PASS (39 pruebas aprobadas, confirmando que los Excels eran 100% prescindibles).

- [ ] **Step 4: Commit**

```bash
git add -u docs/entradas/drive_unidad2/
git commit -m "chore(docs): remove 21 unused input excel files (20.8MB) from drive_unidad2"
```

---

### Task 3: Eliminación de Secciones Normativas Fantasma en `parametros.toml`

**Files:**
- Modify: `datos/parametros.toml` (secciones normativas no consumidas)
- Test: `tests/test_auditoria_parametros.py`, `tests/test_calculos.py`

**Interfaces:**
- Consumes: `datos/parametros.toml`
- Produces: `datos/parametros.toml` depurado sin las 8 secciones normativas no integradas.

- [ ] **Step 1: Remover las 8 secciones normativas sin uso en Python**

Remover en `datos/parametros.toml` los bloques completos de:
1. `[normativa_mtc]` (25 claves)
2. `[normativa_sucamec]` (15 claves)
3. `[normativa_seguridad_subterranea]` (17 claves)
4. `[normativa_hidrocarburos]` (17 claves)
5. `[normativa_recursos_hidricos]` (11 claves)
6. `[normativa_residuos_dme]` (14 claves)
7. `[normativa_efluentes_ptar]` (10 claves)
8. `[normativa_saneamiento_rne]` (20 claves)
*(Total: 129 claves huérfanas eliminadas).*

- [ ] **Step 2: Verificar la reducción de claves huérfanas**

Run: `uv run pytest tests/test_auditoria_parametros.py -v`
Expected: Reducción sustancial del número de claves huérfanas de 279 a 150.

- [ ] **Step 3: Ejecutar suite de cálculos para asegurar cero regresiones**

Run: `uv run pytest tests/test_calculos.py -q`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add datos/parametros.toml
git commit -m "refactor(data): remove 8 unused normative sections from parametros.toml"
```

---

### Task 4: Depuración de Parámetros Huérfanos en Portales y Maquinaria

**Files:**
- Modify: `datos/parametros.toml` (`[portales]`, `[maquinaria]`)
- Test: `tests/test_auditoria_parametros.py`, `tests/test_calculos.py`

**Interfaces:**
- Consumes: `m11_portales.py`, `m06_maquinaria.py`, `rendimientos.py`
- Produces: `[portales]` y `[maquinaria]` en TOML con únicamente los campos leídos por los módulos.

- [ ] **Step 1: Depurar claves en `[portales]`**

Comparar las claves bajo `[portales]` con `src/casmas_pa14/modulos/m11_portales.py` y `m15_voladura_banquetas.py`. Remover las 42 claves correspondientes a sub-especificaciones no utilizadas.

- [ ] **Step 2: Depurar claves en `[maquinaria]`**

Comparar las claves bajo `[maquinaria]` con `src/casmas_pa14/modulos/m06_maquinaria.py` y `src/casmas_pa14/modulos/maquinaria/rendimientos.py`. Remover las 35 claves de tablas muertas (`ciclo_carguio_acarreo`, `accesos`, etc.).

- [ ] **Step 3: Ejecutar pruebas unitarias de maquinaria y portales**

Run: `uv run pytest tests/test_calculos.py -k "maquinaria or portales" -v`
Expected: PASS.

- [ ] **Step 4: Verificar reducción en el test de auditoría**

Run: `uv run pytest tests/test_auditoria_parametros.py -v`
Expected: Huérfanas reducidas en 77 claves adicionales (quedando 73 huérfanas).

- [ ] **Step 5: Commit**

```bash
git add datos/parametros.toml
git commit -m "refactor(data): clean orphan parameters in portales and maquinaria sections"
```

---

### Task 5: Depuración en Campamento, Sostenimiento, Afrontonamiento y Voladura

**Files:**
- Modify: `datos/parametros.toml` (`[campamento]`, `[sostenimiento]`, `[afrontonamiento]`, `[voladura]`, `[voladura_banquetas]`, `[proyecto]`)
- Test: `tests/test_auditoria_parametros.py`, `tests/test_arnes_fuente_excel.py`, `tests/test_arnes_fuente_lisp.py`

**Interfaces:**
- Consumes: Módulos `m05_campamento.py`, `m13_sostenimiento.py`, `m14_afrontonamiento.py`, `m12_voladura.py`, `m15_voladura_banquetas.py`
- Produces: TOML completamente limpio y alineado 1:1 con los módulos de Python.

- [ ] **Step 1: Limpieza en `[campamento]`**

Remover las 29 claves no leídas en `edif01_detalle` y `equipamiento` que no son consumidas por `m05_campamento.py` ni por `lisp_campamento/`.

- [ ] **Step 2: Limpieza en `[sostenimiento]` y `[afrontonamiento]`**

- En `[sostenimiento]`: remover las 6 claves huérfanas (`peso_especifico_roca_t_m3`, `esfuerzo_fluencia_acero_mpa`, `capacidad_adherencia_mpa`, etc.).
- En `[afrontonamiento]`: remover las 26 claves huérfanas no utilizadas en `m14_afrontonamiento.py`.

- [ ] **Step 3: Limpieza en `[voladura]`, `[voladura_banquetas]` y `[proyecto]`**

- Remover las 9 claves huérfanas en `[voladura]`.
- Remover las 2 claves huérfanas en `[voladura_banquetas]`.
- Remover `curso` en `[proyecto]`.

- [ ] **Step 4: Ejecutar el test de auditoría de parámetros**

Run: `uv run pytest tests/test_auditoria_parametros.py -v`
Expected: PASS (0 parámetros huérfanos en `parametros.toml`).

- [ ] **Step 5: Commit**

```bash
git add datos/parametros.toml
git commit -m "refactor(data): eliminate remaining orphan parameters across campamento, sostenimiento and voladura"
```

---

### Task 6: Higiene de Código Python en `src/casmas_pa14`

**Files:**
- Modify: `src/casmas_pa14/modulos/*.py`
- Test: `tests/test_arnes_fuente_excel.py`, `tests/test_arnes_fuente_lisp.py`

**Interfaces:**
- Consumes: Módulos de cálculo en `src/casmas_pa14/modulos/`
- Produces: Código Python limpio, formateado y sin variables no utilizadas.

- [ ] **Step 1: Análisis estático de variables no utilizadas e imports obsoletos**

Run: `uv run ruff check src/ tests/ --select F401,F841`
Expected: All checks passed o correcciones identificadas.

- [ ] **Step 2: Aplicar correcciones automáticas de ruff**

Run: `uv run ruff check --fix src/ tests/ ; uv run ruff format src/ tests/`
Expected: Código formateado y estandarizado.

- [ ] **Step 3: Ejecutar pruebas unitarias completas**

Run: `uv run pytest -q`
Expected: PASS en la suite completa de pruebas unitarias.

- [ ] **Step 4: Commit**

```bash
git add src/ tests/
git commit -m "style(code): clean unused imports, variables and format Python source"
```

---

### Task 7: Verificación en Cascada Integral y Regeneración de Entregables

**Files:**
- Generate/Verify:
  - `salidas/excel/*.xlsx`
  - `salidas/lisp/PA14_dibujos.lsp`
  - `salidas/documentos/prompts_cad.md`
  - `docs/memoria/*.md`
- Test: `tests/test_documentacion.py`, `.\scripts\check.ps1`

**Interfaces:**
- Consumes: Todo el proyecto (`src/casmas_pa14/`, `datos/parametros.toml`)
- Produces: Entregables actualizados y sincronizados sin errores.

- [ ] **Step 1: Regeneración integral del proyecto con el pipeline oficial**

Run: `uv run pa14`
Expected: Salida exitosa de todos los libros Excel, archivos LISP y documentos con resumen final impreso (`L = ... · A = ... · Población = ... · Grupo = ... · Plazo = ...`).

- [ ] **Step 2: Ejecución del script de verificación rápida y guardián de documentación**

Run: `powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1`
Expected:
1. `ruff check` OK.
2. `ruff format` OK.
3. `pytest` OK (100% pruebas aprobadas).
4. `uv run pa14` OK.

- [ ] **Step 3: Actualización del grafo de arquitectura Graphify**

Run: `uvx --from graphifyy graphify update .`
Expected: Grafo de conocimiento en `graphify-out/` sincronizado sin discrepancias.

- [ ] **Step 4: Commit final del ciclo de limpieza**

```bash
git add salidas/ docs/ graphify-out/
git commit -m "chore(release): complete orphan parameters and input excel cleanup"
```

---

## Self-Review Checklist

1. **Spec coverage:** El plan cubre tanto la eliminación de los 21 Excels de entrada como las 279 claves huérfanas en TOML y el código Python.
2. **Step scan:** Cada tarea tiene pasos atómicos claros con comandos ejecutables y resultados esperados concretos.
3. **Type consistency:** No se rompe la firma de `calcular(p, ctx)` ni `libro(r, p)`.
4. **Review Focus:** Aborda el impacto en Excel, AutoLISP, `ctx` y documentación en cascada.
5. **Proportion:** Plan conciso y estructurado de 7 tareas independientes y comprobables.
