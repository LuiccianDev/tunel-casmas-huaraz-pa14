# Graphify Knowledge Graph (`graphify`)

Integración local del servidor **Graphify MCP** para análisis determinista de grafos de conocimiento, mapeo de dependencias y navegación de arquitectura en el proyecto Túnel PA14.

## Contenido del Paquete

- **Servidor MCP (`mcp_config.json`)**:
  - `graphify`: Ejecuta `graphify.serve` sobre `graphify-out/graph.json`, exponiendo `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats` y `shortest_path`.
- **Reglas (`rules/AGENTS.md`)**:
  - Prioridad de consulta al grafo antes de realizar búsquedas recursivas de texto.
  - Mantenimiento determinista mediante `uvx --from graphifyy graphify update .`.
- **Skills (`skills/`)**:
  - `graphify`: Flujo completo de generación, consulta y explicación de grafos de conocimiento multimodales.
