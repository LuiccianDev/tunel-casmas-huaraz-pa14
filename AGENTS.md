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
  # O simplemente ejecutar el script de verificación rápida:
  .\scripts\check.ps1
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

### Reactividad en Cadena y Propagación Integral de Cambios (Efecto Dominó)

- **Cero Datos Aislados:** Todo cambio o ajuste en un parámetro de diseño (geométrico, geológico, operativo, de maquinaria o normativo) debe nacer obligatoriamente en `datos/parametros.toml`.
- **Propagación en Cascada (ctx):** El cambio debe repercutir de forma integral en toda la cadena de dependencias (Geometría → Voladura/Sostenimiento → Maquinaria/Campamento → Servicios → Cronograma). Queda **estrictamente prohibido** que un módulo retenga valores estáticos o copias huérfanas desalineadas del TOML.
- **Fórmulas Dinámicas en Excel:** Las celdas calculadas en los libros de Excel (`NN_Nombre.xlsx`) deben generarse siempre mediante fórmulas nativas referenciadas (`={Simbolo1}*{Simbolo2}`) para que cualquier modificación manual posterior en Excel recalcule automáticamente todas las hojas vinculadas en tiempo real.
- **Regeneración Total Obligatoria:** Toda modificación de parámetros o módulos exige ejecutar inmediatamente `.\scripts\check.ps1` para sincronizar y validar en bloque:
  1. Todos los libros de cálculo (`salidas/excel/*.xlsx`).
  2. Todas las memorias técnicas (`docs/memoria/*.md`).
  3. Los planos y geometrías en AutoLISP (`salidas/lisp/PA14_dibujos.lsp`).
  4. La suite completa de pruebas unitarias (`pytest -q`).

## Navegación de Arquitectura (Graphify)

- **Prioridad Estricta:** Este proyecto utiliza **Graphify** (`graphify-out/`). Para entender la arquitectura o buscar cómo se conectan los módulos, el asistente **DEBE** usar primero las herramientas del servidor MCP (`query_graph`, `get_node`, `shortest_path`).
- Las búsquedas manuales ciegas (como `grep_search` o explorar archivos uno por uno) solo se permiten como último recurso.
- *Nota:* Las reglas completas y comandos específicos están encapsulados en el plugin local (`.agents/plugins/graphify/rules/AGENTS.md`).

## Excel (criterio del usuario)

- Simple, tajante y directo: pocos cálculos, los necesarios.
- Un libro por entregable (`NN_Nombre.xlsx`) y hojas con nombres claros.
- Formato estándar: `Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente`
  (`tabla_parametros`). La columna Fórmula muestra la expresión o el libro de origen.
- **Sin repeticiones**: si un valor viene de otro libro, se cita (p. ej. "03_Seccion").
- **Dinamismo obligatorio (sin hardcoding)**: Los valores calculados en las hojas de
  Excel NUNCA deben ser números estáticos o hardcodeados. Deben escribirse como fórmulas
  nativas de Excel referenciando a los símbolos de los parámetros (p. ej.
  `={Q}*{E}/({T}*{Fv})`). El motor central en `excel.py` resuelve automáticamente los
  símbolos entre llaves `{Simbolo}` a sus coordenadas de celda reales (p. ej. `C15`),
  garantizando que el usuario pueda alterar cualquier dato en Excel y ver el recálculo
  inmediato.
- **Tipografía y Colores Uniformes**:
  - **Tamaño de fuente estricto e invariable (11 pt)**: Todos los textos (título del proyecto, títulos de hojas, nombres de tablas, encabezados, celdas de datos y totales) deben mantener el mismo tamaño (`11 pt`). No usar jerarquías con fuentes más grandes para títulos.
  - **Encabezados de columnas y secciones**: Fondo verde técnico sobrio institucional (`#2E7D32`) con texto en color **blanco (`#FFFFFF`) y negrita**.
  - **Totales y resúmenes**: Fondo verde suave (`#E8F5E9`) con texto en negrita y bordes finos estándar.

## Generación de Planos AutoLISP (.lsp) — Canal Archivo Batch

- Generado exclusivamente por `lisp.py` → `salidas/lisp/PA14_dibujos.lsp`. No editar el `.lsp` a mano.
- **Propósito:** Entregable formal, reproducible y portable del proyecto (se carga en AutoCAD vía `APPLOAD`). No requiere tener AutoCAD abierto durante su generación con `uv run pa14`.
- **Reglas de dibujo:** Usar `entmake` (independiente de OSNAP); unidades en metros; capas con prefijo `PA14-`; texto en ASCII (sin tildes).
- Cada plano nuevo: función `dibujo_xxx(ctx) -> Dibujo` y añadirla en `generar_lisp`.

## AutoCAD Gateway y MCP — Canal Interactivo en Vivo

