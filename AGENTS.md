# AGENTS.md — Reglas para asistentes de IA

Proyecto: **Túnel Casmas Huaraz PA14** (curso de Túneles). Idioma: **español**.

## Entorno (obligatorio)

- Python se ejecuta **solo** dentro del entorno virtual de `uv`. Nunca `python`, `pip`
  ni `py` del sistema.
  - ✅ `uv run pa14`, `uv run pytest`, `uv run python -c "..."`
  - ❌ `python main.py`, `pip install ...`
- Dependencias: `uv add <paquete>` (dev: `uv add --dev <paquete>`). No crear `requirements.txt`.
- Antes de dar una tarea por terminada:
  ```powershell
  uv run ruff format . ; uv run ruff check --fix . ; uv run pytest -q ; uv run pa14
  ```

## Arquitectura

- `datos/parametros.toml` es la **única fuente de datos**. No escribir números de diseño
  en el código; agregar el parámetro al TOML con comentario de unidad y fuente.
  Los supuestos se marcan con `(S)`.
- Un módulo por entregable en `src/casmas_pa14/modulos/mNN_nombre.py` con:
  `CLAVE`, `calcular(p, ctx) -> dict`, `libro(r, p) -> Libro`.
- Registrar módulos nuevos en `main.MODULOS` respetando el orden de dependencias.
- Un módulo lee resultados previos desde `ctx[CLAVE]`; **no recalcula** lo que ya
  existe en otro módulo.
- `excel.py` y `lisp.py` no contienen cálculos de ingeniería, solo presentación.

## Excel (criterio del usuario)

- Simple, tajante y directo: pocos cálculos, los necesarios.
- Un libro por entregable (`NN_Nombre.xlsx`) y hojas con nombres claros.
- Formato estándar: `Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente`
  (`tabla_parametros`). La columna Fórmula muestra la expresión o el libro de origen.
- **Sin repeticiones**: si un valor viene de otro libro, se cita (p. ej. "03_Seccion").

## AutoLISP

- Generado por `lisp.py` → `salidas/lisp/PA14_dibujos.lsp`. No editar el `.lsp` a mano.
- Usar `entmake` (no depende de OSNAP); en `command` anteponer `"_non"` a los puntos.
- Texto en ASCII (sin tildes); unidades en metros; capas con prefijo `PA14-`.
- Cada plano nuevo: función `dibujo_xxx(ctx) -> Dibujo` y añadirla en `generar_lisp`.

## Geología

- **No inventar datos geológicos.** El usuario los proporcionará estructurados.
  Ver instrucciones en `modulos/m02_geologia.py`.

## Investigación

- Si se necesita un valor normativo o técnico, citar la fuente (norma peruana: DS 024-2016-EM,
  RNE, SUCAMEC; o bibliografía) en el comentario del TOML y en la columna Fuente.
- Si no se puede confirmar, marcarlo `(S)` y avisar al usuario.

## Estilo de código

- Ruff (config en `pyproject.toml`), línea 88, Python ≥ 3.11.
- Nombres en español, `snake_case`, funciones cortas y con docstring breve.
- Actualizar `docs/PLANIFICACION.md` al completar o agregar tareas.
