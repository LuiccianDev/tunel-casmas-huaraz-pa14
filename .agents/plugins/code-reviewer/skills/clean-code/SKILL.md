---
name: clean-code
description: "Auditoría de Clean Code, principio de responsabilidad única (SRP), eliminación de antipatrones espagueti y refactorización guiada para el proyecto PA14."
---

# Clean Code & Architectural Review Skill

Esta habilidad guía al asistente y a los subagentes en la aplicación de los principios de **Clean Code** (Robert C. Martin), diseño modular y arquitectura limpia en el proyecto **Túnel Casmas Huaraz PA14**.

---

## 1. Principios Rectores en Python (PA14)

1. **Principio de Responsabilidad Única (SRP):**
   * Cada función y módulo debe hacer una sola cosa y hacerla bien.
   * **Límite estricto post-formateo ($\le 500$ líneas):** Ningún archivo `src/casmas_pa14/modulos/m*.py` ni ningún submódulo de paquete (`lisp_cad/`, `voladura/`, `afrontonamiento/`, `banquetas/`) puede superar las 500 líneas **después de ejecutar `uv run ruff format .`**.
   * **Patrón Fachada + Subpaquete:** Cuando un entregable crece, `mNN_nombre.py` (o `lisp.py`) se mantiene como una fachada ligera ($< 150$ líneas) que reexporta el contrato público (`CLAVE`, `calcular`, `libro`, `memoria`) y delega hacia:
     - `calculo.py`: modelos matemáticos puros.
     - `hojas.py` y `catalogos_hojas.py` / `*_hojas.py`: construcción de tablas y fórmulas dinámicas de Excel.
     - `memoria_doc.py`: narrativa técnica en Markdown.
   * **Prevención de Expansión por Ruff:** `ruff format` expande tuplas multilínea de tablas entre un 40% y un 60%. Apunta siempre a $\le 350$ líneas antes de formatear y ejecuta `uv run ruff format .` antes de correr los tests de arquitectura SRP.
2. **Nombres Significativos y en Español:**
   * Usar nombres claros y descriptivos (`velocidad_diseno`, `radio_minimo`, `calcular_peralte`).
   * Evitar abreviaturas crípticas (`d`, `val`, `res1`, `temp`).
3. **Cero Hardcoding (Fuente Única de Verdad):**
   * Ningún número o constante de ingeniería debe nacer en el código Python. Todo debe originarse en `datos/parametros.toml` o `diseno_vial/dg2018_datos.toml`.
4. **Funciones Pequeñas y con Nivel Único de Abstracción:**
   * Mantener las funciones por debajo de 30-40 líneas.
   * No mezclar lógica matemática de alto nivel con manipulación de bajo nivel de cadenas o formato.

---

## 2. Protocolo de Auditoría de Código (Graphify-First)

Al revisar o refactorizar cualquier archivo en `src/`:

```
1. Inspección del Grafo  ──>  2. Auditoría de Antipatrones  ──>  3. Verificación Automatizada
   (query_graph / MCP)        (God Nodes, Acoplamiento)         (Ruff, Pytest, check.ps1)
```

1. **Paso 1 (Contexto de Dependencias):**
   * Consultar las dependencias del módulo mediante Graphify (`query_graph` o `graphify-out/`).
   * Identificar qué módulos aguas abajo consumen sus salidas.
2. **Paso 2 (Detección de Code Smells):**
   * ¿Hay funciones con más de 4 parámetros sin empaquetar en dataclass o dict?
   * ¿Hay lógica de presentación (Excel/LISP) mezclada con cálculo de ingeniería?
   * ¿Hay bloques repetidos o código duplicado?
3. **Paso 3 (Verificación Continua):**
   * Tras cualquier cambio, ejecutar obligatoriamente:
     ```powershell
     uv run ruff check --fix .
     uv run ruff format .
     uv run pytest -q
     .\scripts\check.ps1 -Fast
     ```
