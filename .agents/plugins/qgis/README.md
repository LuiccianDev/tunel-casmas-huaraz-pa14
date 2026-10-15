# QGIS Geospatial MCP (`qgis`)

Integración segura de **QGIS Desktop** mediante el servidor **QGIS MCP** para gestión de capas vectoriales/ráster, geoprocesamiento y cartografía en el sistema proyectado **WGS 84 / UTM Zona 18S (EPSG:32718)**.

## Contenido del Paquete

- **Servidor MCP (`mcp_config.json`)**:
  - `qgis`: Conecta con QGIS Desktop en `localhost:9876` autenticado con `QGIS_MCP_TOKEN`.
- **Reglas (`rules/AGENTS.md`)**:
  - Verificación inicial de enlace (`ping`), validación estricta de CRS (`EPSG:32718`) y operaciones geoespaciales no destructivas.
- **Skills (`skills/`)**:
  - `qgis-mcp-tools`: Catálogo y guía de ejecución de las 125 herramientas, recursos (`qgis://`) y flujos transaccionales de QGIS MCP.
