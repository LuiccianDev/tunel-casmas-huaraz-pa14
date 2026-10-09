# AutoCAD MCP Server — Servidor Model Context Protocol

**Versión:** 1.0.0  
**Target Framework:** .NET 10 (`net10.0`)  
**Protocolo:** Model Context Protocol (MCP v2.2)  
**Transporte:** STDIO (JSON-RPC)  
**Backend:** Cliente HTTP hacia AutoCAD AI Gateway (`http://localhost:5055/`)  
**Binarios generados:** `AutoCAD_MCP_Server.dll` (ensamblado administrado) y `AutoCAD_MCP_Server.exe` (ejecutable de Windows)

---

## 1. Propósito y Descripción

El **AutoCAD MCP Server** es un servidor que implementa la especificación estándar del **Model Context Protocol (MCP)** en C# / .NET 10. Su función principal es actuar como la interfaz de inteligencia artificial que permite a asistentes y agentes (como Antigravity, Claude Desktop, Cursor o cualquier cliente compatible con MCP) inspeccionar el dibujo activo en AutoCAD 2027 y ejecutar operaciones de diseño de manera segura y paramétrica.

---

## 2. Aclaración de Binarios (.dll vs .exe)

Al compilar este proyecto con `dotnet build -c Release`, el SDK de .NET genera en la carpeta `bin/Release/net10.0/` dos archivos principales:

1. **`AutoCAD_MCP_Server.dll` (Recomendado y Portátil):**  
   Es la biblioteca de ensamblado IL que contiene toda la lógica compilada del servidor MCP. Se ejecuta invocando el runtime de .NET:
   ```powershell
   dotnet "plugins/AutoCAD_MCP_Server/bin/Release/net10.0/AutoCAD_MCP_Server.dll"
   ```
   **Ventajas:** Es independiente de rutas absolutas duras, compatible con variables de entorno de IDEs como `${workspaceFolder}` y garantiza el uso controlado del SDK de .NET 10.

2. **`AutoCAD_MCP_Server.exe` (Ejecutable Nativo de Windows):**  
   Es el contenedor ejecutable generado por .NET para Windows (apphost). Permite invocar directamente el servidor sin anteponer `dotnet` en la línea de órdenes.

---

## 3. Arquitectura Interna

El servidor sigue los patrones modernos de desarrollo en .NET 10 recomendados en `dotnet-backend-patterns` y `dotnet-mcp-builder`:

```
[ Cliente MCP (Antigravity / VS Code / Claude) ]
                 │
                 │ JSON-RPC vía STDIO (Entrada/Salida Estándar)
                 ▼
        [ AutoCAD MCP Server ]
                 │
                 ├── Program.cs (DI Container + McpServer Host)
                 │
                 ├── [ IAutoCADGatewayClient ] (HttpClient tipado con Timeout)
                 │         │
                 │         ▼ HTTP REST (Puerto 5055)
                 │   [ AutoCAD AI Gateway ] ───> AutoCAD 2027
                 │
                 ├── [ ContextTools ]    ───> 7 Herramientas de Inspección DWG
                 └── [ ExecutionTools ]  ───> 5 Herramientas de Acción y Control
```

### Características de Diseño:
1. **Silenciamiento Estricto de `stdout`:**  
   Se ejecuta `builder.Logging.ClearProviders()` para garantizar que ningún log de diagnóstico contamine la salida estándar (`Console.Out`), la cual queda reservada exclusivamente para el intercambio de tramas JSON-RPC del protocolo MCP.
2. **Inyección de Dependencias (.NET DI):**  
   El cliente HTTP (`IAutoCADGatewayClient`) se registra de forma desacoplada con `AddHttpClient`, inyectándose directamente en los constructores de las clases de herramientas.
3. **Segregación de Responsabilidades:**  
   Las 12 herramientas se dividen lógicamente en herramientas de solo lectura (`ContextTools`) y de acción/control (`ExecutionTools`).

---

## 4. Catálogo de Herramientas MCP (12 Herramientas)

### A. Herramientas de Inspección y Contexto (`ContextTools`)

