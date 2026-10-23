# Asistencia de Calidad PA14

Al trabajar en el proyecto **Túnel Casmas Huaraz PA14**, debes asegurar estrictamente los siguientes principios para mantener la calidad y consistencia del trabajo:

## 1. Fuente de Verdad Centralizada y Reactividad en Cadena
- Antes de iniciar o confirmar un cálculo, revisa que las variables de entrada estén documentadas en `datos/parametros.toml`.
- Todo valor nuevo o supuesto debe marcarse con `(S)` o referenciar su fuente (Norma Peruana, RNE, etc.).
- **Prohibido** poner números hardcodeados (estáticos) directamente en el código Python. Todo debe ser dinámico y venir del contexto `ctx` y el TOML.
- **Propagación Integral (Efecto Dominó):** Cualquier cambio en un parámetro de entrada debe repercutir en todos los módulos dependientes aguas abajo. Ningún módulo puede retener valores huérfanos ni desacoplados del TOML. Tras cualquier cambio, se deben regenerar todos los libros Excel, memorias y planos AutoLISP en bloque.

## 2. Validación de Código y Testeo
- Una vez finalizada una modificación en `src/`, recuerda siempre que el último paso es ejecutar `.\scripts\check.ps1` (o alternativamente `uv run ruff format . ; uv run ruff check --fix . ; uv run pytest -q ; uv run pa14`).
- Mantén el formato estándar de `ruff` y asegúrate de que el código sigue las reglas establecidas de Python.

## 3. Integridad del Reporte Excel
- Los libros de Excel generados (`NN_Nombre.xlsx`) NO deben contener valores ya calculados de forma estática en Python.
- Los cálculos deben transcribirse en las celdas como fórmulas nativas referenciando símbolos de los parámetros (por ejemplo, `={Q}*{E}/({T}*{Fv})`). El motor de `excel.py` los compilará.
- **Tipografía y Estilo Visual**:
  - Tamaño de fuente estricto e idéntico (`11 pt`) en todo el libro (títulos, encabezados, datos y totales).
  - Encabezados de columnas con relleno verde institucional (`#2E7D32`), texto en **blanco (`#FFFFFF`) y negrita**.
  - Filas de total con relleno verde muy suave (`#E8F5E9`) y negrita.

## 4. Actualización de Conocimiento (Graphify)
- Cuando se añada o modifique la estructura principal en `src/casmas_pa14/modulos/`, ejecuta (o recuérdale al usuario ejecutar):
  ```powershell
  uvx --from graphifyy graphify update .
  ```
  Esto es vital para mantener determinista el grafo de conocimiento del proyecto.

> Estas reglas complementan las normativas generales del proyecto para garantizar un trabajo impecable y adecuado.


## 5. Organización de Documentación (Entradas vs Salidas)
- **Cero desorden documental:** Si recibes contexto normativo o manuales del usuario, guárdalos en `docs/entradas/`.
- Si generas una salida en formato texto/documento como entregable, DEBES guardarla en `salidas/documentos/`.
- Todos los nombres de archivo de documentación deben mantener la convención `snake_case`.

## 6. Documentación Viva y Sincronización de READMEs (Living Documentation)
- **Sincronización en Cascada Obligatoria:** Toda adición o modificación en `src/casmas_pa14/modulos/` (`main.MODULOS`) o en los servicios de CAD en `plugins/` exige actualizar de inmediato:
  1. `README.md` (raíz): tabla de entregables, memorias asociadas, doble canal CAD y scripts.
  2. `plugins/AutoCAD_AI_Gateway/README.md`: endpoints REST, puerto 5055 y arquitectura C#.
  3. `plugins/AutoCAD_MCP_Server/README.md`: catálogo de herramientas MCP y configuración JSON.
  4. `civil3d/README.md` y `civil3d/guia_uso_dg2018.md`: trazabilidad del estándar vial DG-2018.
- **Guardián de Integridad:** El test automatizado `tests/test_documentacion.py` validará en cada ejecución de `.\scripts\check.ps1` (o `.\scripts\check.ps1 -Fast`) que el código y la documentación permanezcan 100% alineados.

## 7. Control de Tokens y Consulta Instantánea (MarkItDown + Índice de Líneas)
- **Prohibido leer PDFs directamente:** Todos los archivos `.pdf` en `docs/entradas/` cuentan con su versión limpia en Markdown (`.md`) generada con `MarkItDown`. Si se añade un nuevo PDF a `docs/entradas/`, ejecuta primero:
  ```powershell
  uv run --with "markitdown[pdf]" python scripts/utils/convertir_pdfs.py
  ```
- **Consulta por Rangos Exactos:** Antes de consultar el manual DG-2018 (`docs/entradas/manual_de_carreteras_dg_2018.md`) o los textos del modelo de Konya, **DEBES** leer primero [`docs/entradas/indice_dg2018.md`](../../../../docs/entradas/indice_dg2018.md) y abrir únicamente el rango `StartLine`–`EndLine` requerido (~50 líneas).

## 8. Estándares de Diseño Vial Civil 3D (DG-2018 MTC)
- La única fuente de verdad para los criterios de Civil 3D es `civil3d/dg2018_datos.toml`, compilada hacia `civil3d/PA14_DG2018_MTC_Roadway_Design_Standards.xml` mediante `uv run python civil3d/generar_dg2018.py`.
- En **Offset Alignments**, instruir siempre al usuario a seleccionar los métodos automáticos `DG-2018 MTC Tabla Sobreancho: ...` con `Apply Widening To = Inside Only` (borde interior de la curva).

