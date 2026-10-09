# Documentación: Servidor MCP para AutoCAD AI

Este documento explica de manera detallada qué es el Model Context Protocol (MCP), cómo funciona nuestra arquitectura modular con AutoCAD, cómo se invocan las herramientas y cómo se ejecutan los binarios correspondientes.

---

## 1. ¿Qué es MCP (Model Context Protocol)?
El **MCP** es un protocolo estándar y de código abierto creado para que los modelos de Inteligencia Artificial puedan conectarse de manera segura a herramientas externas, bases de datos o programas (en este caso, AutoCAD).

En lugar de que la IA tenga que adivinar o crear códigos complejos para cada programa del mundo, el MCP establece un "idioma universal". El servidor MCP le dice a la IA: *"Hola, tengo estas 12 herramientas (Tools) disponibles, aquí están las instrucciones de cómo usarlas"*.

---

## 2. Arquitectura de Funcionamiento (El Puente)
Para que AutoCAD y la IA se comuniquen sin colapsar el programa de escritorio, hemos implementado una **arquitectura de puente en 3 pasos**:

1. **La IA (Antigravity / Claude):** Decide qué operación requiere en AutoCAD (por ejemplo, leer capas, consultar límites espaciales o dibujar una entidad).
2. **El Servidor MCP (`AutoCAD_MCP_Server` en consola):** Es una aplicación de consola en .NET 10 que escucha en segundo plano mediante `STDIO`. Traduce las intenciones de la IA a peticiones HTTP REST hacia el puerto `5055`.
3. **El Gateway Nativo (`AutoCAD_AI_Gateway` en AutoCAD):** Recibe la petición HTTP, interactúa con el DWG en el hilo principal (`Application.Idle`) y devuelve el resultado.

### Pregunta Clave: ¿Por qué no conectar la IA directamente al Gateway de AutoCAD?
1. **El Idioma Universal:** El MCP es un estándar que inyecta automáticamente el menú de herramientas disponibles de forma nativa en la IA.
2. **El "Guardia de Seguridad" (Estabilidad):** AutoCAD es un entorno monohilo sensible. El servidor MCP valida las solicitudes, gestiona timeouts y actúa como un escudo protector: si algo falla en la red, AutoCAD permanece completamente intacto.
3. **Traducción Pesada:** Operaciones masivas de lectura de geometrías son procesadas por el servidor MCP, reduciendo la carga sobre AutoCAD.

---

## 3. Naturaleza de los Binarios (.dll vs .exe)

Es fundamental distinguir el rol y tipo de salida binaria de cada componente tras ejecutar `dotnet build -c Release`:

| Componente | Tipo de Proyecto | Binario Producido | Cómo se Ejecuta |
|---|---|---|---|
| **`AutoCAD_AI_Gateway`** | Class Library (`net10.0-windows`) | `AutoCAD_AI_Gateway.dll` | Se carga **dentro de AutoCAD** mediante el comando `NETLOAD`. No genera un ejecutable `.exe` independiente. |
| **`AutoCAD_MCP_Server`** | Console Application (`net10.0`) | `AutoCAD_MCP_Server.dll` y `AutoCAD_MCP_Server.exe` | Proceso independiente ejecutado por el cliente de IA mediante `STDIO`. |

### Invocación Recomendada del Servidor MCP:
En `.vscode/mcp.json` y los plugins de Antigravity, la invocación estándar y portátil se realiza mediante el runtime de .NET ejecutando la DLL compilada:
```json
{
  "command": "dotnet",
  "args": [
    "${workspaceFolder}/plugins/AutoCAD_MCP_Server/bin/Release/net10.0/AutoCAD_MCP_Server.dll"
  ]
}
```
Esto evita codificar rutas absolutas y garantiza portabilidad entre diferentes equipos de trabajo.

---

## 4. Invocación y Herramientas Modulares
La arquitectura de herramientas está modularizada en dos clases principales:

1. **`ContextTools.cs` (7 herramientas de inspección):**  
   `obtener_info_dibujo`, `leer_objetos_autocad`, `leer_capas_autocad`, `leer_textos_autocad`, `obtener_limites_dibujo`, `leer_seleccion_autocad`, `listar_bloques_disponibles`.
2. **`ExecutionTools.cs` (5 herramientas de acción):**  
   `ping_autocad_gateway`, `ejecutar_comando_autocad`, `zoom_extension`, `guardar_dibujo`, `configurar_entorno_dibujo`.

---

## 5. Habilitación y Uso

Para habilitar todo este flujo, el entorno requiere que ambas partes del puente estén activas:

1. **Habilitar AutoCAD:** 
   - Abre AutoCAD 2027.
   - Carga el plugin nativo mediante `NETLOAD` seleccionando `plugins/AutoCAD_AI_Gateway/bin/Release/net10.0-windows/AutoCAD_AI_Gateway.dll`.
   - Inicia el servidor de escucha con el comando `AI_START_SERVER` (escucha en `http://localhost:5055/`).
2. **Habilitar el Servidor MCP:**
   - Antigravity y VS Code inician automáticamente el proceso según la configuración de `.vscode/mcp.json` o `.agents/plugins/autocad-gateway/mcp_config.json`.