- **Propósito:** Ejecución directa en tiempo real sobre la ventana activa de AutoCAD del usuario (inspección de capas, dibujo inmediato en pantalla, navegación con zoom).
- **Transporte Seguro:** Comunicación vía MCP o POST a `http://localhost:5055/execute` con prefijo `_.-` (comandos en modo texto no modales) y terminadores de línea adecuados.
- **Criterio de Modo (Nativo vs YQArch):**
  - **Modo Nativo (Predeterminado para Túneles e Infraestructura):**
    - Se utiliza para la geometría del túnel, pernos de anclaje, soporte, emboquille, perfiles geológicos y mallas de perforación usando entidades nativas de CAD (`_.-PLINE`, `_.-ARC`, etc.) y capas `PA14-*`.
    - Es obligatorio cuando el usuario indique explícitamente *"sin YQArch"* o *"CAD nativo"*.
  - **Modo YQArch (Fast Drafting para Edificaciones en Superficie):**
    - Exclusivo para diseño rápido de campamento, talleres, casetas de control y oficinas cuando el usuario lo solicite expresamente o se trate de un plano arquitectónico.
    - Sigue el flujo secuencial estricto: Ejes (`ZXW`/`AX`) → Muros (`WW`) → Aberturas (`AD`/`WD`) → Cotas (`AZH`/`DD`).
- **Estándar Métrico Estricto (Unidades en Metros):**
  - Todo dibujo (en AutoLISP o Gateway interactivo) se realiza **estrictamente en metros**: `INSUNITS = 4`, `MEASUREMENT = 1`, `LUNITS = 2`, `LUPREC = 3`.
  - Queda prohibido trabajar en milímetros o pulgadas.
- **Calibración de Anotaciones (Cotas y Textos Proporcionales):**
  - En entorno métrico, los textos de cota deben medir entre `0.20 m` y `0.25 m` (`DIMTXT = 0.22`, `DIMASZ = 0.18`, `DIMEXE = 0.11`, `DIMEXO = 0.06`, `DIMDEC = 2`) para evitar textos gigantes o microscópicos.
  - La IA debe invocar la herramienta MCP `configurar_entorno_dibujo` antes de comenzar a dibujar interactivamente en un archivo nuevo o no configurado.
- **Configuración de YQArch (Idioma y Unidades):**
  - Si se utiliza YQArch, su idioma de interfaz debe configurarse a **inglés** (`YQLANG` opción inglés / `0`) y sus unidades a metros (`YQUNITS` / escala `SD` a 1:100 o 1:50) para evitar textos o menús en chino y descalibraciones de escala.
- **Verificación Visual:** Toda inyección interactiva en tiempo real debe finalizar ejecutando `_.ZOOM E` para centrar y mostrar el dibujo en pantalla.

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


## Documentación (Entradas y Salidas) y Ahorro de Tokens

- **Entradas (Contexto/Base):** Todo documento de referencia aportado por el usuario (fichas técnicas, marco regulatorio, normativas) debe alojarse en `docs/entradas/`.
- **Prohibido leer PDFs directamente:** Todo `.pdf` en `docs/entradas/` cuenta con su par `.md` convertido con `MarkItDown` (sincronizable vía `uv run --with "markitdown[pdf]" python scripts/convertir_pdfs.py`).
- **Índice de Coordenadas:** Antes de consultar el manual DG-2018 (`docs/entradas/manual_de_carreteras_dg_2018.md`) o los documentos de Konya, el asistente **DEBE** consultar [`docs/entradas/indice_dg2018.md`](docs/entradas/indice_dg2018.md) y leer únicamente el rango de líneas (`StartLine`–`EndLine`) requerido.
- **Salidas (Generados):** Todo documento de texto o markdown generado como producto o entregable del proyecto (como prompts generados o reportes) debe guardarse en `salidas/documentos/`.
- **Nomenclatura:** Todos los archivos documentales deben estar en minúsculas y usar `snake_case`.


## Revisión de Código y Arquitectura (Graphify-First)

- **Cero Búsquedas a Ciegas:** Está PROHIBIDO hacer búsquedas de texto masivas o iterativas para entender la estructura. Debes usar obligatoriamente las herramientas del MCP de Graphify para ver las dependencias, "God Nodes" y rutas cortas.
- **Creación de Grafo:** Si la base de datos o carpeta del grafo no existe al momento de iniciar la revisión, tu primer paso técnico DEBE ser ejecutar `uvx --from graphifyy graphify update .` para inicializar el mapa arquitectónico.
- **Mantenimiento Estricto:** Cualquier refactorización debe aplicar modularidad (SRP) y, al finalizar, siempre se debe resincronizar el grafo.

## Documentación Viva y Sincronización de READMEs (Living Documentation)

- **Sincronización Obligatoria en Cascada:** Queda estrictamente prohibido agregar, modificar o renombrar módulos en `src/casmas_pa14/modulos/` (`main.MODULOS`), parámetros de diseño o servicios en `plugins/` sin actualizar simultáneamente los archivos `README.md` correspondientes:
  1. `README.md` (raíz): Tabla completa de entregables (módulos, hojas, memorias asociadas), directivas del doble canal de AutoCAD y scripts.
  2. `plugins/AutoCAD_AI_Gateway/README.md`: Endpoints REST, puerto 5055, directivas métricas y comandos CAD.
  3. `plugins/AutoCAD_MCP_Server/README.md`: Catálogo exhaustivo de herramientas MCP v2.2 y ejemplos de configuración de clientes.
  4. `civil3d/README.md` y `civil3d/guia_uso_dg2018.md`: Trazabilidad y guía del estándar vial DG-2018.
- **Guardián Automatizado:** Toda modificación es validada por la suite de pruebas (`tests/test_documentacion.py`), garantizando que cualquier desalineación entre el código y los READMEs sea bloqueada de inmediato en `.\scripts\check.ps1` (o `.\scripts\check.ps1 -Fast`).

