# Reglas de Revisión de Código y Optimización (Graphify-First)

Al momento de revisar código, refactorizar o analizar la arquitectura del proyecto, el asistente DEBE seguir este workflow obligatorio:

## 1. Prohibición de Búsquedas Ciegas y Uso de MCP
- **NUNCA** utilices herramientas de búsqueda de texto completas de forma iterativa ni leas archivos enteros a ciegas para entender dependencias.
- Utiliza **SIEMPRE** el servidor MCP de Graphify (`graphify_graphify`) para obtener el mapa de dependencias y el estado arquitectónico consumiendo mínimos tokens.

## 2. Fallback de Creación (Generación del Grafo)
- Si al intentar consultar a Graphify detectas que el grafo **no existe** o no se ha inicializado el proyecto en Graphify (falta la carpeta de salida), **el primer paso obligatorio** es ejecutar la creación del grafo:
  ```powershell
  uvx --from graphifyy graphify update .
  ```
- Solo después de crearlo, procede a analizarlo.

## 3. Flujo de Refactorización (Anti-Espagueti)
1. **Auditoría:** Revisa los "God Nodes" y dependencias usando MCP antes de tocar el código.
2. **Modularidad:** Asegura el Principio de Responsabilidad Única. Nada de archivos/funciones todoterreno. Divide lógica vs. presentación.
3. **Mantenimiento:** Tras terminar de agregar o refactorizar archivos, SIEMPRE vuelve a correr `graphify update` para que la memoria no se desincronice.
