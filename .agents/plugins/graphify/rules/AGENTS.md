# Reglas para Graphify en el Proyecto Túnel PA14

El proyecto cuenta con un grafo de conocimiento generado en `graphify-out/`.

## Directrices para el Asistente:
1. **Prioridad MCP**: Para consultas sobre la arquitectura de la base de código, dependencias entre módulos o flujo de variables, utiliza primero las herramientas del servidor MCP de Graphify (`query_graph`, `shortest_path`, `get_node`) antes de realizar búsquedas recursivas (`grep_search`).
2. **Navegación**:
   - Si existe `graphify-out/wiki/index.md`, consúltalo para comprender los dominios antes de leer archivos completos.
   - Utiliza `graphify-out/GRAPH_REPORT.md` para auditorías globales de arquitectura y módulos críticos (God Nodes).
3. **Mantenimiento**:
   - Al agregar o modificar módulos de ingeniería en `src/casmas_pa14/modulos/`, ejecuta siempre:
     ```powershell
     uvx --from graphifyy graphify update .
     ```
     para mantener el grafo actualizado de manera determinista y sin consumo de tokens de API.
