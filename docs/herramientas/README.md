# Herramientas e Integraciones del Proyecto PA14

Este directorio centraliza la documentación técnica, guías de arquitectura y protocolos de integración con las herramientas externas y servidores Model Context Protocol (MCP) del proyecto **Túnel Casmas Huaraz PA14**.

---

## 📚 Índice de Herramientas y Documentación

| Herramienta / Servidor | Tipo de Integración | Archivo de Documentación | Subagente Especializado |
| :--- | :--- | :--- | :--- |
| **AutoCAD & Civil 3D AI Gateway** | HTTP Gateway (puerto 5055) + MCP Server (.NET 10 / C#) | [`LuiccianDev/autocad-mcp`](https://github.com/LuiccianDev/autocad-mcp) | `cad-civil3d-pa14` |
| **QGIS Geospatial MCP** | Socket TCP (puerto 9876) + WGS84 UTM 18S (EPSG:32718) | [`documentacion_mcp_qgis.md`](./documentacion_mcp_qgis.md) | `qgis-pa14` |
| **Power BI Modeling MCP** | Servidor oficial Microsoft Power BI Authoring (VertiPaq / DAX) | [`documentacion_mcp_powerbi.md`](./documentacion_mcp_powerbi.md) | `powerbi-pa14` |
| **Graphify Knowledge Graph** | Grafo de conocimiento determinista (`graphify-out/`) | [`guia_graphify.md`](./guia_graphify.md) | `auditor-qa-pa14` |
| **Notion Project Manager** | Workspace "Project Manager Luiccian" (`Projects` / `Tasks`) | Directivas en `.agents/plugins/notion-pm/` | `notion-pm` |

---

## 🩺 Diagnóstico Rápido del Entorno ("Doctor")

Para verificar en cualquier momento el estado de conexión de todos los servidores y variables de entorno, ejecuta:

```powershell
.\scripts\doctor.ps1
```

Este comando comprobará puertos activos, tokens de seguridad, frescura de los estándares XML y dependencias de Python en menos de 2 segundos.
