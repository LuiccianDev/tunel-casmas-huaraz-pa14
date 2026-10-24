# Asistente de Calidad PA14 (`asistente-pa14`)

Plugin principal de ingeniería y aseguramiento de calidad para el proyecto **Túnel Casmas Huaraz PA14**.

## Contenido del Paquete

### Subagentes Especializados (`agents/`)
- **`calculista` (`calculista-pa14`)**: Subagente especializado en cálculo geomecánico, sostenimiento, reactividad TOML (`parametros.toml`) → `ctx` y compilación de fórmulas nativas dinámicas en Excel (`NN_Nombre.xlsx`) sin números estáticos.
- **`geologo` (`geologo-pa14`)**: Subagente especializado en caracterización del macizo rocoso (RMR de Bieniawski 1989, Índice Q de Barton 1974/2002, GSI) y estratigrafía regional bajo la regla estricta de *cero invención de datos geológicos*.

### Hooks de Ciclo de Vida (`hooks.json`)
- **`pa14-environment-guard`**:
  - `PreToolUse` (`run_command`): Intercepta y bloquea ejecuciones directas de Python o Pip fuera del entorno `uv run`.
  - `PostToolUse` (`edit_file|write_file`): Supervisa modificaciones en código de cálculo (`src/casmas_pa14/`) o parámetros para recordar la validación con `check.ps1`.

### Reglas (`rules/AGENTS.md`)
- Fuente de verdad centralizada en `datos/parametros.toml` y propagación reactiva en cadena (`ctx`).
- Integridad de libros Excel (`11 pt`, encabezados `#2E7D32`, fórmulas nativas dinámicas `={Simbolo}`).
- Sincronización obligatoria de documentación viva (`README.md`) y consulta de PDFs mediante `MarkItDown` e `indice_dg2018.md`.

### Skills (`skills/`)
- **`auditor-normativo`**: Consulta eficiente de normativa técnica peruana (DG-2018, DS 024-2016-EM, RNE) por rangos exactos de líneas.
- **`calculista-pa14`**: Protocolo de cálculo de ingeniería subterránea y reactividad TOML → ctx → Excel.
- **`excel-reader`**: Inspección rápida de hojas, dimensiones, cabeceras y filas de archivos Excel (`.xlsx`, `.xlsm`) sin saturar la ventana de contexto.
