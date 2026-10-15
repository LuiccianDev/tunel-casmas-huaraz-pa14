# Power BI Modeling MCP (`powerbi`)

Integración del servidor oficial **Microsoft Power BI Authoring / Modeling MCP Server** (`@microsoft/powerbi-modeling-mcp`) para diseño semántico, medidas DAX y validación de modelos tabulares.

## Contenido del Paquete

- **Servidor MCP (`mcp_config.json`)**:
  - `powerbi`: Provee 21 herramientas multiplexoras (`connection_operations`, `measure_operations`, `table_operations`, `dax_query_operations`, etc.) con aceptación automática de licencia.
- **Reglas (`rules/AGENTS.md`)**:
  - Protocolo de conexión previa e inspección de esquemas antes de redactar medidas DAX.
  - Operaciones transaccionales seguras (`useTransaction: true`).
- **Skills (`skills/`)**:
  - `powerbi-modeling-tools`: Guía exhaustiva de payloads y esquemas para las 21 herramientas del servidor MCP de Power BI.
