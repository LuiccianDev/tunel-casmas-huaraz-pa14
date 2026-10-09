---
name: powerbi-modeling-tools
description: Reference and execution guide for Microsoft Power BI Authoring / Modeling MCP Server (21 multiplexer tools). Use when connecting to Power BI models, authoring DAX measures, modifying tables/columns/relationships, managing PBIP/TMDL models, creating calculation groups, or running DAX queries.
---

# Power BI Modeling MCP Tools Reference (21 Multiplexer Tools)

Guía completa del servidor oficial **Power BI Authoring MCP Server** (`@microsoft/powerbi-modeling-mcp` / `microsoft/powerbi-modeling-mcp`). Permite a agentes de IA interactuar con modelos semánticos tabulares en **Power BI Desktop**, proyectos **PBIP / TMDL**, y **Microsoft Fabric**.

---

## 1. Arquitectura de Herramientas Multiplexoras ("Coarse Tools")

El servidor expone **21 herramientas compuestas por dominio**. Todas las llamadas envuelven los parámetros dentro de un objeto `request` con el atributo obligatorio `operation`:

```json
{
  "request": {
    "operation": "Create",
    "definitions": [ ... ]
  }
}
```

---

## 2. Catálogo de las 21 Herramientas Multiplexoras

| Herramienta | Operaciones Soportadas | Propósito Principal |
|---|---|---|
| `connection_operations` | `Help`, `Connect`, `ConnectFabric`, `ConnectFolder`, `ConnectBimFile`, `Disconnect`, `GetConnection`, `ListConnections`, `ListLocalInstances` | Gestión de enlaces a Power BI Desktop, Fabric, TMDL local o `.bim`. |
| `database_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List`, `DeployToFabric`, `ExportTMDL`, `ImportTMDL` | Gestión del modelo semántico / base de datos tabular a nivel global. |
| `model_operations` | `Help`, `Get`, `Update`, `GetStatistics`, `EvaluateBestPractices`, `Refresh` | Estadísticas del modelo, renombre, y evaluador de mejores prácticas. |
| `table_operations` | `Help`, `Create`, `CreateFieldParameter`, `Update`, `Delete`, `Get`, `List`, `RefreshWithXMLA`, `RefreshWithAPI`, `Rename`, `MarkAsDateTable`, `GetSchema`, `ExportTMDL`, `ExportTMSL` | Tablas del modelo, parámetros de campo, marcado como tabla de fechas. |
| `column_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List`, `Rename`, `ExportTMDL` | Columnas estándar y calculadas, tipos de datos, orden por columna. |
| `measure_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List`, `Rename`, `Move`, `ExportTMDL` | Medidas DAX, expresiones, formato, carpetas de visualización y movimiento entre tablas. |
| `relationship_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Relaciones (claves, cardinalidad 1:* ó 1:1, dirección de filtro cruzado, estado activo/inactivo). |
| `dax_query_operations` | `Help`, `Execute`, `Validate`, `ClearCache` | Ejecución y validación sintáctica de consultas DAX (`EVALUATE ...`). |
| `calculation_group_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Grupos y elementos de cálculo para inteligencia de tiempo (YTD, QTD, MoM, etc.). |
| `calendar_operations` | `Help`, `Create`, `GenerateDateRange` | Creación y configuración de tablas calendario automáticas. |
| `user_hierarchy_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Jerarquías de exploración para usuarios finales (ej. Año > Mes > Día). |
| `partition_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Particiones de almacenamiento y refresco incremental. |
| `perspective_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Perspectivas para simplificar la vista del modelo para diferentes audiencias. |
| `security_role_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Roles de seguridad a nivel de fila (RLS) y nivel de objeto (OLS). |
| `named_expression_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Parámetros y consultas de Power Query (lenguaje M). |
| `function_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Funciones personalizadas del modelo. |
| `query_group_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Carpetas organizativas de consultas de Power Query. |
| `culture_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Culturas e idiomas soportados para traducciones. |
| `object_translation_operations` | `Help`, `Create`, `Update`, `Delete`, `Get`, `List` | Traducciones de nombres de tablas, columnas y medidas. |
| `trace_operations` | `Help`, `StartTrace`, `StopTrace`, `GetTraceEvents` | Trazas en vivo para análisis y diagnóstico del motor VertiPaq. |
| `transaction_operations` | `Help`, `Begin`, `Commit`, `Rollback` | Control explícito de transacciones trans-operación en el modelo. |

---

## 3. Patrones de Uso y Ejemplos de Payloads

### A. Conectar al Modelo (Obligatorio antes de cualquier acción)

**A Power BI Desktop local:**
```json
{
  "request": {
    "operation": "Connect",
    "connectionString": "Data Source=localhost:PORT"
  }
}
```
*O listar instancias abiertas:*
```json
{
  "request": {
    "operation": "ListLocalInstances"
  }
}
```

**A un proyecto PBIP / TMDL:**
```json
{
  "request": {
    "operation": "ConnectFolder",
    "folderPath": "c:/Ruta/Al/Proyecto.Dataset/definition"
  }
}
```

---

### B. Crear o Modificar Medidas DAX (`measure_operations`)

**Crear una nueva medida con transacción atómica:**
```json
{
  "request": {
    "operation": "Create",
    "definitions": [
      {
        "name": "Total Ventas",
        "tableName": "Ventas",
        "expression": "SUM(Ventas[Monto])",
        "formatString": "$#,##0.00",
        "displayFolder": "Métricas Clave",
        "description": "Suma del monto total vendido"
      }
    ],
    "options": {
      "useTransaction": true,
      "continueOnError": false
    }
  }
}
```

**Mover una medida a otra tabla (no usar Update):**
```json
{
  "request": {
    "operation": "Move",
    "moveDefinitions": [
      {
        "name": "Total Ventas",
        "destinationTableName": "_Medidas"
      }
    ]
  }
}
```

---

### C. Validar y Ejecutar Consultas DAX (`dax_query_operations`)

**Validar la sintaxis de una medida o cálculo:**
```json
{
  "request": {
    "operation": "Validate",
    "query": "EVALUATE ROW(\"Test\", [Total Ventas])"
  }
}
```

**Ejecutar consulta y obtener resultados inline:**
```json
{
  "request": {
    "operation": "Execute",
    "query": "EVALUATE TOPN(10, Ventas, Ventas[Monto], DESC)",
    "resultMode": "Inline",
    "maxRows": 100
  }
}
```

---

### D. Inspección Previa de Esquemas (`table_operations` / `model_operations`)

**Inspeccionar columnas y tipos de una tabla:**
```json
{
  "request": {
    "operation": "GetSchema",
    "references": [
      {
        "name": "Ventas"
      }
    ]
  }
}
```

**Evaluar mejores prácticas del modelo:**
```json
{
  "request": {
    "operation": "EvaluateBestPractices"
  }
}
```

---

## 4. Reglas Críticas de Calidad y Seguridad

1. **Inspección Previa (Cero Supuestos):** Nunca inferir nombres de columnas o tablas; siempre ejecutar `List` o `GetSchema` primero.
2. **Uso de Variables DAX (`VAR` / `RETURN`):** Redactar medidas legibles, modulares y de alto rendimiento.
3. **Manejo de Transacciones:** Para modificaciones múltiples, utilizar `options: { "useTransaction": true }` para evitar estados intermedios inconsistentes.
4. **Respaldos:** Antes de modificaciones masivas, advertir o asegurar que el archivo `.pbix` o carpeta PBIP tenga copia de seguridad.
