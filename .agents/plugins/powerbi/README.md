# Power BI Modeling MCP (`powerbi`)

Integración del servidor oficial **Microsoft Power BI Authoring / Modeling MCP Server** (`@microsoft/powerbi-modeling-mcp`) para diseño semántico, medidas DAX y validación de modelos tabulares.

## Contenido del Paquete

- **Subagente Especializado (`agents/powerbi.md`)**:
  - `powerbi-pa14`: Ingeniero especialista en Business Intelligence, modelado semántico tabular VertiPaq, arquitectura en estrella y formulación DAX avanzada (`VAR`/`RETURN`).
- **Servidor MCP (`mcp_config.json`)**:
  - `powerbi`: Provee 21 herramientas multiplexoras (`connection_operations`, `measure_operations`, `table_operations`, `dax_query_operations`, etc.) con aceptación automática de licencia.
- **Hooks de Ciclo de Vida (`hooks.json` & `hook_powerbi_guard.py`)**:
  - `powerbi-integrity-guard`: Garantiza que las modificaciones estructurales viajen en transacciones atómicas (`useTransaction: true`) y valida la consistencia sintáctica previa en fórmulas DAX.
- **Reglas (`rules/AGENTS.md`)**:
  - Protocolo de conexión previa e inspección de esquemas antes de redactar medidas DAX.
  - Operaciones transaccionales seguras (`useTransaction: true`).
- **Skills (`skills/`)**:
  - `powerbi-modeling-tools`: Guía exhaustiva de payloads y esquemas para las 21 herramientas del servidor MCP de Power BI.
