# Documentación del Servidor MCP de Power BI (Power BI Authoring)

Esta guía documenta la integración del servidor MCP oficial de Microsoft ([`@microsoft/powerbi-modeling-mcp`](https://www.npmjs.com/package/@microsoft/powerbi-modeling-mcp)) en el proyecto **Túnel Casmas Huaraz PA14**.

---

## 1. Arquitectura de Integración

El servidor MCP está integrado **exclusivamente a nivel de proyecto (local)**:

1. **Para Antigravity:**
   - Ubicación: `.agents/plugins/powerbi/`
   - Configuración: `plugin.json` y `mcp_config.json`.
   - Reglas de asistente: `.agents/plugins/powerbi/rules/AGENTS.md`.
   - Se carga automáticamente al abrir este espacio de trabajo sin alterar la configuración global de la máquina.

2. **Para VS Code / Cursor / Cline:**
   - Ubicación: `.vscode/mcp.json` bajo la clave `"servers" -> "powerbi"`.
   - Transporte: `stdio` vía `npx` universal.

---

## 2. Configuración Universal (`npx`)

Se utiliza `npx` para evitar depender de rutas absolutas de usuarios locales (`C:\Users\...`):

```json
{
  "powerbi": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "@microsoft/powerbi-modeling-mcp@latest",
      "--start",
      "--accept-eula"
    ],
    "env": {
      "PBI_MODELING_MCP_ACCEPT_EULA": "true"
    }
  }
}
```

### Argumentos Clave:
* `-y`: Permite la ejecución de `npx` sin requerir confirmación interactiva en terminal.
* `--start`: Inicia el servidor MCP en modo predeterminado de lectura/escritura (`ReadWrite`).
* `--accept-eula` y `PBI_MODELING_MCP_ACCEPT_EULA: true`: Acepta el contrato de licencia EULA de Microsoft para ejecución autónoma.

---

## 3. Prerrequisitos de Uso

1. **Node.js**: Instalado en el sistema (compatible con versiones 18+).
2. **Entorno de Datos (uno de los siguientes)**:
   - **Power BI Desktop**: Con el archivo `.pbix` abierto en la máquina local.
   - **Proyecto PBIP / TMDL**: Carpeta con la definición del modelo semántico.
   - **Microsoft Fabric**: Área de trabajo con acceso al modelo semántico en la nube.

---

## 4. Flujo de Trabajo con el Asistente

### Paso 1: Conectar al modelo
El primer comando que se debe dar al asistente es conectar al modelo activo:
```text
Conectar al modelo 'Reporte_PA14' en Power BI Desktop
```

### Paso 2: Consultar estructura
```text
¿Cuáles son las tablas y relaciones actuales en el modelo?
```

### Paso 3: Crear o refactorizar medidas DAX
```text
Crea una medida para calcular el Avance Acumulado de Excavación usando SUMX y valida la fórmula con DAX.
```

### Paso 4: Evaluar mejores prácticas
```text
Evalúa las mejores prácticas de modelado en el modelo semántico y sugiere optimizaciones.
```
