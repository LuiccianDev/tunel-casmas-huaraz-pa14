# QGIS Geospatial MCP (`qgis`)

Integración segura de **QGIS Desktop** mediante el servidor **QGIS MCP** para gestión de capas vectoriales/ráster, geoprocesamiento y cartografía en el sistema proyectado **WGS 84 / UTM Zona 18S (EPSG:32718)**.

## Contenido del Paquete

- **Subagente Especializado (`agents/qgis.md`)**:
  - `qgis-pa14`: Ingeniero especialista en SIG, modelación territorial, cuencas, perfiles de elevación y edición vectorial transaccional segura.
- **Servidor MCP (`mcp_config.json`)**:
  - `qgis`: Conecta con QGIS Desktop en `localhost:9876` autenticado de forma segura heredando `QGIS_MCP_TOKEN` desde las variables de entorno del sistema (Zero-Secrets en archivos).
- **Hooks de Ciclo de Vida (`hooks.json` & `hook_qgis_guard.py`)**:
  - `qgis-integrity-guard`: Previene cambios no autorizados al CRS proyectado oficial (`EPSG:32718`) y protege las capas base originales de modificaciones destructivas.
- **Reglas (`rules/AGENTS.md`)**:
  - Verificación inicial de enlace (`ping`), validación estricta de CRS (`EPSG:32718`) y operaciones geoespaciales no destructivas.
- **Skills (`skills/`)**:
  - `qgis-mcp-tools`: Catálogo y guía de ejecución de las 125 herramientas, recursos (`qgis://`) y flujos transaccionales de QGIS MCP.
