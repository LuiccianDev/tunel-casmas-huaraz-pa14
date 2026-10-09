# Documentación del Servidor MCP de QGIS (Conexión Segura)

Esta guía documenta la integración y configuración segura del servidor MCP oficial de QGIS ([`nkarasiak/qgis-mcp`](https://github.com/nkarasiak/qgis-mcp)) en el proyecto **Túnel Casmas Huaraz PA14**.

---

## 1. Arquitectura de Integración y Seguridad

La integración opera **estrictamente a nivel de proyecto (local)** con autenticación mutua por token:

```
[Agente de IA / Antigravity] 
        │
        ▼ (MCP Stdio / JSON-RPC)
[qgis-mcp-server FastMCP (uvx)]
        │
        ▼ (Socket TCP 127.0.0.1:9876 con Token 'pa14-qgis-token-casmas-2026')
[QGIS MCP Plugin (QGIS Desktop)]
        │
        ▼ (PyQGIS API nativa)
[Proyecto SIG del Túnel PA14]
```

### Características de Seguridad:
1. **Autenticación con Token:** Cualquier petición al puerto local `9876` que no envíe el encabezado de autenticación con el token `pa14-qgis-token-casmas-2026` es rechazada inmediatamente.
2. **Loopback Estricto:** Conexión fijada a `localhost` (`127.0.0.1`), inaccesible desde redes externas o Wi-Fi.
3. **Aislamiento de Proyecto:** Configurado exclusivamente en `.agents/plugins/qgis/` y `.vscode/mcp.json`. Cero impacto en la configuración global del sistema (`~/.gemini/config/`).

---

## 2. Configuración en el Proyecto

### A. Para Antigravity (`.agents/plugins/qgis/mcp_config.json`)
```json
{
  "mcpServers": {
    "qgis": {
      "command": "uvx",
      "args": [
        "--from",
        "https://github.com/nkarasiak/qgis-mcp/archive/refs/heads/main.zip",
        "qgis-mcp-server"
      ],
      "env": {
        "QGIS_MCP_HOST": "localhost",
        "QGIS_MCP_PORT": "9876",
        "QGIS_MCP_TOKEN": "pa14-qgis-token-casmas-2026"
      }
    }
  }
}
```

### B. Para VS Code / Cursor (`.vscode/mcp.json`)
```json
{
  "qgis": {
    "type": "stdio",
    "command": "uvx",
    "args": [
      "--from",
      "https://github.com/nkarasiak/qgis-mcp/archive/refs/heads/main.zip",
      "qgis-mcp-server"
    ],
    "env": {
      "QGIS_MCP_HOST": "localhost",
      "QGIS_MCP_PORT": "9876",
      "QGIS_MCP_TOKEN": "pa14-qgis-token-casmas-2026"
    }
  }
}
```

---

## 3. Pasos de Puesta en Marcha en QGIS Desktop

1. **Instalar el complemento:**
   * Abre **QGIS** (versión 3.28 o superior).
   * Ve a **Complementos** > **Administrar e instalar complementos**.
   * Busca **QGIS MCP** e instálalo.
2. **Configurar el Token de Seguridad:**
   * Abre el panel acoplable de **QGIS MCP**.
   * En la configuración del plugin, introduce el token:
     ```text
     pa14-qgis-token-casmas-2026
     ```
   * *(Alternativamente, puedes definir en Windows la variable de entorno `QGIS_MCP_TOKEN=pa14-qgis-token-casmas-2026` antes de abrir QGIS).*
3. **Iniciar el Servidor:**
   * Haz clic en **Start Server** en el panel de QGIS MCP.
   * El indicador mostrará que el servidor TCP está escuchando en `localhost:9876`.

---

## 4. Verificación y Casos de Uso con el Asistente

### Paso 1: Prueba de Conectividad (Ping)
En el chat del asistente, ejecuta:
> *"Llama a la herramienta ping de QGIS"*

Respuesta esperada:
```json
{"pong": true}
```

### Paso 2: Casos de Uso en el Túnel Casmas Huaraz PA14
* **Verificación de SRC:** Asegurarse de que el proyecto trabaje en **WGS 84 / UTM Zona 18S (EPSG:32718)**.
* **Trazado de Eje y Portales:** Cargar el eje del túnel ($L = 5539.3\text{ m}$) y ubicar los portales Este (Casma) y Oeste (Huaraz).
* **Capas Geológicas y Cobertura:** Consultar capas de fallas geológicas, litología y curvas de nivel para el cálculo de sobrecapa.
* **Áreas de Instalación:** Ubicar y delimitar campamentos, polvorines, canteras y botaderos sobre la ortofoto o mapa base.