| Herramienta | Descripción | Parámetros |
|---|---|---|
| **`obtener_info_dibujo`** | Obtiene metadatos del dibujo: nombre de archivo DWG, estado de solo lectura y unidades configuradas (`INSUNITS`). | Ninguno |
| **`leer_objetos_autocad`** | Devuelve el resumen (conteo por tipo) de todas las entidades en el espacio modelo (Line, Polyline, Circle, BlockReference, etc.). | Ninguno |
| **`leer_capas_autocad`** | Lista todas las capas con sus estados (bloqueada, congelada, apagada) y código de color ACI. | Ninguno |
| **`leer_textos_autocad`** | Lista todos los textos (`DBText` y `MText`) con su contenido, capa y coordenadas exactas `(X, Y)`. | Ninguno |
| **`obtener_limites_dibujo`** | Obtiene las coordenadas extremas mínimas y máximas del dibujo (`Extmin` y `Extmax`). | Ninguno |
| **`leer_seleccion_autocad`** | Devuelve la cantidad de entidades que el usuario tiene seleccionadas con el ratón. | Ninguno |
| **`listar_bloques_disponibles`** | Obtiene los nombres de todas las definiciones de bloques cargadas en el archivo actual. | Ninguno |

### B. Herramientas de Ejecución y Configuración (`ExecutionTools`)

| Herramienta | Descripción | Parámetros |
|---|---|---|
| **`ping_autocad_gateway`** | Envía un ping al Gateway en el puerto 5055 para verificar la conectividad activa. | Ninguno |
| **`ejecutar_comando_autocad`** | Inyecta comandos de dibujo, macros AutoLISP o comandos YQArch directamente a AutoCAD. | `command` (cadena con saltos `\n`) |
| **`zoom_extension`** | Ejecuta un Zoom Extensión (`_.ZOOM E`) para centrar y encuadrar todo en pantalla. | Ninguno |
| **`guardar_dibujo`** | Guarda el archivo DWG activo en AutoCAD (`_.QSAVE`). | Ninguno |
| **`configurar_entorno_dibujo`** | Calibra automáticamente las variables métricas del dibujo (`INSUNITS=4`, `MEASUREMENT=1`, `DIMTXT=0.22`, `DIMASZ=0.18`, etc.). | Ninguno |

---

## 5. Configuración en Clientes MCP

### Método 1: Estándar y Recomendado (Portátil con `dotnet` y `${workspaceFolder}`)
Este es el formato estándar configurado en `.vscode/mcp.json` para el espacio de trabajo con token de seguridad:

```json
{
  "servers": {
    "autocad-mcp": {
      "type": "stdio",
      "command": "dotnet",
      "args": [
        "${workspaceFolder}/plugins/AutoCAD_MCP_Server/bin/Release/net10.0/AutoCAD_MCP_Server.dll"
      ],
      "env": {
        "AUTOCAD_GATEWAY_TOKEN": "pa14-autocad-token-casmas-2026"
      }
    }
  }
}
```

### Método 2: En Plugins de Antigravity (`.agents/plugins/autocad-gateway/mcp_config.json`)
Para plugins dentro del workspace con rutas relativas a la raíz y seguridad de token:

```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "dotnet",
      "args": [
        "plugins/AutoCAD_MCP_Server/bin/Release/net10.0/AutoCAD_MCP_Server.dll"
      ],
      "env": {
        "AUTOCAD_GATEWAY_TOKEN": "pa14-autocad-token-casmas-2026"
      }
    }
  }
}
```

### Método 3: Clientes Externos con Binario Directo (`.exe`)
Si se configura un cliente externo de Windows (como Claude Desktop fuera del proyecto) que requiera invocar directamente el ejecutable:

```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "C:\\Users\\DAVID\\Desktop\\WorksSpacesCoding\\Tunel-Casmas-Huaraz-PA14\\plugins\\AutoCAD_MCP_Server\\bin\\Release\\net10.0\\AutoCAD_MCP_Server.exe"
    }
  }
}
```

---

## 6. Compilación

Para compilar el proyecto de forma independiente:
```powershell
dotnet build -c Release plugins/AutoCAD_MCP_Server/AutoCAD_MCP_Server.csproj
```

O compilar toda la solución de integración CAD:
```powershell
.\scripts\build_plugins.ps1
```
