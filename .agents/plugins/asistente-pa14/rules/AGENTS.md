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
