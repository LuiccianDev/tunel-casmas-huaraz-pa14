# Documentación del Servidor MCP de QGIS (Conexión Segura y Zero-Secrets)

Esta guía documenta la integración y configuración segura del servidor MCP oficial de QGIS ([`nkarasiak/qgis-mcp`](https://github.com/nkarasiak/qgis-mcp)) en el proyecto **Túnel Casmas Huaraz PA14**.

---

## 1. Arquitectura de Integración y Principio Zero-Secrets

La integración opera **estrictamente a nivel local** mediante autenticación mutua por token seguro:

```
[Agente de IA / Antigravity / Cursor] 
        │
        ▼ (MCP Stdio / JSON-RPC)
[qgis-mcp-server FastMCP (uvx)]
   ├── Hereda 'QGIS_MCP_TOKEN' desde variables de entorno del S.O.
   └── Lee Host:Port desde configuración (localhost:9876)
        │
        ▼ (Socket TCP 127.0.0.1:9876 con encabezado de Token)
[QGIS MCP Plugin (QGIS Desktop)]
        │
        ▼ (PyQGIS API nativa)
[Proyecto SIG del Túnel PA14 (EPSG:32718)]
```

### Características de Seguridad:
1. **Regla Zero-Secrets:** El token de autenticación **NUNCA** debe guardarse en archivos versionados (`.mcp.json`, `mcp_config.json`, `.git`). Se administra localmente en el sistema operativo del usuario mediante la variable de entorno `QGIS_MCP_TOKEN`.
2. **Autenticación con Token:** Cualquier petición al puerto local `9876` que no envíe el encabezado de autenticación con el token configurado es rechazada inmediatamente por el plugin de QGIS.
3. **Loopback Estricto:** Conexión fijada a `localhost` (`127.0.0.1`), inaccesible desde redes externas, Wi-Fi o máquinas remotas.
4. **Heredación Automática:** Al ejecutarse a través de `uvx`, el servidor MCP hereda automáticamente las variables de entorno de la sesión de Windows.

---

## 2. Configuración del Cliente MCP en el Proyecto

Los archivos de configuración mantienen los parámetros de red (`localhost` y puerto `9876`), prescindiendo de claves o tokens sensibles:

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
        "QGIS_MCP_PORT": "9876"
      }
    }
  }
}
```

### B. Para VS Code / Cursor (`.vscode/mcp.json`)
```json
{
  "servers": {
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
        "QGIS_MCP_PORT": "9876"
      }
    }
  }
}
```

---

## 3. Guía Paso a Paso: Creación del Token y Variables de Entorno en Windows

Para que el servidor MCP se autentique exitosamente contra QGIS Desktop sin exponer contraseñas en el repositorio, la variable `QGIS_MCP_TOKEN` debe existir en el entorno de usuario.

### Método 1: Configuración Permanente vía PowerShell (Recomendado)
Abre una ventana de PowerShell y ejecuta:

```powershell
# 1. Definir el token de acceso seguro (ámbito Usuario, persiste entre reinicios)
[System.Environment]::SetEnvironmentVariable('QGIS_MCP_TOKEN', 'pa14-qgis-token-casmas-2026', 'User')

# 2. (Opcional) Definir host y puerto si deseas estandarizarlos globalmente
[System.Environment]::SetEnvironmentVariable('QGIS_MCP_HOST', 'localhost', 'User')
[System.Environment]::SetEnvironmentVariable('QGIS_MCP_PORT', '9876', 'User')
```

> **Nota:** Después de ejecutar estos comandos, reinicia tu editor (VS Code / Cursor / terminal de Antigravity) para que tome las nuevas variables del perfil de usuario.

---

### Método 2: Interfaz Gráfica de Windows (GUI)
Si prefieres configurar las variables visualmente:

1. Presiona `Win + R`, escribe:
   ```text
   sysdm.cpl
   ```
   y presiona **Enter**.
2. Dirígete a la pestaña **Opciones avanzadas** y haz clic en **Variables de entorno...**.
3. En la sección superior (**Variables de usuario para [TuUsuario]**), haz clic en **Nueva...**:
   * **Nombre de la variable:** `QGIS_MCP_TOKEN`
   * **Valor de la variable:** `pa14-qgis-token-casmas-2026` (o tu token personalizado)
4. (Opcional) Puedes agregar también `QGIS_MCP_HOST` con valor `localhost` y `QGIS_MCP_PORT` con valor `9876`.
5. Haz clic en **Aceptar** en todas las ventanas para guardar los cambios.

---

### Método 3: Consola de Comandos (CMD)
Desde una consola CMD:

```cmd
setx QGIS_MCP_TOKEN "pa14-qgis-token-casmas-2026"
```

---

## 4. Configuración del Token en QGIS Desktop

Para emparejar QGIS con el servidor MCP:

### A. Desde la Interfaz Gráfica del Plugin en QGIS
1. Abre **QGIS Desktop** (versión 3.28 o superior).
2. Si aún no tienes el complemento, ve a **Complementos** > **Administrar e instalar complementos**, busca **QGIS MCP** e instálalo.
3. Abre el panel lateral **QGIS MCP**.
4. En el campo de configuración **Token**, introduce exactamente el mismo valor:
   ```text
   pa14-qgis-token-casmas-2026
   ```
5. Verifica que el puerto sea `9876` y haz clic en **Start Server** (Iniciar Servidor).
6. La luz indicadora cambiará a verde indicando que el socket TCP está escuchando.

### B. Desde la Consola Python de QGIS (PyQGIS)
Si deseas configurar el token directamente por código dentro de QGIS:
1. Abre la consola de Python en QGIS (`Ctrl + Alt + P`).
2. Ejecuta el siguiente fragmento:
   ```python
   from qgis.PyQt.QtCore import QSettings

   s = QSettings()
   s.setValue("qgis_mcp/token", "pa14-qgis-token-casmas-2026")
   s.setValue("qgis_mcp/port", 9876)
   print("Token y puerto de QGIS MCP configurados exitosamente en QSettings.")
   ```

---

## 5. Diagnóstico y Verificación de Conexión

### Paso 1: Verificar que Windows reconoce la variable de entorno
En PowerShell ejecuta:

```powershell
Get-ChildItem Env:QGIS_MCP_*
```

Salida esperada:
```text
Name                           Value
----                           -----
QGIS_MCP_HOST                  localhost
QGIS_MCP_PORT                  9876
QGIS_MCP_TOKEN                 pa14-qgis-token-casmas-2026
```

### Paso 2: Prueba de Conectividad con el Asistente (Ping)
En el chat del asistente de IA, solicita:
> *"Llama a la herramienta ping de QGIS"*

Respuesta esperada:
```json
{
  "pong": true
}
```

---

## 6. Casos de Uso en el Túnel Casmas Huaraz PA14
* **Verificación de SRC:** Asegurarse de que el proyecto trabaje en **WGS 84 / UTM Zona 18S (EPSG:32718)**.
* **Trazado de Eje y Portales:** Cargar el eje del túnel ($L = 5539.3\text{ m}$) y ubicar los portales Este (Casma) y Oeste (Huaraz).
* **Capas Geológicas y Cobertura:** Consultar capas de fallas geológicas, litología y curvas de nivel para el cálculo de sobrecapa.
* **Áreas de Instalación:** Ubicar y delimitar campamentos, polvorines, canteras y botaderos sobre la ortofoto o mapa base.
