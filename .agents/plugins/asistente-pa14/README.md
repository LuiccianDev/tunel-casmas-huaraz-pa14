# Asistente de Calidad PA14 (`asistente-pa14`)

Plugin principal de ingeniería y aseguramiento de calidad para el proyecto **Túnel Casmas Huaraz PA14**.

## Contenido del Paquete

- **Reglas (`rules/AGENTS.md`)**:
  - Fuente de verdad centralizada en `datos/parametros.toml` y propagación reactiva en cadena (`ctx`).
  - Integridad de libros Excel (`11 pt`, encabezados `#2E7D32`, fórmulas nativas dinámicas `={Simbolo}`).
  - Sincronización obligatoria de documentación viva (`README.md`) y consulta de PDFs mediante `MarkItDown` e `indice_dg2018.md`.
- **Skills (`skills/`)**:
  - `excel-reader`: Inspección rápida de hojas, dimensiones, cabeceras y filas de archivos Excel (`.xlsx`, `.xlsm`) sin saturar la ventana de contexto.
